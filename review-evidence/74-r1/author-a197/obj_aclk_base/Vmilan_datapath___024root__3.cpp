// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

extern const VlWide<28>/*895:0*/ Vmilan_datapath__ConstPool__CONST_hca6ff4b2_0;
extern const VlUnpacked<CData/*0:0*/, 14> Vmilan_datapath__ConstPool__TABLE_h90282f34_0;
extern const VlUnpacked<CData/*2:0*/, 16> Vmilan_datapath__ConstPool__TABLE_h1b26f04f_0;
extern const VlWide<47>/*1503:0*/ Vmilan_datapath__ConstPool__CONST_hbff50867_0;
extern const VlWide<13>/*415:0*/ Vmilan_datapath__ConstPool__CONST_hb995d365_0;
extern const VlWide<9>/*287:0*/ Vmilan_datapath__ConstPool__CONST_hc5471b50_0;

void Vmilan_datapath___024root___nba_sequent__TOP__2(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___nba_sequent__TOP__2\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*6:0*/ milan_datapath__DOT__csr_tctx_rd_addr_w;
    milan_datapath__DOT__csr_tctx_rd_addr_w = 0;
    CData/*7:0*/ milan_datapath__DOT__tdm_lane_streams__DOT__rword;
    milan_datapath__DOT__tdm_lane_streams__DOT__rword = 0;
    CData/*3:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__free_mask_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__free_mask_w = 0;
    CData/*3:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__free_mask_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__free_mask_w = 0;
    CData/*3:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__free_mask_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__free_mask_w = 0;
    CData/*3:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__free_mask_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__free_mask_w = 0;
    QData/*63:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s = 0;
    IData/*31:0*/ milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__diff_w;
    milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__diff_w = 0;
    CData/*0:0*/ milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run_v;
    milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run_v = 0;
    CData/*0:0*/ milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run0_v;
    milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run0_v = 0;
    IData/*31:0*/ milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__diff_w;
    milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__diff_w = 0;
    CData/*0:0*/ milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run_v;
    milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run_v = 0;
    CData/*0:0*/ milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run0_v;
    milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run0_v = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_allowed__54__command_type;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_allowed__54__command_type = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__182__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__182__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__183__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__183__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__184__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__184__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__185__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__185__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__186__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__186__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__187__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__187__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__188__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__188__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__189__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__189__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__190__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__190__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__191__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__191__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__192__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__192__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__193__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__193__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__194__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__194__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__195__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__195__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__196__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__196__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__197__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__197__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__198__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__198__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__199__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__199__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__200__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__200__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__201__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__201__w = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_acc__257__Vfuncout;
    __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_acc__257__Vfuncout = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_acc__257__v;
    __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_acc__257__v = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_u__258__Vfuncout;
    __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_u__258__Vfuncout = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_u__258__v;
    __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_u__258__v = 0;
    CData/*4:0*/ __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__302__Vfuncout;
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__302__Vfuncout = 0;
    CData/*0:0*/ __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__302__t;
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__302__t = 0;
    CData/*2:0*/ __VdfgRegularize_h6e95ff9d_0_51;
    __VdfgRegularize_h6e95ff9d_0_51 = 0;
    CData/*2:0*/ __VdfgRegularize_h6e95ff9d_0_52;
    __VdfgRegularize_h6e95ff9d_0_52 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_179;
    __VdfgRegularize_h6e95ff9d_0_179 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_182;
    __VdfgRegularize_h6e95ff9d_0_182 = 0;
    CData/*1:0*/ __VdfgRegularize_h6e95ff9d_0_185;
    __VdfgRegularize_h6e95ff9d_0_185 = 0;
    CData/*1:0*/ __VdfgRegularize_h6e95ff9d_0_186;
    __VdfgRegularize_h6e95ff9d_0_186 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_284;
    __VdfgRegularize_h6e95ff9d_0_284 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_295;
    __VdfgRegularize_h6e95ff9d_0_295 = 0;
    CData/*0:0*/ __VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__pend_r__v0;
    __VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__pend_r__v0 = 0;
    IData/*23:0*/ __VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v0;
    __VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v0 = 0;
    CData/*4:0*/ __VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v0;
    __VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v0 = 0;
    IData/*23:0*/ __VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r__v0;
    __VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r__v0 = 0;
    CData/*4:0*/ __VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r__v0;
    __VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r__v0 = 0;
    CData/*0:0*/ __VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v0;
    __VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v0 = 0;
    CData/*2:0*/ __VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v1;
    __VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v1 = 0;
    VlWide<14>/*447:0*/ __Vtemp_36;
    VlWide<9>/*287:0*/ __Vtemp_38;
    IData/*31:0*/ __Vtemp_39;
    VlWide<3>/*95:0*/ __Vtemp_46;
    IData/*31:0*/ __Vilp1;
    // Body
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r) 
                  >> 3U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_pick_ix_w = 3U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_slot_w 
            = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_slot_r) 
                     >> 6U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r) 
                  >> 4U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_pick_ix_w = 4U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_slot_w 
            = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_slot_r) 
                     >> 8U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w)) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r) 
            >> 5U))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_pick_ix_w = 5U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_slot_w 
            = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_slot_r) 
                     >> 0x0aU));
    }
    vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__sof 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__in_frame)) 
           & (IData)(vlSelfRef.s_axis_mac_rx_tvalid));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__push_ram_w 
        = ((0U != (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_cnt_r)) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_v_r) 
              >> (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_rp_r)));
    vlSelfRef.s_axi_bvalid = vlSelfRef.milan_datapath__DOT__csr__DOT__b_valid;
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_240 = ((4U 
                                                   >= 
                                                   (7U 
                                                    & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r)) 
                                                  & (((((2U 
                                                         == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[4U]) 
                                                        << 4U) 
                                                       | (((2U 
                                                            == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[3U]) 
                                                           << 3U) 
                                                          | ((2U 
                                                              == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[2U]) 
                                                             << 2U))) 
                                                      | (((2U 
                                                           == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[1U]) 
                                                          << 1U) 
                                                         | (2U 
                                                            == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[0U]))) 
                                                     >> 
                                                     (7U 
                                                      & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_img_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_live_r) 
           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_cap_r));
    vlSelfRef.o_mac_ifg = (0x000000ffU & vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ifg);
    vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[0U] 
        = vlSelfRef.milan_datapath__DOT__avtprx_locked_c;
    vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[1U] 
        = vlSelfRef.milan_datapath__DOT__avtprx_unlocked_c;
    vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[2U] 
        = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__avtprx_seqmm_c)) 
                    << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__avtprx_intr_c))));
    vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[3U] 
        = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__avtprx_seqmm_c)) 
                     << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__avtprx_intr_c))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[4U] 
        = vlSelfRef.milan_datapath__DOT__avtprx_mreset_c;
    vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[5U] 
        = vlSelfRef.milan_datapath__DOT__avtprx_tu_c;
    vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[6U] 
        = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__avtprx_late_c)) 
                    << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__avtprx_unsupp_c))));
    vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[7U] 
        = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__avtprx_late_c)) 
                     << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__avtprx_unsupp_c))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[8U] 
        = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__avtprx_frx_c)) 
                    << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__avtprx_early_c))));
    vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[9U] 
        = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__avtprx_frx_c)) 
                     << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__avtprx_early_c))) 
                   >> 0x00000020U));
    vlSelfRef.o_mc_hash = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mc_hi)) 
                            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mc_lo)));
    vlSelfRef.milan_datapath__DOT__cfg_crft_dmac = 
        (((QData)((IData)((0x0000ffffU & vlSelfRef.milan_datapath__DOT__csr__DOT__crft_dmhi))) 
          << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__crft_dmlo)));
    vlSelfRef.milan_datapath__DOT__cfg_crft_sid = (
                                                   ((QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__crft_sidhi)) 
                                                    << 0x00000020U) 
                                                   | (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__crft_sidlo)));
    vlSelfRef.o_mac_tx_en = (1U & vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ctrl);
    vlSelfRef.o_mac_rx_en = (1U & (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ctrl 
                                   >> 1U));
    vlSelfRef.o_mac_promisc = (1U & (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ctrl 
                                     >> 2U));
    vlSelfRef.o_mac_allmulti = (1U & (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ctrl 
                                      >> 3U));
    vlSelfRef.milan_datapath__DOT__pp_aecp_cur_config_w 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__cfg_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p1_en_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__wr_en_w));
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__s_tlast_q 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.s_axis_mac_rx_tlast));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__134__Vfuncout;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_next_w 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__link_up_q_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__eff_link_w));
    vlSelfRef.o_mac_addr = (((QData)((IData)((0x0000ffffU 
                                              & vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ahi))) 
                             << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_alo)));
    vlSelfRef.milan_datapath__DOT__link_guard__DOT__both_alive_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__rx_alive_r) 
           & (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__tx_alive_r));
    vlSelfRef.s_axi_rvalid = vlSelfRef.milan_datapath__DOT__csr__DOT__r_valid;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__free_mask_w 
        = (0x0000000fU & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__writing_r) 
                             | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__occupied_r))));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__free_mask_w 
        = (0x0000000fU & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__writing_r) 
                             | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__occupied_r))));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__free_mask_w 
        = (0x0000000fU & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__writing_r) 
                             | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__occupied_r))));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__free_mask_w 
        = (0x0000000fU & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__writing_r) 
                             | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__occupied_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__free_mask_w 
        = (0x0000000fU & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__writing_r) 
                             | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__occupied_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ok_w = 0U;
    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__exp_pend_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ok_w = 1U;
    }
    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__exp_pend_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ok_w = 1U;
    }
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__exp_pend_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ok_w = 1U;
    }
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__exp_pend_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ok_w = 1U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_sink_w = 0U;
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_sink_w = 0U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w)) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r) 
            >> 1U))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_sink_w = 1U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_pop_w 
        = ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_st_r) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_sel_r)) 
            << 1U) | ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_sel_r)) 
                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_st_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_push_w 
        = ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_v_w) 
             & (0x20U != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r[1U])) 
            << 1U) | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_v_w) 
                      & (0x20U != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r[0U])));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_ix_w = 0U;
    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_ix_w = 3U;
    }
    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_ix_w = 2U;
    }
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_ix_w = 1U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_ok_w = 0U;
    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_ok_w = 1U;
    }
    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_ok_w = 1U;
    }
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_ok_w = 1U;
    }
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_ix_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_ok_w = 1U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_sink_w = 0U;
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_evt_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_sink_w = 0U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w)) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_evt_r) 
            >> 1U))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_sink_w = 1U;
    }
    vlSelfRef.milan_datapath__DOT__rsp_render_tick_p_w 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__tick_d_r));
    __Vtemp_36[0U] = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_vlan_r) 
                      << 0x00000010U);
    __Vtemp_36[1U] = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_seq_r) 
                       << 0x00000010U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_flags_r));
    __Vtemp_36[2U] = (IData)(((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_da_r 
                               << 0x00000010U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_cc_r))));
    __Vtemp_36[3U] = (IData)((((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_da_r 
                                << 0x00000010U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_cc_r))) 
                              >> 0x00000020U));
    __Vtemp_36[4U] = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_tkuid_r) 
                       << 0x00000010U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_lsuid_r));
    __Vtemp_36[5U] = (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_lseid_r);
    __Vtemp_36[6U] = (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_lseid_r 
                              >> 0x00000020U));
    __Vtemp_36[7U] = (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_tkeid_r);
    __Vtemp_36[8U] = (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_tkeid_r 
                              >> 0x00000020U));
    __Vtemp_36[9U] = (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_ctlr_r);
    __Vtemp_36[10U] = (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_ctlr_r 
                               >> 0x00000020U));
    __Vtemp_36[11U] = (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_sid_r);
    __Vtemp_36[12U] = (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_sid_r 
                               >> 0x00000020U));
    __Vtemp_36[13U] = (0xfc00002cU | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_msg_r) 
                                       << 0x00000010U) 
                                      | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_status_r) 
                                         << 0x0000000bU)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_pdu_byte_w 
        = (0x000000ffU & ((((0U == (0x0000001fU & ((IData)(0x01b8U) 
                                                   - 
                                                   ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_bidx_r) 
                                                    << 3U))))
                             ? 0U : (__Vtemp_36[(((IData)(7U) 
                                                  + 
                                                  (0x000001ffU 
                                                   & ((IData)(0x01b8U) 
                                                      - 
                                                      ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_bidx_r) 
                                                       << 3U)))) 
                                                 >> 5U)] 
                                     << ((IData)(0x00000020U) 
                                         - (0x0000001fU 
                                            & ((IData)(0x01b8U) 
                                               - ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_bidx_r) 
                                                  << 3U)))))) 
                           | (__Vtemp_36[(0x0000000fU 
                                          & (((IData)(0x01b8U) 
                                              - ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_bidx_r) 
                                                 << 3U)) 
                                             >> 5U))] 
                              >> (0x0000001fU & ((IData)(0x01b8U) 
                                                 - 
                                                 ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_bidx_r) 
                                                  << 3U))))) 
                          & (- (IData)((0x01bfU >= 
                                        (0x000001ffU 
                                         & ((IData)(0x01b8U) 
                                            - ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_bidx_r) 
                                               << 3U))))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__trc_rd_data_w = 0U;
    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__rd_lane_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__trc_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__rd_word_r[3U];
    }
    if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__rd_lane_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__trc_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__rd_word_r[2U];
    }
    if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__rd_lane_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__trc_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__rd_word_r[1U];
    }
    if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__rd_lane_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__trc_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__rd_word_r[0U];
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__maap_txn_ready_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_valid_r) 
           & ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r)) 
              | (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r))));
    vlSelfRef.o_eth_rst = vlSelfRef.milan_datapath__DOT__link_guard__DOT__eth_rst_r;
    vlSelfRef.milan_datapath__DOT__link_guard__DOT__man_reinit_r 
        = (1U & (vlSelfRef.milan_datapath__DOT__csr__DOT__link_ctrl 
                 >> 1U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__pend_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__pend_r) 
           | (0U != (((((((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[0U] 
                           | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[1U]) 
                          | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[2U]) 
                         | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[3U]) 
                        | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[4U]) 
                       | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[5U]) 
                      | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[6U]) 
                     | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[7U])));
    vlSelfRef.milan_datapath__DOT__mga_engaged_q_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__engaged_r));
    vlSelfRef.o_irq_csr = (0U != (vlSelfRef.milan_datapath__DOT__csr__DOT__irq_status 
                                  & vlSelfRef.milan_datapath__DOT__csr__DOT__irq_mask));
    vlSelfRef.milan_datapath__DOT__evt_link_change 
        = ((IData)(vlSelfRef.axis_resetn) && ((IData)(vlSelfRef.milan_datapath__DOT__speed_q) 
                                              != (IData)(vlSelfRef.milan_datapath__DOT__speed_sync)));
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w 
        = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r) 
                 - (IData)(1U)));
    milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__diff_w 
        = (vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__cyc_r 
           - vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__prevc_r);
    milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__diff_w 
        = (vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__cyc_r 
           - vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__prevc_r);
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w 
        = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r) 
                 - (IData)(1U)));
    vlSelfRef.milan_datapath__DOT__ltap_regs_w[0U] 
        = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__epoch_r;
    vlSelfRef.milan_datapath__DOT__ltap_regs_w[1U] 
        = (IData)((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[0U]) 
                                      << 0x00000010U) 
                                     | vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r[0U]))) 
                    << 0x00000020U) | (QData)((IData)(
                                                      (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__timeouts_r) 
                                                        << 0x00000010U) 
                                                       | (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__samples_r))))));
    vlSelfRef.milan_datapath__DOT__ltap_regs_w[2U] 
        = (IData)(((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[0U]) 
                                       << 0x00000010U) 
                                      | vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r[0U]))) 
                     << 0x00000020U) | (QData)((IData)(
                                                       (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__timeouts_r) 
                                                         << 0x00000010U) 
                                                        | (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__samples_r))))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__ltap_regs_w[3U] 
        = (IData)((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[1U]) 
                                      << 0x00000010U) 
                                     | vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r[1U]))) 
                    << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[0U]))));
    vlSelfRef.milan_datapath__DOT__ltap_regs_w[4U] 
        = (IData)(((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[1U]) 
                                       << 0x00000010U) 
                                      | vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r[1U]))) 
                     << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[0U]))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__ltap_regs_w[5U] 
        = (IData)((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[2U]) 
                                      << 0x00000010U) 
                                     | vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r[2U]))) 
                    << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[1U]))));
    vlSelfRef.milan_datapath__DOT__ltap_regs_w[6U] 
        = (IData)(((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[2U]) 
                                       << 0x00000010U) 
                                      | vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r[2U]))) 
                     << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[1U]))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__ltap_regs_w[7U] 
        = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__epoch_r)) 
                    << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[2U]))));
    vlSelfRef.milan_datapath__DOT__ltap_regs_w[8U] 
        = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__epoch_r)) 
                     << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[2U]))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__ltap_regs_w[9U] 
        = (IData)((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[0U]) 
                                      << 0x00000010U) 
                                     | vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r[0U]))) 
                    << 0x00000020U) | (QData)((IData)(
                                                      (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__timeouts_r) 
                                                        << 0x00000010U) 
                                                       | (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__samples_r))))));
    vlSelfRef.milan_datapath__DOT__ltap_regs_w[10U] 
        = (IData)(((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[0U]) 
                                       << 0x00000010U) 
                                      | vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r[0U]))) 
                     << 0x00000020U) | (QData)((IData)(
                                                       (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__timeouts_r) 
                                                         << 0x00000010U) 
                                                        | (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__samples_r))))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__ltap_regs_w[11U] 
        = (IData)((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[1U]) 
                                      << 0x00000010U) 
                                     | vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r[1U]))) 
                    << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[0U]))));
    vlSelfRef.milan_datapath__DOT__ltap_regs_w[12U] 
        = (IData)(((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[1U]) 
                                       << 0x00000010U) 
                                      | vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r[1U]))) 
                     << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[0U]))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__ltap_regs_w[13U] 
        = (IData)((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[2U]) 
                                      << 0x00000010U) 
                                     | vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r[2U]))) 
                    << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[1U]))));
    vlSelfRef.milan_datapath__DOT__ltap_regs_w[14U] 
        = (IData)(((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[2U]) 
                                       << 0x00000010U) 
                                      | vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r[2U]))) 
                     << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[1U]))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__ltap_regs_w[15U] 
        = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[2U];
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_265 = (7U 
                                                  & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
                                                     - 
                                                     (1U 
                                                      & (- (IData)(
                                                                   (0U 
                                                                    != 
                                                                    (7U 
                                                                     & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_285 = ((0U 
                                                   == 
                                                   (1U 
                                                    & (- (IData)(
                                                                 (0U 
                                                                  != 
                                                                  (7U 
                                                                   & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r)))))) 
                                                  & (0U 
                                                     != 
                                                     (7U 
                                                      & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
                                                         >> 3U))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_q_r 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_r
        [((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r))
           ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__scan_ix_r)
           : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ridx_r))];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w = 0U;
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w 
            = (0x00000fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r);
    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w 
            = (0x00000fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r);
    }
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w)))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w 
                = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r 
                                  >> 0x0cU));
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w 
                = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r 
                                  >> 0x0cU));
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w = 0U;
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w 
            = (0x00000fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r);
    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w 
            = (0x00000fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r);
    }
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w)))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w 
                = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r 
                                  >> 0x0cU));
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w 
                = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r 
                                  >> 0x0cU));
        }
    }
    vlSelfRef.milan_datapath__DOT__rmap_rd_valid_r 
        = ((IData)(vlSelfRef.axis_resetn) & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_busy_r) 
                                             & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_side_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__byte_acc_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_active_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_en_r) 
              & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_closed_r)) 
                 & (0x0240U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_ptr_r)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__byte_acc_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_active_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_en_r) 
              & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_closed_r)) 
                 & (0x0240U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_ptr_r)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__byte_acc_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_active_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_en_r) 
              & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_closed_r)) 
                 & (0x0240U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_ptr_r)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__byte_acc_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_active_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_en_r) 
              & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_closed_r)) 
                 & (0x0240U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_ptr_r)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__byte_acc_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_active_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_en_r) 
              & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_closed_r)) 
                 & (0x0240U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_ptr_r)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_l_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p1_l_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_avail_w 
        = (1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__gp_valid_r) 
                    | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_busy_r) 
                       | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_stale_r))))));
    vlSelfRef.s_axi_rdata = vlSelfRef.milan_datapath__DOT__csr__DOT__r_data;
    vlSelfRef.milan_datapath__DOT__csr__DOT__rd_pend2 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_pend));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__open_w 
        = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_open_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__ll_val_w 
        = (0x000007ffU & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__waddr_r) 
                           - (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__ll_addr_r)) 
                          - (IData)(2U)));
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cur_app_r) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_type_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_ev_w 
            = (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mvrp_q_r 
                     >> 0x00000010U));
        __Vtemp_38[0U] = 0U;
        __Vtemp_38[1U] = 0U;
        __Vtemp_38[2U] = 0U;
        __Vtemp_38[3U] = 0U;
        __Vtemp_38[4U] = 0U;
        __Vtemp_38[5U] = 0U;
        __Vtemp_38[6U] = 0U;
        __Vtemp_38[7U] = 0U;
        __Vtemp_38[8U] = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mvrp_q_r);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__alen_w = 2U;
    } else {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_type_w 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[8U] 
                              >> 0x00000015U));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_ev_w 
            = (7U & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[8U] 
                      << 0x0000000eU) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[8U] 
                                         >> 0x00000012U)));
        __Vtemp_38[0U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[0U];
        __Vtemp_38[1U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[1U];
        __Vtemp_38[2U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[2U];
        __Vtemp_38[3U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[3U];
        __Vtemp_38[4U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[4U];
        __Vtemp_38[5U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[5U];
        __Vtemp_38[6U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[6U];
        __Vtemp_38[7U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[7U];
        __Vtemp_38[8U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[8U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__alen_w 
            = ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r))
                ? 0x19U : ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r))
                            ? 0x22U : ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r))
                                        ? 8U : (4U 
                                                & (- (IData)(
                                                             (4U 
                                                              == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r))))))));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_fp_w 
        = (3U & (((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[8U] 
                   << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[8U] 
                                      >> 0x00000010U)) 
                 & (- (IData)((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cur_app_r)))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[0U] 
        = __Vtemp_38[0U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[1U] 
        = __Vtemp_38[1U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[2U] 
        = __Vtemp_38[2U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[3U] 
        = __Vtemp_38[3U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[4U] 
        = __Vtemp_38[4U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[5U] 
        = __Vtemp_38[5U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[6U] 
        = __Vtemp_38[6U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[7U] 
        = __Vtemp_38[7U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[8U] 
        = (0x0000ffffU & __Vtemp_38[8U]);
    vlSelfRef.milan_datapath__DOT__strtbl_sid_w = (vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[0U]
                                                    ? vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[0U]
                                                    : 
                                                   (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[1U])) 
                                                     << 0x00000020U) 
                                                    | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[0U]))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_168 = (1U 
                                                  & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_busy_r)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_169 = (1U 
                                                  & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_dir_r)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_170 = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_rden_r) 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_dir_r));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_188 = ((~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_dir_r)) 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_rden_r));
    if ((1U & (~ (IData)(vlSelfRef.axis_resetn)))) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_status_q_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_probing_q_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_state_q_r = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_valid_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_id_w = 0U;
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_id_w = 0U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_valid_w)) 
               & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
                     >> 1U))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_id_w = 1U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_valid_w)) 
               & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
                     >> 2U))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_id_w = 2U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_valid_w)) 
               & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
                     >> 3U))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_id_w = 3U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_valid_w)) 
               & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
                     >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_id_w = 4U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_valid_w)) 
               & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
                     >> 5U))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_id_w = 5U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_valid_w)) 
               & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
                     >> 6U))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_id_w = 6U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_valid_w)) 
               & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
                     >> 7U))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_id_w = 7U;
    }
    vlSelfRef.milan_datapath__DOT__csr__DOT__sweep_cnt 
        = vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__sweep_cnt;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__v_mrp_valid_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__out_valid_r) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__out_emit_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v2) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v2;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v3) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v4) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v5) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v5;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v6) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v6;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v7) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v7;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v8) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[8U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v8;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v9) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[9U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v9;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v10) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[10U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v10;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v11) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v2) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v2;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v3) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v4) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v5) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v5;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v6) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v6;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v7) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v7;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v8) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[8U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v8;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v9) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[9U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v9;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v10) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[10U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v10;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v11) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[8U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[9U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[10U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[8U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[9U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[10U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_q_r__v0) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_q_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__lb_q_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__lb_q_r__v0;
    }
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
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v4) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v5) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v6) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[3U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__st_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__st_r;
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__slot_r;
    vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 0U;
    if ((0x00008000U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00004000U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00002000U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00001000U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000800U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000400U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act = 0U;
    if ((0x00008000U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[15U];
    }
    if ((0x00004000U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[14U];
    }
    if ((0x00002000U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[13U];
    }
    if ((0x00001000U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[12U];
    }
    if ((0x00000800U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[11U];
    }
    if ((0x00000400U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[10U];
    }
    if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[9U];
    }
    if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[8U];
    }
    if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[7U];
    }
    if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[6U];
    }
    if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[5U];
    }
    if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[4U];
    }
    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[3U];
    }
    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[2U];
    }
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[1U];
    }
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[0U];
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pick_vld_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pick_dep_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pick_if_w = 0U;
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_r) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pick_vld_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pick_dep_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pick_if_w = 0U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pick_vld_w)) 
         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_avail_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pick_vld_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pick_dep_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pick_if_w = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r__v1] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r__v2) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r[0U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__to_cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__to_cnt_r;
    vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__flush_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__flush_r;
    vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__sel_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__sel_r;
    vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__locked_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__locked_r;
    if (vlSelfRef.axis_resetn) {
        if (vlSelfRef.milan_datapath__DOT__link_guard__DOT__tx_trans_w) {
            vlSelfRef.milan_datapath__DOT__link_guard__DOT__tx_armed_r = 1U;
        }
        vlSelfRef.milan_datapath__DOT__tkd_crfq_r = vlSelfRef.milan_datapath__DOT__crft_count_w;
        if (vlSelfRef.milan_datapath__DOT__link_guard__DOT__rx_trans_w) {
            vlSelfRef.milan_datapath__DOT__link_guard__DOT__rx_armed_r = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__alloc_gnt_o) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__cur_slot_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_slot_w;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__alloc_gnt_o) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__cur_slot_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_slot_w;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__alloc_gnt_o) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__cur_slot_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_slot_w;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__alloc_gnt_o) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__cur_slot_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_slot_w;
        }
        if ((0xffU == (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__tick_cnt_r))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__tick_cnt_r = 0U;
            vlSelfRef.milan_datapath__DOT__talker_diag__DOT__tick_p_r = 1U;
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__tick_cnt_r 
                = (0x000000ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__tick_cnt_r)));
            vlSelfRef.milan_datapath__DOT__talker_diag__DOT__tick_p_r = 0U;
        }
        vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r 
            = vlSelfRef.milan_datapath__DOT__tkd_streaming_w;
        vlSelfRef.__Vdly__milan_datapath__DOT__ptp_sync__DOT__snap_ret_s 
            = ((6U & ((IData)(vlSelfRef.milan_datapath__DOT__ptp_sync__DOT__snap_ret_s) 
                      << 1U)) | (IData)(vlSelfRef.milan_datapath__DOT__ptp_sync__DOT__snap_tgl_ts));
        if ((1U & VL_REDXOR_4((6U & (IData)(vlSelfRef.milan_datapath__DOT__ptp_sync__DOT__snap_ret_s))))) {
            vlSelfRef.milan_datapath__DOT__ptp_sync__DOT__tod_rd_valid_reg = 1U;
            vlSelfRef.milan_datapath__DOT__ptp_sync__DOT__tod_rd_reg 
                = vlSelfRef.milan_datapath__DOT__ptp_sync__DOT__snap_val_ts;
        } else {
            vlSelfRef.milan_datapath__DOT__ptp_sync__DOT__tod_rd_valid_reg = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__v_alloc_gnt_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__cur_slot_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ff_slot_w;
        }
        vlSelfRef.milan_datapath__DOT__avtprx_match = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_parse_p = 0U;
        if (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__in_acc) {
            if (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__fire) {
                vlSelfRef.milan_datapath__DOT__avtprx_mr_bit 
                    = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__b1) 
                             >> 3U));
                vlSelfRef.milan_datapath__DOT__avtprx_sid_frame 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__sid;
                vlSelfRef.milan_datapath__DOT__avtprx_match 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__match_hit;
                vlSelfRef.milan_datapath__DOT__avtprx_parse_p = 1U;
                vlSelfRef.milan_datapath__DOT__avtprx_subtype 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__subtype;
                vlSelfRef.milan_datapath__DOT__avtprx_idx = 0U;
            }
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_valid_w = 0U;
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_valid_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_cancel_w 
                = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[1U] 
                         >> 0x0000000eU));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w 
                = (0x0000003fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[1U] 
                                  >> 8U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_owner_w 
                = (0x000000ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[1U]);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_deadline_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[0U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[0U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[2U] 
                    << 0x00000011U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[1U] 
                                       >> 0x0000000fU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[1U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[3U] 
                    << 0x00000011U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[2U] 
                                       >> 0x0000000fU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[2U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[4U] 
                    << 0x00000011U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[3U] 
                                       >> 0x0000000fU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[3U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[5U] 
                    << 0x00000011U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[4U] 
                                       >> 0x0000000fU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[4U] 
                = ((0xffffe000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[4U]) 
                   | (0x00001fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[5U] 
                                     >> 0x0000000fU)));
        }
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_valid_w = 1U;
        }
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_valid_w = 1U;
        }
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_valid_w = 1U;
        }
        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_valid_w = 1U;
        }
        if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_valid_w = 1U;
        }
        if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_valid_w = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
             & (0U == (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[0U] 
                = (IData)((0x00007fffffffffffULL & 
                           (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                             << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U])))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[1U] 
                = ((0xffff8000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[1U]) 
                   | (IData)(((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U])))) 
                              >> 0x00000020U)));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
             & (1U == (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[1U] 
                = ((0x00007fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[1U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U]))))) 
                      << 0x0000000fU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[2U] 
                = ((0xc0000000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[2U]) 
                   | (((IData)((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                    << 0x00000020U) 
                                   | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U]))))) 
                       >> 0x00000011U) | ((IData)((
                                                   (0x00007fffffffffffULL 
                                                    & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                                        << 0x00000020U) 
                                                       | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U])))) 
                                                   >> 0x00000020U)) 
                                          << 0x0000000fU)));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
             & (2U == (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[2U] 
                = ((0x3fffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[2U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U]))))) 
                      << 0x0000001eU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[3U] 
                = (((IData)((0x00007fffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                 << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U]))))) 
                    >> 2U) | ((IData)(((0x00007fffffffffffULL 
                                        & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                            << 0x00000020U) 
                                           | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U])))) 
                                       >> 0x00000020U)) 
                              << 0x0000001eU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[4U] 
                = ((0xffffe000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[4U]) 
                   | ((IData)(((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                    << 0x00000020U) 
                                   | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U])))) 
                               >> 0x00000020U)) >> 2U));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
             & (3U == (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[4U] 
                = ((0x00001fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[4U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U]))))) 
                      << 0x0000000dU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[5U] 
                = ((0xf0000000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[5U]) 
                   | (((IData)((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                    << 0x00000020U) 
                                   | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U]))))) 
                       >> 0x00000013U) | ((IData)((
                                                   (0x00007fffffffffffULL 
                                                    & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                                        << 0x00000020U) 
                                                       | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U])))) 
                                                   >> 0x00000020U)) 
                                          << 0x0000000dU)));
        }
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_cancel_w 
                = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[7U] 
                         >> 0x0000000aU));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w 
                = (0x0000003fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[7U] 
                                  >> 4U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_owner_w 
                = (0x000000ffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[7U] 
                                   << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[6U] 
                                             >> 0x0000001cU)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_deadline_w 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[6U] 
                    << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[5U] 
                              >> 0x0000001cU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[5U] 
                = ((0x0fffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[5U]) 
                   | (0xf0000000U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[7U] 
                                     << 0x00000011U)));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[6U] 
                = (((0x0ffe0000U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[8U] 
                                    << 0x00000011U)) 
                    | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[7U] 
                       >> 0x0000000fU)) | (0xf0000000U 
                                           & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[8U] 
                                              << 0x00000011U)));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[7U] 
                = (((0x0ffe0000U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[9U] 
                                    << 0x00000011U)) 
                    | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[8U] 
                       >> 0x0000000fU)) | (0xf0000000U 
                                           & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[9U] 
                                              << 0x00000011U)));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[8U] 
                = (((0x0ffe0000U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[10U] 
                                    << 0x00000011U)) 
                    | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[9U] 
                       >> 0x0000000fU)) | (0xf0000000U 
                                           & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[10U] 
                                              << 0x00000011U)));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[9U] 
                = (((0x0ffe0000U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[11U] 
                                    << 0x00000011U)) 
                    | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[10U] 
                       >> 0x0000000fU)) | (0xf0000000U 
                                           & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[11U] 
                                              << 0x00000011U)));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[10U] 
                = ((0xfffffe00U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[10U]) 
                   | (0x000001ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[11U] 
                                     >> 0x0000000fU)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 1U) & (0U == (0x00000018U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[5U] 
                = ((0x0fffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[5U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                   << 0x00000011U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                     >> 0x0000000fU)))) 
                      << 0x0000001cU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[6U] 
                = (((IData)((0x00007fffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                 << 0x00000011U) | 
                                ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                 >> 0x0000000fU)))) 
                    >> 4U) | ((IData)(((0x00007fffffffffffULL 
                                        & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                            << 0x00000011U) 
                                           | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                              >> 0x0000000fU))) 
                                       >> 0x00000020U)) 
                              << 0x0000001cU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[7U] 
                = ((0xfffff800U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[7U]) 
                   | ((IData)(((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                    << 0x00000011U) 
                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                      >> 0x0000000fU))) 
                               >> 0x00000020U)) >> 4U));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 1U) & (8U == (0x00000018U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[7U] 
                = ((0x000007ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[7U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                   << 0x00000011U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                     >> 0x0000000fU)))) 
                      << 0x0000000bU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[8U] 
                = ((0xfc000000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[8U]) 
                   | (((IData)((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                    << 0x00000011U) 
                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                      >> 0x0000000fU)))) 
                       >> 0x00000015U) | ((IData)((
                                                   (0x00007fffffffffffULL 
                                                    & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                                        << 0x00000011U) 
                                                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                                          >> 0x0000000fU))) 
                                                   >> 0x00000020U)) 
                                          << 0x0000000bU)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 1U) & (0x00000010U == (0x00000018U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[8U] 
                = ((0x03ffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[8U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                   << 0x00000011U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                     >> 0x0000000fU)))) 
                      << 0x0000001aU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[9U] 
                = (((IData)((0x00007fffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                 << 0x00000011U) | 
                                ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                 >> 0x0000000fU)))) 
                    >> 6U) | ((IData)(((0x00007fffffffffffULL 
                                        & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                            << 0x00000011U) 
                                           | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                              >> 0x0000000fU))) 
                                       >> 0x00000020U)) 
                              << 0x0000001aU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[10U] 
                = ((0xfffffe00U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[10U]) 
                   | ((IData)(((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                    << 0x00000011U) 
                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                      >> 0x0000000fU))) 
                               >> 0x00000020U)) >> 6U));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 1U) & (0x00000018U == (0x00000018U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[10U] 
                = ((0x000001ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[10U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                   << 0x00000011U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                     >> 0x0000000fU)))) 
                      << 9U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[11U] 
                = ((0xff000000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[11U]) 
                   | (((IData)((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                    << 0x00000011U) 
                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                      >> 0x0000000fU)))) 
                       >> 0x00000017U) | ((IData)((
                                                   (0x00007fffffffffffULL 
                                                    & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                                        << 0x00000011U) 
                                                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                                          >> 0x0000000fU))) 
                                                   >> 0x00000020U)) 
                                          << 9U)));
        }
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_cancel_w 
                = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[13U] 
                         >> 6U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w 
                = (0x0000003fU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[13U]);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_owner_w 
                = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[12U] 
                   >> 0x00000018U);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_deadline_w 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[12U] 
                    << 8U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[11U] 
                              >> 0x00000018U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[11U] 
                = ((0x00ffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[11U]) 
                   | (0xff000000U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[13U] 
                                     << 0x00000011U)));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[12U] 
                = (((0x00fe0000U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[14U] 
                                    << 0x00000011U)) 
                    | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[13U] 
                       >> 0x0000000fU)) | (0xff000000U 
                                           & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[14U] 
                                              << 0x00000011U)));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[13U] 
                = (((0x00fe0000U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[15U] 
                                    << 0x00000011U)) 
                    | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[14U] 
                       >> 0x0000000fU)) | (0xff000000U 
                                           & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[15U] 
                                              << 0x00000011U)));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[14U] 
                = (((0x00fe0000U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[16U] 
                                    << 0x00000011U)) 
                    | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[15U] 
                       >> 0x0000000fU)) | (0xff000000U 
                                           & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[16U] 
                                              << 0x00000011U)));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[15U] 
                = (((0x00fe0000U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[17U] 
                                    << 0x00000011U)) 
                    | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[16U] 
                       >> 0x0000000fU)) | (0xff000000U 
                                           & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[17U] 
                                              << 0x00000011U)));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[16U] 
                = ((0xffffffe0U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[16U]) 
                   | (0x0000001fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[17U] 
                                     >> 0x0000000fU)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 2U) & (0U == (0x000000c0U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[11U] 
                = ((0x00ffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[11U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                   << 0x00000022U) 
                                  | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U])) 
                                      << 2U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                                >> 0x0000001eU))))) 
                      << 0x00000018U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[12U] 
                = (((IData)((0x00007fffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                 << 0x00000022U) | 
                                (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U])) 
                                  << 2U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                            >> 0x0000001eU))))) 
                    >> 8U) | ((IData)(((0x00007fffffffffffULL 
                                        & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                            << 0x00000022U) 
                                           | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U])) 
                                               << 2U) 
                                              | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                                 >> 0x0000001eU)))) 
                                       >> 0x00000020U)) 
                              << 0x00000018U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[13U] 
                = ((0xffffff80U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[13U]) 
                   | ((IData)(((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                    << 0x00000022U) 
                                   | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U])) 
                                       << 2U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                                 >> 0x0000001eU)))) 
                               >> 0x00000020U)) >> 8U));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 2U) & (0x00000040U == (0x000000c0U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[13U] 
                = ((0x0000007fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[13U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                   << 0x00000022U) 
                                  | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U])) 
                                      << 2U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                                >> 0x0000001eU))))) 
                      << 7U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[14U] 
                = ((0xffc00000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[14U]) 
                   | (((IData)((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                    << 0x00000022U) 
                                   | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U])) 
                                       << 2U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                                 >> 0x0000001eU))))) 
                       >> 0x00000019U) | ((IData)((
                                                   (0x00007fffffffffffULL 
                                                    & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                                        << 0x00000022U) 
                                                       | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U])) 
                                                           << 2U) 
                                                          | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                                             >> 0x0000001eU)))) 
                                                   >> 0x00000020U)) 
                                          << 7U)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 2U) & (0x00000080U == (0x000000c0U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[14U] 
                = ((0x003fffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[14U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                   << 0x00000022U) 
                                  | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U])) 
                                      << 2U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                                >> 0x0000001eU))))) 
                      << 0x00000016U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[15U] 
                = (((IData)((0x00007fffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                 << 0x00000022U) | 
                                (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U])) 
                                  << 2U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                            >> 0x0000001eU))))) 
                    >> 0x0000000aU) | ((IData)(((0x00007fffffffffffULL 
                                                 & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                                     << 0x00000022U) 
                                                    | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U])) 
                                                        << 2U) 
                                                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                                          >> 0x0000001eU)))) 
                                                >> 0x00000020U)) 
                                       << 0x00000016U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[16U] 
                = ((0xffffffe0U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[16U]) 
                   | ((IData)(((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                    << 0x00000022U) 
                                   | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U])) 
                                       << 2U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                                 >> 0x0000001eU)))) 
                               >> 0x00000020U)) >> 0x0000000aU));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 2U) & (0x000000c0U == (0x000000c0U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[16U] 
                = ((0x0000001fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[16U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                   << 0x00000022U) 
                                  | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U])) 
                                      << 2U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                                >> 0x0000001eU))))) 
                      << 5U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[17U] 
                = ((0xfff00000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[17U]) 
                   | (((IData)((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                    << 0x00000022U) 
                                   | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U])) 
                                       << 2U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                                 >> 0x0000001eU))))) 
                       >> 0x0000001bU) | ((IData)((
                                                   (0x00007fffffffffffULL 
                                                    & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                                        << 0x00000022U) 
                                                       | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U])) 
                                                           << 2U) 
                                                          | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                                             >> 0x0000001eU)))) 
                                                   >> 0x00000020U)) 
                                          << 5U)));
        }
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_cancel_w 
                = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[19U] 
                         >> 2U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w 
                = (0x0000003fU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[19U] 
                                   << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[18U] 
                                             >> 0x0000001cU)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_owner_w 
                = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[18U] 
                                  >> 0x00000014U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_deadline_w 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[18U] 
                    << 0x0000000cU) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[17U] 
                                       >> 0x00000014U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[17U] 
                = ((0x000fffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[17U]) 
                   | (0xfff00000U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[19U] 
                                     << 0x00000011U)));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[18U] 
                = (((0x000e0000U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[20U] 
                                    << 0x00000011U)) 
                    | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[19U] 
                       >> 0x0000000fU)) | (0xfff00000U 
                                           & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[20U] 
                                              << 0x00000011U)));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[19U] 
                = (((0x000e0000U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[21U] 
                                    << 0x00000011U)) 
                    | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[20U] 
                       >> 0x0000000fU)) | (0xfff00000U 
                                           & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[21U] 
                                              << 0x00000011U)));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[20U] 
                = (((0x000e0000U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[22U] 
                                    << 0x00000011U)) 
                    | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[21U] 
                       >> 0x0000000fU)) | (0xfff00000U 
                                           & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[22U] 
                                              << 0x00000011U)));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[21U] 
                = (((0x000e0000U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[23U] 
                                    << 0x00000011U)) 
                    | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[22U] 
                       >> 0x0000000fU)) | (0xfff00000U 
                                           & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[23U] 
                                              << 0x00000011U)));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[22U] 
                = ((0xfffffffeU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[22U]) 
                   | (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[23U] 
                            >> 0x0000000fU)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 3U) & (0U == (0x00000600U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[17U] 
                = ((0x000fffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[17U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                   << 0x00000013U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                     >> 0x0000000dU)))) 
                      << 0x00000014U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[18U] 
                = (((IData)((0x00007fffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                 << 0x00000013U) | 
                                ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                 >> 0x0000000dU)))) 
                    >> 0x0000000cU) | ((IData)(((0x00007fffffffffffULL 
                                                 & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                                     << 0x00000013U) 
                                                    | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                                       >> 0x0000000dU))) 
                                                >> 0x00000020U)) 
                                       << 0x00000014U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[19U] 
                = ((0xfffffff8U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[19U]) 
                   | ((IData)(((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                    << 0x00000013U) 
                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                      >> 0x0000000dU))) 
                               >> 0x00000020U)) >> 0x0000000cU));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 3U) & (0x00000200U == (0x00000600U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[19U] 
                = ((7U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[19U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                   << 0x00000013U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                     >> 0x0000000dU)))) 
                      << 3U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[20U] 
                = ((0xfffc0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[20U]) 
                   | (((IData)((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                    << 0x00000013U) 
                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                      >> 0x0000000dU)))) 
                       >> 0x0000001dU) | ((IData)((
                                                   (0x00007fffffffffffULL 
                                                    & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                                        << 0x00000013U) 
                                                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                                          >> 0x0000000dU))) 
                                                   >> 0x00000020U)) 
                                          << 3U)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 3U) & (0x00000400U == (0x00000600U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[20U] 
                = ((0x0003ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[20U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                   << 0x00000013U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                     >> 0x0000000dU)))) 
                      << 0x00000012U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[21U] 
                = (((IData)((0x00007fffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                 << 0x00000013U) | 
                                ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                 >> 0x0000000dU)))) 
                    >> 0x0000000eU) | ((IData)(((0x00007fffffffffffULL 
                                                 & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                                     << 0x00000013U) 
                                                    | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                                       >> 0x0000000dU))) 
                                                >> 0x00000020U)) 
                                       << 0x00000012U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[22U] 
                = ((0xfffffffeU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[22U]) 
                   | ((IData)(((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                    << 0x00000013U) 
                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                      >> 0x0000000dU))) 
                               >> 0x00000020U)) >> 0x0000000eU));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 3U) & (0x00000600U == (0x00000600U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[22U] 
                = ((1U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[22U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                   << 0x00000013U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                     >> 0x0000000dU)))) 
                      << 1U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[23U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[23U]) 
                   | (((IData)((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                    << 0x00000013U) 
                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                      >> 0x0000000dU)))) 
                       >> 0x0000001fU) | ((IData)((
                                                   (0x00007fffffffffffULL 
                                                    & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                                        << 0x00000013U) 
                                                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                                          >> 0x0000000dU))) 
                                                   >> 0x00000020U)) 
                                          << 1U)));
        }
        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_cancel_w 
                = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[24U] 
                         >> 0x0000001eU));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w 
                = (0x0000003fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[24U] 
                                  >> 0x00000018U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_owner_w 
                = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[24U] 
                                  >> 0x00000010U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_deadline_w 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[24U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[23U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[23U] 
                = ((0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[23U]) 
                   | ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[25U] 
                       << 0x00000011U) | (0x00010000U 
                                          & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[24U] 
                                             >> 0x0000000fU))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[24U] 
                = ((0x0000ffffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[25U] 
                                   >> 0x0000000fU)) 
                   | ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[26U] 
                       << 0x00000011U) | (0x00010000U 
                                          & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[25U] 
                                             >> 0x0000000fU))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[25U] 
                = ((0x0000ffffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[26U] 
                                   >> 0x0000000fU)) 
                   | ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[27U] 
                       << 0x00000011U) | (0x00010000U 
                                          & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[26U] 
                                             >> 0x0000000fU))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[26U] 
                = ((0x0000ffffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[27U] 
                                   >> 0x0000000fU)) 
                   | ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[28U] 
                       << 0x00000011U) | (0x00010000U 
                                          & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[27U] 
                                             >> 0x0000000fU))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[27U] 
                = ((0xe0000000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[27U]) 
                   | ((0x0000ffffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[28U] 
                                      >> 0x0000000fU)) 
                      | (0x1fff0000U & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[29U] 
                                         << 0x00000011U) 
                                        | (0x00010000U 
                                           & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[28U] 
                                              >> 0x0000000fU))))));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 4U) & (0U == (0x00003000U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[23U] 
                = ((0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[23U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                   << 0x00000024U) 
                                  | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U])) 
                                      << 4U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                                >> 0x0000001cU))))) 
                      << 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[24U] 
                = ((0x80000000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[24U]) 
                   | (((IData)((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                    << 0x00000024U) 
                                   | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U])) 
                                       << 4U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                                 >> 0x0000001cU))))) 
                       >> 0x00000010U) | ((IData)((
                                                   (0x00007fffffffffffULL 
                                                    & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                                        << 0x00000024U) 
                                                       | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U])) 
                                                           << 4U) 
                                                          | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                                             >> 0x0000001cU)))) 
                                                   >> 0x00000020U)) 
                                          << 0x00000010U)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 4U) & (0x00001000U == (0x00003000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[24U] 
                = ((0x7fffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[24U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                   << 0x00000024U) 
                                  | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U])) 
                                      << 4U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                                >> 0x0000001cU))))) 
                      << 0x0000001fU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[25U] 
                = (((IData)((0x00007fffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                 << 0x00000024U) | 
                                (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U])) 
                                  << 4U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                            >> 0x0000001cU))))) 
                    >> 1U) | ((IData)(((0x00007fffffffffffULL 
                                        & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                            << 0x00000024U) 
                                           | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U])) 
                                               << 4U) 
                                              | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                                 >> 0x0000001cU)))) 
                                       >> 0x00000020U)) 
                              << 0x0000001fU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[26U] 
                = ((0xffffc000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[26U]) 
                   | ((IData)(((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                    << 0x00000024U) 
                                   | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U])) 
                                       << 4U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                                 >> 0x0000001cU)))) 
                               >> 0x00000020U)) >> 1U));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 4U) & (0x00002000U == (0x00003000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[26U] 
                = ((0x00003fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[26U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                   << 0x00000024U) 
                                  | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U])) 
                                      << 4U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                                >> 0x0000001cU))))) 
                      << 0x0000000eU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[27U] 
                = ((0xe0000000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[27U]) 
                   | (((IData)((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                    << 0x00000024U) 
                                   | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U])) 
                                       << 4U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                                 >> 0x0000001cU))))) 
                       >> 0x00000012U) | ((IData)((
                                                   (0x00007fffffffffffULL 
                                                    & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                                        << 0x00000024U) 
                                                       | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U])) 
                                                           << 4U) 
                                                          | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                                             >> 0x0000001cU)))) 
                                                   >> 0x00000020U)) 
                                          << 0x0000000eU)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 4U) & (0x00003000U == (0x00003000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[27U] 
                = ((0x1fffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[27U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                   << 0x00000024U) 
                                  | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U])) 
                                      << 4U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                                >> 0x0000001cU))))) 
                      << 0x0000001dU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[28U] 
                = (((IData)((0x00007fffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                 << 0x00000024U) | 
                                (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U])) 
                                  << 4U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                            >> 0x0000001cU))))) 
                    >> 3U) | ((IData)(((0x00007fffffffffffULL 
                                        & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                            << 0x00000024U) 
                                           | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U])) 
                                               << 4U) 
                                              | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                                 >> 0x0000001cU)))) 
                                       >> 0x00000020U)) 
                              << 0x0000001dU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[29U] 
                = ((0xfffff000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[29U]) 
                   | ((IData)(((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                    << 0x00000024U) 
                                   | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U])) 
                                       << 4U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                                 >> 0x0000001cU)))) 
                               >> 0x00000020U)) >> 3U));
        }
        if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_cancel_w 
                = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[30U] 
                         >> 0x0000001aU));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w 
                = (0x0000003fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[30U] 
                                  >> 0x00000014U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_owner_w 
                = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[30U] 
                                  >> 0x0000000cU));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_deadline_w 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[30U] 
                    << 0x00000014U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[29U] 
                                       >> 0x0000000cU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[29U] 
                = ((0x00000fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[29U]) 
                   | ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[31U] 
                       << 0x00000011U) | (0x0001f000U 
                                          & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[30U] 
                                             >> 0x0000000fU))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[30U] 
                = ((0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[31U] 
                                   >> 0x0000000fU)) 
                   | ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[32U] 
                       << 0x00000011U) | (0x0001f000U 
                                          & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[31U] 
                                             >> 0x0000000fU))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[31U] 
                = ((0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[32U] 
                                   >> 0x0000000fU)) 
                   | ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[33U] 
                       << 0x00000011U) | (0x0001f000U 
                                          & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[32U] 
                                             >> 0x0000000fU))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[32U] 
                = ((0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[33U] 
                                   >> 0x0000000fU)) 
                   | ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[34U] 
                       << 0x00000011U) | (0x0001f000U 
                                          & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[33U] 
                                             >> 0x0000000fU))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[33U] 
                = ((0xfe000000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[33U]) 
                   | ((0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[34U] 
                                      >> 0x0000000fU)) 
                      | (0x01fff000U & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[35U] 
                                         << 0x00000011U) 
                                        | (0x0001f000U 
                                           & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[34U] 
                                              >> 0x0000000fU))))));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 5U) & (0U == (0x00018000U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[29U] 
                = ((0x00000fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[29U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                   << 0x00000015U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                     >> 0x0000000bU)))) 
                      << 0x0000000cU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[30U] 
                = ((0xf8000000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[30U]) 
                   | (((IData)((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                    << 0x00000015U) 
                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                      >> 0x0000000bU)))) 
                       >> 0x00000014U) | ((IData)((
                                                   (0x00007fffffffffffULL 
                                                    & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                                        << 0x00000015U) 
                                                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                                          >> 0x0000000bU))) 
                                                   >> 0x00000020U)) 
                                          << 0x0000000cU)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 5U) & (0x00008000U == (0x00018000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[30U] 
                = ((0x07ffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[30U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                   << 0x00000015U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                     >> 0x0000000bU)))) 
                      << 0x0000001bU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[31U] 
                = (((IData)((0x00007fffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                 << 0x00000015U) | 
                                ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                 >> 0x0000000bU)))) 
                    >> 5U) | ((IData)(((0x00007fffffffffffULL 
                                        & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                            << 0x00000015U) 
                                           | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                              >> 0x0000000bU))) 
                                       >> 0x00000020U)) 
                              << 0x0000001bU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[32U] 
                = ((0xfffffc00U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[32U]) 
                   | ((IData)(((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                    << 0x00000015U) 
                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                      >> 0x0000000bU))) 
                               >> 0x00000020U)) >> 5U));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 5U) & (0x00010000U == (0x00018000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[32U] 
                = ((0x000003ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[32U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                   << 0x00000015U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                     >> 0x0000000bU)))) 
                      << 0x0000000aU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[33U] 
                = ((0xfe000000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[33U]) 
                   | (((IData)((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                    << 0x00000015U) 
                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                      >> 0x0000000bU)))) 
                       >> 0x00000016U) | ((IData)((
                                                   (0x00007fffffffffffULL 
                                                    & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                                        << 0x00000015U) 
                                                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                                          >> 0x0000000bU))) 
                                                   >> 0x00000020U)) 
                                          << 0x0000000aU)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 5U) & (0x00018000U == (0x00018000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[33U] 
                = ((0x01ffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[33U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                   << 0x00000015U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                     >> 0x0000000bU)))) 
                      << 0x00000019U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[34U] 
                = (((IData)((0x00007fffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                 << 0x00000015U) | 
                                ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                 >> 0x0000000bU)))) 
                    >> 7U) | ((IData)(((0x00007fffffffffffULL 
                                        & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                            << 0x00000015U) 
                                           | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                              >> 0x0000000bU))) 
                                       >> 0x00000020U)) 
                              << 0x00000019U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[35U] 
                = ((0xffffff00U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[35U]) 
                   | ((IData)(((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                    << 0x00000015U) 
                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                      >> 0x0000000bU))) 
                               >> 0x00000020U)) >> 7U));
        }
        if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_cancel_w 
                = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[36U] 
                         >> 0x00000016U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w 
                = (0x0000003fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[36U] 
                                  >> 0x00000010U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_owner_w 
                = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[36U] 
                                  >> 8U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_deadline_w 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[36U] 
                    << 0x00000018U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[35U] 
                                       >> 8U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[35U] 
                = ((0x000000ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[35U]) 
                   | ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[37U] 
                       << 0x00000011U) | (0x0001ff00U 
                                          & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[36U] 
                                             >> 0x0000000fU))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[36U] 
                = ((0x000000ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[37U] 
                                   >> 0x0000000fU)) 
                   | ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[38U] 
                       << 0x00000011U) | (0x0001ff00U 
                                          & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[37U] 
                                             >> 0x0000000fU))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[37U] 
                = ((0x000000ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[38U] 
                                   >> 0x0000000fU)) 
                   | ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[39U] 
                       << 0x00000011U) | (0x0001ff00U 
                                          & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[38U] 
                                             >> 0x0000000fU))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[38U] 
                = ((0x000000ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[39U] 
                                   >> 0x0000000fU)) 
                   | ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[40U] 
                       << 0x00000011U) | (0x0001ff00U 
                                          & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[39U] 
                                             >> 0x0000000fU))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[39U] 
                = ((0xffe00000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[39U]) 
                   | ((0x000000ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[40U] 
                                      >> 0x0000000fU)) 
                      | (0x001fff00U & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[41U] 
                                         << 0x00000011U) 
                                        | (0x0001ff00U 
                                           & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[40U] 
                                              >> 0x0000000fU))))));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 6U) & (0U == (0x000c0000U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[35U] 
                = ((0x000000ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[35U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                   << 0x00000026U) 
                                  | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U])) 
                                      << 6U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                                >> 0x0000001aU))))) 
                      << 8U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[36U] 
                = ((0xff800000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[36U]) 
                   | (((IData)((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                    << 0x00000026U) 
                                   | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U])) 
                                       << 6U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                                 >> 0x0000001aU))))) 
                       >> 0x00000018U) | ((IData)((
                                                   (0x00007fffffffffffULL 
                                                    & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                                        << 0x00000026U) 
                                                       | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U])) 
                                                           << 6U) 
                                                          | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                                             >> 0x0000001aU)))) 
                                                   >> 0x00000020U)) 
                                          << 8U)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 6U) & (0x00040000U == (0x000c0000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[36U] 
                = ((0x007fffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[36U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                   << 0x00000026U) 
                                  | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U])) 
                                      << 6U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                                >> 0x0000001aU))))) 
                      << 0x00000017U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[37U] 
                = (((IData)((0x00007fffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                 << 0x00000026U) | 
                                (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U])) 
                                  << 6U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                            >> 0x0000001aU))))) 
                    >> 9U) | ((IData)(((0x00007fffffffffffULL 
                                        & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                            << 0x00000026U) 
                                           | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U])) 
                                               << 6U) 
                                              | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                                 >> 0x0000001aU)))) 
                                       >> 0x00000020U)) 
                              << 0x00000017U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[38U] 
                = ((0xffffffc0U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[38U]) 
                   | ((IData)(((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                    << 0x00000026U) 
                                   | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U])) 
                                       << 6U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                                 >> 0x0000001aU)))) 
                               >> 0x00000020U)) >> 9U));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 6U) & (0x00080000U == (0x000c0000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[38U] 
                = ((0x0000003fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[38U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                   << 0x00000026U) 
                                  | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U])) 
                                      << 6U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                                >> 0x0000001aU))))) 
                      << 6U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[39U] 
                = ((0xffe00000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[39U]) 
                   | (((IData)((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                    << 0x00000026U) 
                                   | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U])) 
                                       << 6U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                                 >> 0x0000001aU))))) 
                       >> 0x0000001aU) | ((IData)((
                                                   (0x00007fffffffffffULL 
                                                    & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                                        << 0x00000026U) 
                                                       | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U])) 
                                                           << 6U) 
                                                          | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                                             >> 0x0000001aU)))) 
                                                   >> 0x00000020U)) 
                                          << 6U)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 6U) & (0x000c0000U == (0x000c0000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[39U] 
                = ((0x001fffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[39U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                   << 0x00000026U) 
                                  | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U])) 
                                      << 6U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                                >> 0x0000001aU))))) 
                      << 0x00000015U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[40U] 
                = (((IData)((0x00007fffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                 << 0x00000026U) | 
                                (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U])) 
                                  << 6U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                            >> 0x0000001aU))))) 
                    >> 0x0000000bU) | ((IData)(((0x00007fffffffffffULL 
                                                 & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                                     << 0x00000026U) 
                                                    | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U])) 
                                                        << 6U) 
                                                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                                          >> 0x0000001aU)))) 
                                                >> 0x00000020U)) 
                                       << 0x00000015U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[41U] 
                = ((0xfffffff0U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[41U]) 
                   | ((IData)(((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                    << 0x00000026U) 
                                   | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U])) 
                                       << 6U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                                 >> 0x0000001aU)))) 
                               >> 0x00000020U)) >> 0x0000000bU));
        }
        if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_valid_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_cancel_w 
                = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[42U] 
                         >> 0x00000012U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w 
                = (0x0000003fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[42U] 
                                  >> 0x0000000cU));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_owner_w 
                = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[42U] 
                                  >> 4U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_deadline_w 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[42U] 
                    << 0x0000001cU) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[41U] 
                                       >> 4U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[41U] 
                = ((0x0000000fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[41U]) 
                   | ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[43U] 
                       << 0x00000011U) | (0x0001fff0U 
                                          & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[42U] 
                                             >> 0x0000000fU))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[42U] 
                = ((0x0000000fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[43U] 
                                   >> 0x0000000fU)) 
                   | ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[44U] 
                       << 0x00000011U) | (0x0001fff0U 
                                          & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[43U] 
                                             >> 0x0000000fU))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[43U] 
                = ((0x0000000fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[44U] 
                                   >> 0x0000000fU)) 
                   | ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[45U] 
                       << 0x00000011U) | (0x0001fff0U 
                                          & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[44U] 
                                             >> 0x0000000fU))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[44U] 
                = ((0x0000000fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[45U] 
                                   >> 0x0000000fU)) 
                   | ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[46U] 
                       << 0x00000011U) | (0x0001fff0U 
                                          & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[45U] 
                                             >> 0x0000000fU))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[45U] 
                = ((0xfffe0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[45U]) 
                   | ((0x0000000fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[46U] 
                                      >> 0x0000000fU)) 
                      | (0x0001fff0U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[46U] 
                                        >> 0x0000000fU))));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 7U) & (0U == (0x00600000U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[41U] 
                = ((0x0000000fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[41U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                                   << 0x00000017U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                     >> 9U)))) << 4U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[42U] 
                = ((0xfff80000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[42U]) 
                   | (((IData)((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                                    << 0x00000017U) 
                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                      >> 9U)))) >> 0x0000001cU) 
                      | ((IData)(((0x00007fffffffffffULL 
                                   & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                                       << 0x00000017U) 
                                      | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                         >> 9U))) >> 0x00000020U)) 
                         << 4U)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 7U) & (0x00200000U == (0x00600000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[42U] 
                = ((0x0007ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[42U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                                   << 0x00000017U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                     >> 9U)))) << 0x00000013U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[43U] 
                = (((IData)((0x00007fffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                                 << 0x00000017U) | 
                                ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                 >> 9U)))) >> 0x0000000dU) 
                   | ((IData)(((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                                    << 0x00000017U) 
                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                      >> 9U))) >> 0x00000020U)) 
                      << 0x00000013U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[44U] 
                = ((0xfffffffcU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[44U]) 
                   | ((IData)(((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                                    << 0x00000017U) 
                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                      >> 9U))) >> 0x00000020U)) 
                      >> 0x0000000dU));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 7U) & (0x00400000U == (0x00600000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[44U] 
                = ((3U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[44U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                                   << 0x00000017U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                     >> 9U)))) << 2U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[45U] 
                = ((0xfffe0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[45U]) 
                   | (((IData)((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                                    << 0x00000017U) 
                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                      >> 9U)))) >> 0x0000001eU) 
                      | ((IData)(((0x00007fffffffffffULL 
                                   & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                                       << 0x00000017U) 
                                      | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                         >> 9U))) >> 0x00000020U)) 
                         << 2U)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 7U) & (0x00600000U == (0x00600000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[45U] 
                = ((0x0001ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[45U]) 
                   | ((IData)((0x00007fffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                                   << 0x00000017U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                     >> 9U)))) << 0x00000011U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[46U] 
                = (((IData)((0x00007fffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                                 << 0x00000017U) | 
                                ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                 >> 9U)))) >> 0x0000000fU) 
                   | ((IData)(((0x00007fffffffffffULL 
                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                                    << 0x00000017U) 
                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                      >> 9U))) >> 0x00000020U)) 
                      << 0x00000011U));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__noadp_exp_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r 
                = ((~ ((IData)(1U) << (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                             - (IData)(1U))))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r));
        }
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r 
                = (2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r));
        }
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r 
                = (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__st_set_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r) 
                   | (3U & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r))));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__st_clr_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_ren_r) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_rempty_w)))) {
            vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_pair_w 
                = vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r
                [(7U & (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_bin_r))];
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__take_wr_w) {
            if ((7U != (0x00001fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                       >> 3U)))) {
                vlSelfRef.milan_datapath__DOT__pp_aecp_dyn_dirty_w = 1U;
            }
        }
        if (((((0x0fU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_done_w)) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_taint_r))) 
             | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_giveup_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__dirty_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sink_r))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__dirty_r));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_wr_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__dirty_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__dirty_r) 
                   | (3U & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r))));
        }
        vlSelfRef.milan_datapath__DOT__src_recentre_q_r 
            = vlSelfRef.milan_datapath__DOT__media_clk_src_r;
        if (vlSelfRef.milan_datapath__DOT__crf_clk_selected_r) {
            if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__engaged_r)) 
                       | (0x208cU <= (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__quiet_r))))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__media_grid_align__DOT__quiet_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_frame_ev_w)
                        ? 0U : (0x00003fffU & ((0x208cU 
                                                <= (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__quiet_r))
                                                ? (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__quiet_r)
                                                : ((IData)(1U) 
                                                   + (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__quiet_r)))));
                if (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_frame_ev_w) {
                    vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__ref_r 
                        = vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__tst_next_w;
                }
                vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__tst_r 
                    = vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__tst_next_w;
                vlSelfRef.__Vdly__milan_datapath__DOT__media_grid_align__DOT__slip_r = 0U;
                vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__engaged_r 
                    = vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_frame_ev_w;
                vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__err_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__media_grid_align__DOT__acc_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__mnco_servo_trim_w = 0U;
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__media_grid_align__DOT__quiet_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_frame_ev_w)
                        ? 0U : (0x00003fffU & ((IData)(1U) 
                                               + (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__quiet_r))));
                if (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_frame_ev_w) {
                    if (vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__fold_dn_w) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__media_grid_align__DOT__slip_r 
                            = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__slip_r) 
                                              - (IData)(1U)));
                    } else if (vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__fold_up_w) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__media_grid_align__DOT__slip_r 
                            = (0x0000001fU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__slip_r)));
                    }
                    if ((1U & (~ (((0xf380U == (IData)(vlSelfRef.milan_datapath__DOT__mnco_servo_trim_w)) 
                                   & VL_LTS_III(32, 0U, vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__err_w)) 
                                  | ((0x0c80U == (IData)(vlSelfRef.milan_datapath__DOT__mnco_servo_trim_w)) 
                                     & VL_GTS_III(32, 0U, vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__err_w)))))) {
                        __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_acc__257__v 
                            = (vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__acc_r 
                               + vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__err_w);
                        __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_acc__257__Vfuncout 
                            = (VL_LTS_III(32, 0x00c80000U, __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_acc__257__v)
                                ? 0x00c80000U : (VL_GTS_III(32, 0xff380000U, __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_acc__257__v)
                                                  ? 0xff380000U
                                                  : __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_acc__257__v));
                        vlSelfRef.__Vdly__milan_datapath__DOT__media_grid_align__DOT__acc_r 
                            = __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_acc__257__Vfuncout;
                    }
                    __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_u__258__v 
                        = (VL_MULS_III(32, (IData)(0xffffffffU), 
                                       (vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__err_w 
                                        << 2U)) - VL_SHIFTRS_III(32,32,32, vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__acc_r, 0x0000000cU));
                    vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__err_r 
                        = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__err_w);
                    __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_u__258__Vfuncout 
                        = (VL_LTS_III(32, 0x00000c80U, __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_u__258__v)
                            ? 0x00000c80U : (VL_GTS_III(32, 0xfffff380U, __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_u__258__v)
                                              ? 0x0000f380U
                                              : (0x0000ffffU 
                                                 & __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_u__258__v)));
                    vlSelfRef.__Vdly__milan_datapath__DOT__mnco_servo_trim_w 
                        = __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_u__258__Vfuncout;
                }
                vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__tst_r 
                    = vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__tst_next_w;
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__media_grid_align__DOT__quiet_r = 0U;
            vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__tst_r 
                = vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__tst_next_w;
            vlSelfRef.__Vdly__milan_datapath__DOT__media_grid_align__DOT__slip_r = 0U;
            vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__engaged_r = 0U;
            vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__err_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__media_grid_align__DOT__acc_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__mnco_servo_trim_w = 0U;
        }
        vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__rollover_r = 0U;
        if ((((IData)(vlSelfRef.milan_datapath__DOT__mac_events_w) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__stats_rst_p))) 
             & (0xffffffffU == vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__counters[0U]))) {
            vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__rollover_r = 1U;
        }
        if (((((IData)(vlSelfRef.milan_datapath__DOT__mac_events_w) 
               >> 1U) & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__stats_rst_p))) 
             & (0xffffffffU == vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__counters[1U]))) {
            vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__rollover_r = 1U;
        }
        if (((((IData)(vlSelfRef.milan_datapath__DOT__mac_events_w) 
               >> 2U) & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__stats_rst_p))) 
             & (0xffffffffU == vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__counters[2U]))) {
            vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__rollover_r = 1U;
        }
        if (((((IData)(vlSelfRef.milan_datapath__DOT__mac_events_w) 
               >> 3U) & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__stats_rst_p))) 
             & (0xffffffffU == vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__counters[3U]))) {
            vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__rollover_r = 1U;
        }
        if (((((IData)(vlSelfRef.milan_datapath__DOT__mac_events_w) 
               >> 4U) & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__stats_rst_p))) 
             & (0xffffffffU == vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__counters[4U]))) {
            vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__rollover_r = 1U;
        }
        if (((((IData)(vlSelfRef.milan_datapath__DOT__mac_events_w) 
               >> 5U) & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__stats_rst_p))) 
             & (0xffffffffU == vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__counters[5U]))) {
            vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__rollover_r = 1U;
        }
        if (((((IData)(vlSelfRef.milan_datapath__DOT__mac_events_w) 
               >> 6U) & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__stats_rst_p))) 
             & (0xffffffffU == vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__counters[6U]))) {
            vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__rollover_r = 1U;
        }
        if (((((IData)(vlSelfRef.milan_datapath__DOT__mac_events_w) 
               >> 7U) & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__stats_rst_p))) 
             & (0xffffffffU == vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__counters[7U]))) {
            vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__rollover_r = 1U;
        }
        if (((((IData)(vlSelfRef.milan_datapath__DOT__mac_events_w) 
               >> 8U) & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__stats_rst_p))) 
             & (0xffffffffU == vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__counters[8U]))) {
            vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__rollover_r = 1U;
        }
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_txp_q_r 
            = ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__ltap_txmac_w) 
                 << 3U) | (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__aaf_tx_acc_w) 
                            & (IData)(vlSelfRef.milan_datapath__DOT__aaf_tx_tlast)) 
                           << 2U)) | ((((~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__aaf_tx_inframe_r)) 
                                        & (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__aaf_tx_acc_w)) 
                                       << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__aafcap_pv_w)));
        vlSelfRef.milan_datapath__DOT__csr__DOT__ltap_clr_p = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_rxp_q_r 
            = (((((IData)(vlSelfRef.milan_datapath__DOT__rend_pcm_tvalid_w) 
                  & (IData)(vlSelfRef.milan_datapath__DOT__dpkt_pcm_tlast_w)) 
                 << 3U) | (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w) 
                            & (IData)(vlSelfRef.milan_datapath__DOT__dpkt_pcm_tlast_w)) 
                           << 2U)) | (((IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_p) 
                                       << 1U) | ((~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__mac_rx_inframe_r)) 
                                                 & (IData)(vlSelfRef.s_axis_mac_rx_tvalid))));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_la_mvrp_r = 0U;
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r) {
                if ((0x17U >= (0x0000001fU & ((IData)(0x0000000cU) 
                                              * (1U 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r 
                        = (((~ ((IData)(0x00000fffU) 
                                << (0x0000001fU & ((IData)(0x0000000cU) 
                                                   * 
                                                   (1U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) 
                            & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r) 
                           | (0x00ffffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_vid_r) 
                                             << (0x0000001fU 
                                                 & ((IData)(0x0000000cU) 
                                                    * 
                                                    (1U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))));
                }
            }
        }
        vlSelfRef.milan_datapath__DOT__cmap_rd_valid_w = 0U;
        if (vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_capture__map_rd_en_i) {
            vlSelfRef.milan_datapath__DOT__cmap_rd_valid_w = 1U;
            vlSelfRef.milan_datapath__DOT__cmap_rd_data_w 
                = (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_fed_r) 
                    << 0x0000000eU) | (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w) 
                                        << 0x0000000dU) 
                                       | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                       [(7U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r))]));
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_q2_r 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_q1_r;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__iv_bytes_r 
            = (0x00000001ffffffffULL & ((QData)((IData)(
                                                        (0x0000ffffU 
                                                         & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_mif_r 
                                                            >> 
                                                            (0x0000001fU 
                                                             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_q1_r) 
                                                                << 4U)))))) 
                                        * (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__frame_bytes_r))));
        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r 
            = (0x0000ffffU & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_next_w));
        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_done_p = 0U;
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__beat_w) {
            vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r 
                = ((7U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r))
                    ? 7U : (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r))));
            if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r))) {
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__182__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__185__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_1__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__182__w 
                                              >> 0x20U)));
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_4__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__185__w 
                                              >> 0x38U)));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__183__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_msg_r 
                    = (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_4__lane));
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_2__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__183__w 
                                              >> 0x28U)));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__184__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_3__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__184__w 
                                              >> 0x30U)));
                vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__is_maap_r 
                    = (((0x22U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_1__lane)) 
                        & (0xf0U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_2__lane))) 
                       & (0xfeU == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_3__lane)));
            }
            if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r))) {
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__186__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_5__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__186__w 
                                              >> 0x10U)));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__187__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_6__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__187__w 
                                              >> 0x18U)));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__188__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_7__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__188__w 
                                              >> 0x20U)));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__189__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_8__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__189__w 
                                              >> 0x28U)));
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_start_r 
                    = ((0x000000000000ffffULL & vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_start_r) 
                       | ((QData)((IData)(((((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_5__lane) 
                                             << 0x00000018U) 
                                            | ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_6__lane) 
                                               << 0x00000010U)) 
                                           | (((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_7__lane) 
                                               << 8U) 
                                              | (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_8__lane))))) 
                          << 0x00000010U));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__190__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_9__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__190__w 
                                              >> 0x30U)));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__191__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_10__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__191__w 
                                              >> 0x38U)));
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_start_r 
                    = ((0x0000ffffffff0000ULL & vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_start_r) 
                       | (IData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_9__lane) 
                                           << 8U) | (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_10__lane)))));
            }
            if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r))) {
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__192__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__194__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_11__lane 
                    = (0x000000ffU & (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__192__w));
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_13__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__194__w 
                                              >> 0x10U)));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__193__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__195__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_12__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__193__w 
                                              >> 8U)));
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_14__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__195__w 
                                              >> 0x18U)));
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_cnt_r 
                    = (((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_11__lane) 
                        << 8U) | (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_12__lane));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__196__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_15__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__196__w 
                                              >> 0x20U)));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__197__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_16__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__197__w 
                                              >> 0x28U)));
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_conf_start_r 
                    = ((0x000000000000ffffULL & vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_conf_start_r) 
                       | ((QData)((IData)(((((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_13__lane) 
                                             << 0x00000018U) 
                                            | ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_14__lane) 
                                               << 0x00000010U)) 
                                           | (((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_15__lane) 
                                               << 8U) 
                                              | (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_16__lane))))) 
                          << 0x00000010U));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__198__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_17__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__198__w 
                                              >> 0x30U)));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__199__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_18__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__199__w 
                                              >> 0x38U)));
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_conf_start_r 
                    = ((0x0000ffffffff0000ULL & vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_conf_start_r) 
                       | (IData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_17__lane) 
                                           << 8U) | (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_18__lane)))));
            }
            if ((5U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r))) {
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__200__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_19__lane 
                    = (0x000000ffU & (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__200__w));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__201__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_20__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__201__w 
                                              >> 8U)));
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_conf_cnt_r 
                    = (((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_19__lane) 
                        << 8U) | (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_20__lane));
            }
            if (vlSelfRef.s_axis_mac_rx_tlast) {
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_done_p 
                    = (((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__is_maap_r) 
                        & (5U <= (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r))) 
                       & vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl);
                vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__is_maap_r = 0U;
            }
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_ctrl_req_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_we_r)) 
             & (0U == (0x000000ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ctrl_scratch_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_wdata_r;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_accept_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_src_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__mreq_src_r;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_rel_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__mreq_rel_r;
        }
        if (vlSelfRef.milan_datapath__DOT__csr__DOT__rd_pend) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit_q 
                = vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit;
            vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux_q 
                = vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux;
            vlSelfRef.milan_datapath__DOT__csr__DOT__shadow_qq 
                = vlSelfRef.milan_datapath__DOT__csr__DOT__shadow_q;
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux_q 
                = vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux;
            vlSelfRef.milan_datapath__DOT__csr__DOT__strm_hit_q 
                = ((0x0800U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                   & (0x0870U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)));
            vlSelfRef.milan_datapath__DOT__csr__DOT__rd_in_window_q 
                = (1U & ((~ (0U != (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q) 
                                                   >> 0x0000000bU)))) 
                         | ((0x08f8U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            | ((0x08fcU == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                               | (((0x0870U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                   & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) 
                                  | (((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) 
                                     | (((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                         & (0x08d4U 
                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) 
                                        | ((0x08d4U 
                                            == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                           | ((0x08d8U 
                                               == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              | ((0x0900U 
                                                  <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                 & (0x0940U 
                                                    > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))))))))))));
        }
        if (vlSelfRef.milan_datapath__DOT__csr__DOT__rds_busy_r) {
            if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_cyc_r))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__rds_cyc_r 
                    = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_cyc_r) 
                             - (IData)(1U)));
            } else if (vlSelfRef.milan_datapath__DOT__csr__DOT__rds_valid_w) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__rds_busy_r = 0U;
            }
        } else if (((IData)(vlSelfRef.s_axi_arready) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_is_slow_w))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__rds_busy_r = 1U;
            vlSelfRef.milan_datapath__DOT__csr__DOT__rds_dir_r 
                = vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r;
            vlSelfRef.milan_datapath__DOT__csr__DOT__rds_idx_r 
                = (7U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r));
            vlSelfRef.milan_datapath__DOT__csr__DOT__rds_cyc_r = 3U;
            vlSelfRef.milan_datapath__DOT__csr__DOT__rds_word_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r)
                    ? ((0x0810U == (IData)(vlSelfRef.s_axi_araddr))
                        ? 0U : ((0x081cU == (IData)(vlSelfRef.s_axi_araddr))
                                 ? 1U : 2U)) : ((0x0810U 
                                                 == (IData)(vlSelfRef.s_axi_araddr))
                                                 ? 4U
                                                 : 
                                                ((0x0824U 
                                                  == (IData)(vlSelfRef.s_axi_araddr))
                                                  ? 2U
                                                  : 3U)));
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__done_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__err_r = 0U;
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reg_we_w) 
             & (0U == (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_valid_r = 0U;
        }
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r))) {
            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__err_r = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 0U;
            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__done_r = 1U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 0U;
                } else if (vlSelfRef.i_nvm_mem_wr_done) {
                    if (vlSelfRef.i_nvm_mem_wr_err) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 0x0cU;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r 
                            = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r);
                        if ((1U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 0x0bU;
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r 
                                = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r) 
                                                  - (IData)(1U)));
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 9U;
                        }
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r))) {
                if (vlSelfRef.i_nvm_mem_wr_ready) {
                    if (vlSelfRef.i_nvm_mem_wr_done) {
                        if (vlSelfRef.i_nvm_mem_wr_err) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 0x0cU;
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r 
                                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r);
                            if ((1U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r))) {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 0x0bU;
                            } else {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r 
                                    = (0x0000ffffU 
                                       & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r) 
                                          - (IData)(1U)));
                            }
                        }
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 0x0aU;
                    }
                }
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_wvalid_w) {
                if ((1U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 0x0bU;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r 
                        = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r) 
                                          - (IData)(1U)));
                }
            }
        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r))) {
                    if (vlSelfRef.i_nvm_mem_wr_done) {
                        if (vlSelfRef.i_nvm_mem_wr_err) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 0x0cU;
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r 
                                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r);
                            if ((1U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r))) {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 0x0bU;
                            } else {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r 
                                    = (0x0000ffffU 
                                       & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r) 
                                          - (IData)(1U)));
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 5U;
                            }
                        }
                    }
                } else if (vlSelfRef.i_nvm_mem_wr_ready) {
                    if (vlSelfRef.i_nvm_mem_wr_done) {
                        if (vlSelfRef.i_nvm_mem_wr_err) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 0x0cU;
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r 
                                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r);
                            if ((1U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r))) {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 0x0bU;
                            } else {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r 
                                    = (0x0000ffffU 
                                       & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r) 
                                          - (IData)(1U)));
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 5U;
                            }
                        }
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 7U;
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_wvalid_w) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__byte_r 
                        = ((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))
                            ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r
                           [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r]
                            : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_wdata_w));
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 6U;
                }
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_rready_w) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r);
                if ((1U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 0x0bU;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r 
                        = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r) 
                                          - (IData)(1U)));
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 2U;
                }
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r))) {
                if (vlSelfRef.i_nvm_mem_rsp_valid) {
                    if (vlSelfRef.i_nvm_mem_rsp_err) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_valid_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 0x0cU;
                    } else if (vlSelfRef.i_nvm_mem_rsp_last) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_valid_r = 1U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_addr_r 
                            = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r 
                               >> 3U);
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_data_r 
                            = vlSelfRef.i_nvm_mem_rsp_data;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 4U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__byte_r 
                            = (0x000000ffU & (IData)(
                                                     (vlSelfRef.i_nvm_mem_rsp_data 
                                                      >> 
                                                      (0x0000003fU 
                                                       & (((IData)(0x3fU) 
                                                           - 
                                                           (0x00000038U 
                                                            & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r 
                                                               << 3U))) 
                                                          - (IData)(7U))))));
                    }
                }
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_hit_w) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__byte_r 
                    = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_data_r 
                                              >> (0x0000003fU 
                                                  & (((IData)(0x3fU) 
                                                      - 
                                                      (0x00000038U 
                                                       & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r 
                                                          << 3U))) 
                                                     - (IData)(7U))))));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 4U;
            } else if (vlSelfRef.i_nvm_mem_req_ready) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 3U;
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r))) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_rready_w) {
                if ((1U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 0x0bU;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r 
                        = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r) 
                                          - (IData)(1U)));
                }
            }
        } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_now_w) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_base_r 
                    + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w) 
                   + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_offset_w));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__eff_len_w;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_r = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__op_region_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__op_mut_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_opmut_w;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__op_full_r 
                = (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_op_w)) 
                    & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_offset_w))) 
                   & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__eff_len_w) 
                      == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__was_write_r 
                = (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_op_w));
            if ((0U != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_len_r)) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__span_ok_w) {
                    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__eff_len_w))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 0x0bU;
                    } else if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_op_w))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_live_w)
                                ? 2U : 1U);
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r 
                            = ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_op_w))
                                ? 5U : 9U);
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_valid_r = 0U;
                    }
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 0x0cU;
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r 
                    = (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_op_w)) 
                        & (0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_len_w)))
                        ? 1U : (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_op_w)) 
                                 & (0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_len_w)))
                                 ? 8U : 0x0bU));
            }
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_la_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_join_r = 0U;
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__rnd_act_r) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_txop_done_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__td_tk_r = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__rnd_act_r) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_txop_done_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__td_ls_r = 1U;
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__rnd_act_r) 
              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__td_tk_r) 
                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_txop_done_w))) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__td_ls_r) 
                | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_txop_done_w)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_join_r 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_join_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__rnd_act_r = 0U;
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__rnd_act_r) 
              & (0x0cU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_msrp_r))) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__hw_full_q_r)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_join_r 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_join_r));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_hit_w) {
            if ((4U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                       - (IData)(0x00000032U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_la_mvrp_r = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_la_r 
                    = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_la_r));
            } else if ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                              - (IData)(0x00000032U)))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_la_r 
                        = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_la_r));
                }
            }
            if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                           - (IData)(0x00000032U)) 
                          >> 2U)))) {
                if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                               - (IData)(0x00000032U)) 
                              >> 1U)))) {
                    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_join_r 
                            = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_join_r));
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__rnd_act_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__td_tk_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__td_ls_r = 0U;
                    }
                }
            }
        }
        vlSelfRef.milan_datapath__DOT__tctx_rd_valid_w = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_q_r 
            = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w) 
               & (~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_q_r)));
        if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_q_r) {
            vlSelfRef.milan_datapath__DOT__tctx_rd_data_w 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_q_r;
            vlSelfRef.milan_datapath__DOT__tctx_rd_valid_w = 1U;
        }
        if (((0x0800U == (IData)(vlSelfRef.s_axi_awaddr)) 
             & (IData)(vlSelfRef.s_axi_awready))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_fresh_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_we_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__declaring_r 
                = (((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_waddr_w))) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__declaring_r)) 
                   | (3U & ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[2U] 
                                          >> 0x00000012U))) 
                            << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_waddr_w))));
        }
        vlSelfRef.milan_datapath__DOT__aaf_frame_p_w = 0U;
        if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tsw_pend_r) {
            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__tsw_pend_r = 0U;
        }
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__est_r = 0U;
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
                if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tsw_pend_r)))) {
                    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r)))) {
                        vlSelfRef.milan_datapath__DOT__aaf_frames_w 
                            = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_q_r);
                    }
                    vlSelfRef.milan_datapath__DOT__aaf_frame_p_w = 1U;
                    vlSelfRef.milan_datapath__DOT__aaf_frame_idx_w 
                        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
                    vlSelfRef.milan_datapath__DOT__aaf_frame_tu_w 
                        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__etu_r;
                    vlSelfRef.milan_datapath__DOT__aaf_frame_mr_w 
                        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__emr_r;
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__est_r = 0U;
                }
            } else if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tsw_pend_r)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__est_r = 5U;
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
                if (vlSelfRef.milan_datapath__DOT__aaf_tx_tready) {
                    if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                         == (0x0000001fU & ((IData)(5U) 
                                            + ((IData)(6U) 
                                               * (7U 
                                                  & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                     >> 1U))))))) {
                        if ((0U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r))) {
                            __VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__pend_r__v0 
                                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
                            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__pend_r__v0 = 1U;
                        }
                        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__est_r = 4U;
                    } else {
                        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r 
                            = (0x0000001fU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r)));
                    }
                }
            } else {
                if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))) {
                    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eseq_r 
                        = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_q_r);
                } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))) {
                    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ets_r 
                        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_q_r;
                }
                if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))) {
                    if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eiss_r) 
                         != (0x0000001fU & ((IData)(6U) 
                                            * (7U & 
                                               ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                >> 1U)))))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__eiss_r 
                            = (0x0000001fU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eiss_r)));
                        if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eo_r) 
                             == ((7U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                        >> 1U)) - (IData)(1U)))) {
                            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__esmp_r 
                                = (7U & ((IData)(1U) 
                                         + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__esmp_r)));
                            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__eo_r = 0U;
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__eo_r 
                                = (3U & ((IData)(1U) 
                                         + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eo_r)));
                        }
                    }
                    if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ecap_r) 
                         != (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eiss_r))) {
                        if ((0x17U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ecap_r))) {
                            __VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v0 
                                = (0x00ffffffU & (IData)(
                                                         (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__stg_q_r 
                                                          >> 0x18U)));
                            __VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v0 
                                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ecap_r;
                            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v0 = 1U;
                            __VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r__v0 
                                = (0x00ffffffU & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__stg_q_r));
                            __VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r__v0 
                                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ecap_r;
                            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r__v0 = 1U;
                        }
                        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__ecap_r 
                            = (0x0000001fU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ecap_r)));
                        if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ecap_r) 
                             == (0x0000001fU & (((IData)(6U) 
                                                 * 
                                                 (7U 
                                                  & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                     >> 1U))) 
                                                - (IData)(1U))))) {
                            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__est_r = 3U;
                        }
                    }
                }
                if ((2U != (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__fph_r 
                        = (0x0000000fU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r)));
                }
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
            if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))) {
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__evid_r 
                    = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_q_r 
                                      >> 5U));
            } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))) {
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__edmac_r 
                    = ((0x0000ffff00000000ULL & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__edmac_r) 
                       | (IData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_q_r)));
            } else {
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__edmac_r 
                    = ((0x00000000ffffffffULL & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__edmac_r) 
                       | ((QData)((IData)((0x0000ffffU 
                                           & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_q_r))) 
                          << 0x00000020U));
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__euid_r 
                    = (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_q_r 
                       >> 0x10U);
            }
            if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__fph_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__est_r = 2U;
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__fph_r 
                    = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r)));
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__fph_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__eiss_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__ecap_r = 0U;
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__esmp_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__eo_r = 0U;
            if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r[0U]) {
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r = 0U;
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__etu_r 
                    = vlSelfRef.milan_datapath__DOT__clkv_tu_w;
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__emr_r 
                    = (1U & (IData)(vlSelfRef.milan_datapath__DOT__mcr_mr_v_w));
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ebank_r 
                    = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__wbank_r[0U])));
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__est_r = 2U;
            }
        }
        if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__stg_we_w) {
            if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__own_last_w) {
                if ((5U == vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r[0U])) {
                    __VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v0 
                        = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__wbank_r[0U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v0 = 1U;
                } else {
                    __VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v1 
                        = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r[0U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v1 = 1U;
                }
            }
            if (((0U == vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r[0U]) 
                 & (0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__tsw_pend_r = 1U;
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tsw_t_r = 0U;
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tsw_val_r 
                    = (((vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[1U] 
                         << 8U) | (vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[0U] 
                                   >> 0x00000018U)) 
                       + vlSelfRef.milan_datapath__DOT____Vcellinp__aaf_packetizer__transit_ns_i);
            }
        }
        if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_stream_en_w)))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v2 = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__aidx_r) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__gslope_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__over_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__over_acc_r) 
                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__refuse_w));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__over_acc_r = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__sum_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__fit_w)
                    ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cand_w)
                    : vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__acc_r);
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__acc_r = 0U;
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__over_acc_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__over_acc_r) 
                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__refuse_w));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__acc_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__fit_w)
                    ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cand_w)
                    : vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__acc_r);
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_giveup_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__alarm_r = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_req_w) 
             & (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_class_w)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__barrier_pend_r 
                = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_gnt_w)));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__accept_w) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_valid_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mem_busy_r = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_ix_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_w) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_ix_r 
                = (0x000001ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_ix_r)));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r = 0U;
            if (((IData)(vlSelfRef.i_desc_mem_rsp_last) 
                 | (IData)(vlSelfRef.i_desc_mem_rsp_err))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mem_busy_r = 0U;
            }
        }
        if (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_valid_r) 
               | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mem_busy_r)) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_w))) 
             & (0x1000U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r 
                = (0x00001fffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r)));
        }
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r))) {
            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r))) {
                if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 7U;
                } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r))) {
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_pipe_r) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_pipe_r = 0U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_data_r 
                            = ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_kind_r))
                                ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_q_r
                                : ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_kind_r))
                                    ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_reg_r
                                    : (((0x00001fffU 
                                         & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                            >> 3U)) 
                                        < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__len_lanes_w))
                                        ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_q_r
                                        : 0ULL)));
                    } else {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_pend_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__img_valid_r)
                                ? 6U : 0U);
                    }
                } else if ((0x3fU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_byte_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_byte_r 
                        = (0x0000003fU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_byte_r)));
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 0x0bU;
                } else if (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__key_type_r)) 
                            & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_name_r)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_byte_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_name_r = 1U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 0x0bU;
                } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_answer_r) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_err_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_data_r = 0ULL;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_pipe_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 0x0dU;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 6U;
                }
            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 0x0cU;
                } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_w) 
                            & (IData)(vlSelfRef.i_desc_mem_rsp_err))) {
                    if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__miss_cnt_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__miss_cnt_r 
                            = (0x0000ffffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__miss_cnt_r)));
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_err_r = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_data_r = 0ULL;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_pipe_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_len_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_nbase_r = 0xffffU;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 0x0dU;
                } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_w) 
                            & (IData)(vlSelfRef.i_desc_mem_rsp_last))) {
                    if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_nbase_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_byte_r = 0U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_answer_r = 1U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_name_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 0x0bU;
                    } else {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_err_r = 0U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_data_r = 0ULL;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_pipe_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 0x0dU;
                    }
                } else if ((0x1000U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r))) {
                    if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__miss_cnt_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__miss_cnt_r 
                            = (0x0000ffffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__miss_cnt_r)));
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_err_r = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_data_r = 0ULL;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_pipe_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mem_busy_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_len_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_nbase_r = 0xffffU;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 0x0dU;
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r))) {
                if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_valid_r)) 
                           & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mem_busy_r))))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_valid_r = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_addr_r 
                        = ((IData)(0x20000000U) + (0xfffffff8U 
                                                   & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_off_r));
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_beats_r 
                        = (0x000001ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__len_lanes_w));
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__accept_w) {
                    if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__fetch_cnt_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__fetch_cnt_r 
                            = (0x0000ffffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__fetch_cnt_r)));
                    }
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 0x0aU;
                } else if ((0x1000U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r))) {
                    if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__miss_cnt_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__miss_cnt_r 
                            = (0x0000ffffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__miss_cnt_r)));
                    }
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_valid_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_err_r = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_data_r = 0ULL;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_pipe_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_len_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_nbase_r = 0xffffU;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 0x0dU;
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_rd_r 
                    = (0x0000001fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_rd_r)));
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_rdy_r) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_cmp_r 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_cmp_r)));
                    if (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__type_hit_w) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__e_usable_w)) 
                          & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__key_index_r) 
                             >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_base_r))) 
                         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rel_w) 
                            < (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_q_r[2U] 
                               >> 0x00000010U)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_len_r 
                            = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_q_r[2U]);
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_nbase_r 
                            = ((0xffffU == (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_q_r[0U] 
                                            >> 0x00000010U))
                                ? 0x0000ffffU : (0x0000ffffU 
                                                 & (((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_q_r[0U] 
                                                      << 0x00000010U) 
                                                     | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_q_r[0U] 
                                                        >> 0x00000010U)) 
                                                    + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rel_w))));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_off_r 
                            = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_q_r[1U] 
                               + ((0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_q_r[0U]) 
                                  * (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rel_w)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 9U;
                    } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__type_hit_w) 
                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__e_usable_w)) 
                                & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__last_w)))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_base_r 
                            = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_base_r) 
                                              + ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_q_r[2U] 
                                                  << 0x00000010U) 
                                                 | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_q_r[2U] 
                                                    >> 0x00000010U))));
                    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__last_w) 
                                | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__type_hit_w) 
                                   & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__e_usable_w))))) {
                        if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__miss_cnt_r))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__miss_cnt_r 
                                = (0x0000ffffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__miss_cnt_r)));
                        }
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_err_r = 1U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_data_r = 0ULL;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_pipe_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_len_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_nbase_r = 0xffffU;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 0x0dU;
                    }
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_rdy_r = 1U;
            }
        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r))) {
                if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__take_wr_w) 
                      & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_name_w))) 
                     & (0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rowr_cnt_r)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rowr_cnt_r 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rowr_cnt_r)));
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_pend_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_pend_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_pend_r = 1U;
                    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_kind_r)))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_err_r = 1U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_data_r = 0ULL;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_pipe_r = 0U;
                        if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__miss_cnt_r))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__miss_cnt_r 
                                = (0x0000ffffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__miss_cnt_r)));
                        }
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_len_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_nbase_r = 0xffffU;
                    } else {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_err_r = 0U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_data_r = 0ULL;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_pipe_r = 0U;
                    }
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 0x0dU;
                }
                if (((((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r)) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__take_wr_w)) 
                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_name_w)) 
                     & ((((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__key_type_r)) 
                          & ((0x0000ffffU & ((IData)(1U) 
                                             + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_nbase_r))) 
                             == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                                >> 6U)))) 
                         | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_nbase_r) 
                            == (0x000003ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                               >> 6U)))) 
                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_111)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_byte_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_answer_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_name_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 0x0bU;
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__take_rd_w) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_pend_r = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_err_r = 0U;
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_name_w) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_pipe_r = 1U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_kind_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 0x0dU;
                    } else if ((0x0fU == (0x0000000fU 
                                          & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                             >> 0x00000010U)))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__key_cfg_r 
                            = (0x0000ffffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r));
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__key_type_r 
                            = (0x0000ffffU & (IData)(
                                                     (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r 
                                                      >> 0x10U)));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__key_index_r 
                            = (0x0000ffffU & (IData)(
                                                     (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r 
                                                      >> 0x20U)));
                        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__img_valid_r) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_rd_r = 0U;
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_cmp_r = 0U;
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_base_r = 0U;
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_rdy_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 8U;
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_pend_r = 1U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_kind_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 0U;
                        }
                    } else if ((IData)(((0x000d0000U 
                                         == (0x000f0000U 
                                             & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w)) 
                                        & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__img_valid_r))))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_pend_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_kind_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 0U;
                    } else {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_pipe_r = 1U;
                        if ((0x00080000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w)) {
                            if ((0x00040000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w)) {
                                if ((0x00020000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w)) {
                                    if ((0x00010000U 
                                         & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w)) {
                                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_kind_r = 0U;
                                    } else {
                                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_kind_r = 2U;
                                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_reg_r 
                                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__img_valid_r)
                                                ? (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_len_r))
                                                : 0ULL);
                                    }
                                } else if ((0x00010000U 
                                            & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w)) {
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_kind_r = 2U;
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_reg_r 
                                        = (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_config_r));
                                } else {
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_kind_r = 2U;
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_reg_r 
                                        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__img_valid_r)
                                            ? (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_nbase_r))
                                            : 0ULL);
                                }
                            } else if ((0x00020000U 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w)) {
                                if ((0x00010000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w)) {
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_kind_r = 2U;
                                    if (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_111) 
                                         & (((0U == 
                                              (0x0000ffffU 
                                               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r))) 
                                             | ((0U 
                                                 == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__key_type_r)) 
                                                & (1U 
                                                   == 
                                                   (0x0000ffffU 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r))))) 
                                            & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_lookup_entry_w 
                                               < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_names_r))))) {
                                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_reg_r 
                                            = ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_lookup_entry_w)) 
                                               << 6U);
                                    } else {
                                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_reg_r = 0ULL;
                                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_err_r = 1U;
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_kind_r = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_kind_r = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_kind_r = 0U;
                        }
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 0x0dU;
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_w) 
                     & (IData)(vlSelfRef.i_desc_mem_rsp_err))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 7U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__fault_r = 7U;
                } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_w) 
                            & (IData)(vlSelfRef.i_desc_mem_rsp_last))) {
                    if (((0x000fffffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_load_lane_r 
                                         + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_beats_r))) 
                         < vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_total_lanes_w)) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_load_lane_r 
                            = (0x000fffffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_load_lane_r 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_beats_r)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 4U;
                    } else {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__img_valid_r = 1U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__fault_r = 0U;
                        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_pend_r) 
                             & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_kind_r)))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_rd_r = 0U;
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_cmp_r = 0U;
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_base_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 8U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_pend_r = 0U;
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_rdy_r = 0U;
                        } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_pend_r) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 0x0dU;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_pend_r = 0U;
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_err_r = 0U;
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_data_r 
                                = (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_config_r));
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_pipe_r = 0U;
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 6U;
                        }
                    }
                } else if ((0x1000U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 7U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__fault_r = 8U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mem_busy_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r = 0U;
                }
            } else if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_names_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__img_valid_r = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__fault_r = 0U;
                if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_pend_r) 
                     & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_kind_r)))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_rd_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_cmp_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_base_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 8U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_pend_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_rdy_r = 0U;
                } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_pend_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 0x0dU;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_pend_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_err_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_data_r 
                        = (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_config_r));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_pipe_r = 0U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 6U;
                }
            } else {
                if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_valid_r)) 
                           & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mem_busy_r))))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_valid_r = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_addr_r 
                        = ((IData)(0x20000000U) + (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_names_off_r 
                                                   + 
                                                   (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_load_lane_r 
                                                    << 3U)));
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_beats_r 
                        = ((0x000001f8U < vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_lanes_left_w)
                            ? 0x000001f8U : (0x000001ffU 
                                             & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_lanes_left_w));
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__accept_w) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 5U;
                } else if ((0x1000U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 7U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__fault_r = 8U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_valid_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r = 0U;
                }
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_w) 
                     & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_ix_r)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_b0_r 
                        = vlSelfRef.i_desc_mem_rsp_data;
                }
                if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_w) 
                     & (IData)(vlSelfRef.i_desc_mem_rsp_err))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 7U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__fault_r = 7U;
                } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_w) 
                            & (IData)(vlSelfRef.i_desc_mem_rsp_last))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_load_lane_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 4U;
                } else if ((0x1000U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 7U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__fault_r = 8U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mem_busy_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r = 0U;
                }
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_ok_w) {
                if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_valid_r)) 
                           & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mem_busy_r))))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_valid_r = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_addr_r 
                        = ((IData)(0x20000000U) + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_index_off_r);
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_beats_r 
                        = (0x000001ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_entries_r) 
                                          << 1U));
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__accept_w) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 3U;
                } else if ((0x1000U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 7U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__fault_r = 8U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_valid_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r = 0U;
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 7U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__fault_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_fault_w;
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r))) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_w) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__cksum_r 
                    = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__cksum_r 
                        + (IData)((vlSelfRef.i_desc_mem_rsp_data 
                                   >> 0x20U))) + (IData)(vlSelfRef.i_desc_mem_rsp_data));
                if ((0U == (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_ix_r)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_b0_r 
                        = vlSelfRef.i_desc_mem_rsp_data;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_config_r 
                        = (0x0000ffffU & (IData)(vlSelfRef.i_desc_mem_rsp_data));
                } else if ((1U == (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_ix_r)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_entries_r 
                        = (0x0000ffffU & (IData)((vlSelfRef.i_desc_mem_rsp_data 
                                                  >> 0x30U)));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_names_r 
                        = (0x0000ffffU & (IData)((vlSelfRef.i_desc_mem_rsp_data 
                                                  >> 0x20U)));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_index_off_r 
                        = (IData)(vlSelfRef.i_desc_mem_rsp_data);
                } else if ((2U == (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_ix_r)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_names_off_r 
                        = (IData)((vlSelfRef.i_desc_mem_rsp_data 
                                   >> 0x20U));
                } else {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_desc_max_r 
                        = (0x0000ffffU & (IData)((vlSelfRef.i_desc_mem_rsp_data 
                                                  >> 0x30U)));
                }
            }
            if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_w) 
                 & (IData)(vlSelfRef.i_desc_mem_rsp_err))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 7U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__fault_r = 7U;
            } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_w) 
                        & (IData)(vlSelfRef.i_desc_mem_rsp_last))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 2U;
            } else if ((0x1000U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 7U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__fault_r = 8U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mem_busy_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r = 0U;
            }
        } else {
            if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_valid_r)) 
                       & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mem_busy_r))))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__cksum_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_valid_r = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_addr_r = 0x20000000U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_beats_r = 4U;
            }
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__accept_w) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 1U;
            } else if ((0x1000U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 7U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__fault_r = 8U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_valid_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r = 0U;
            }
        }
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r))) {
            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r))) {
                if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r))) {
                    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__status_r 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_shape_fault_r)
                                ? 0x0aU : 0U);
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sent_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__frame_len_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pad_len_w;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 4U;
                    } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wr_ready_r) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_out_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_end_r;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r 
                            = (0x000007ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_end_r) 
                                              - (IData)(0x000cU)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_next_pos_r;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r = 0ULL;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pending_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r 
                            = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_next_pos_r) 
                                >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_total_r))
                                ? 0x0fU : 0x0aU);
                    }
                } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r))) {
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pending_r) {
                        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wr_ready_r) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r 
                                = (0x000007ffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r)));
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pending_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r 
                                = (0x000007ffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r)));
                            if (((0x000007ffU & ((IData)(1U) 
                                                 + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r))) 
                                 >= (0x000007ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_len_r)))) {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_out_r 
                                    = (0x000007ffU 
                                       & ((IData)(8U) 
                                          + ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_out_r) 
                                             + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_rlen_r))));
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r 
                                    = (0x000007ffU 
                                       & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_out_r) 
                                           + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_rlen_r)) 
                                          - (IData)(4U)));
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r 
                                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_next_pos_r;
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r = 0U;
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r = 0ULL;
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r 
                                    = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_next_pos_r) 
                                        >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_total_r))
                                        ? 0x0fU : 0x0aU);
                            }
                        }
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pending_r = 1U;
                    }
                } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wr_ready_r) {
                    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_wr_phase_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_wr_phase_r = 1U;
                    } else {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_wr_phase_r = 0U;
                        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_exec_r) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 2U;
                        } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_len_r))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r 
                                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_start_r;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pending_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 0x0dU;
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_out_r 
                                = (0x000007ffU & ((IData)(8U) 
                                                  + 
                                                  ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_out_r) 
                                                   + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_rlen_r))));
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r 
                                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_next_pos_r;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r 
                                = (0x000007ffU & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_out_r) 
                                                   + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_rlen_r)) 
                                                  - (IData)(4U)));
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r = 0ULL;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r 
                                = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_next_pos_r) 
                                    >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_total_r))
                                    ? 0x0fU : 0x0aU);
                        }
                    }
                }
            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r))) {
                    if ((0x020cU < (0x000007ffU & ((IData)(8U) 
                                                   + 
                                                   ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_out_r) 
                                                    + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_rlen_w)))))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_next_pos_r;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_load_data_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r = 0ULL;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pending_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r 
                            = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_next_pos_r) 
                                >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_total_r))
                                ? 0x0fU : 0x0aU);
                    } else {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_exec_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_exec_w;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_rlen_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_rlen_w;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_status_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_status_w;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_wr_phase_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_upc_w;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r 
                            = (0x0000ffffU & (IData)(
                                                     (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r 
                                                      >> 0x30U)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ty_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ctrs_r 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_exec_w) 
                               & (0x0029U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_cmd_r)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__regun_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__acq_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__lockc_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gstri_r 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_exec_w) 
                               & (0x000fU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_cmd_r)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gavb_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gasp_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__eavl_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gcfg_r 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_exec_w) 
                               & (7U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_cmd_r)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsfmt_r 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_exec_w) 
                               & (9U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_cmd_r)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsrate_r 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_exec_w) 
                               & (0x0015U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_cmd_r)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gclks_r 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_exec_w) 
                               & (0x0017U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_cmd_r)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssrate_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sclks_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssfmt_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssinfo_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gctrl_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sctrl_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gname_r 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_exec_w) 
                               & (0x0011U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_cmd_r)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sname_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__scfg_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setc_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 0x0cU;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r 
                            = (0x0000ffffU & (IData)(
                                                     (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r 
                                                      >> 0x20U)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_ix_r 
                            = (0x0000ffffU & (IData)(
                                                     (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r 
                                                      >> 0x10U)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_cfg_r 
                            = (0x0000ffffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r));
                    }
                } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pending_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pending_r = 0U;
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_load_data_r) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r 
                            = (0x000007ffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r)));
                        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r))) {
                            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r))) {
                                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r))) {
                                    if ((8U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r))) {
                                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r 
                                            = ((0xffffffffffffff00ULL 
                                                & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r) 
                                               | (IData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)));
                                    }
                                } else if ((8U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r))) {
                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r 
                                        = ((0xffffffffffff00ffULL 
                                            & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r) 
                                           | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)) 
                                              << 8U));
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r))) {
                                if ((8U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r))) {
                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r 
                                        = ((0xffffffffff00ffffULL 
                                            & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r) 
                                           | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)) 
                                              << 0x00000010U));
                                }
                            } else if ((8U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r))) {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r 
                                    = ((0xffffffff00ffffffULL 
                                        & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r) 
                                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)) 
                                          << 0x00000018U));
                            }
                        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r))) {
                            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r))) {
                                if ((8U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r))) {
                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r 
                                        = ((0xffffff00ffffffffULL 
                                            & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r) 
                                           | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)) 
                                              << 0x00000020U));
                                }
                            } else if ((8U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r))) {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r 
                                    = ((0xffff00ffffffffffULL 
                                        & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r) 
                                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)) 
                                          << 0x00000028U));
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r))) {
                            if ((8U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r))) {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r 
                                    = ((0xff00ffffffffffffULL 
                                        & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r) 
                                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)) 
                                          << 0x00000030U));
                            }
                        } else if ((8U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r 
                                = ((0x00ffffffffffffffULL 
                                    & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r) 
                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)) 
                                      << 0x00000038U));
                        }
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r 
                            = (0x000007ffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r)));
                        if (((0x000007ffU & ((IData)(1U) 
                                             + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r))) 
                             >= (0x000007ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_len_r)))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_load_data_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 0x0bU;
                        }
                    } else {
                        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r))) {
                            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r))) {
                                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r))) {
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_cmd_r 
                                        = ((0xff00U 
                                            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_cmd_r)) 
                                           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o));
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_start_r 
                                        = (0x000007ffU 
                                           & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r)));
                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r = 0U;
                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r = 0ULL;
                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_load_data_r 
                                        = (0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_len_r));
                                    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_len_r))) {
                                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 0x0bU;
                                    }
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_next_pos_r 
                                        = (0x000007ffU 
                                           & ((IData)(1U) 
                                              + ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r) 
                                                 + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_len_r))));
                                } else {
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_cmd_r 
                                        = ((0x00ffU 
                                            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_cmd_r)) 
                                           | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o) 
                                              << 8U));
                                }
                            } else if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r)))) {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_cmd_status_r 
                                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o;
                            }
                        } else if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r) 
                                             >> 1U)))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_len_r 
                                = ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r))
                                    ? ((0xff00U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_len_r)) 
                                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o))
                                    : ((0x00ffU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_len_r)) 
                                       | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o) 
                                          << 8U)));
                        }
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r 
                            = (0x000007ffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r)));
                        if ((7U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r 
                                = (7U & ((IData)(1U) 
                                         + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r)));
                        }
                    }
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pending_r = 1U;
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_started_r) {
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pending_r) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pending_r = 0U;
                        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r))) {
                            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r))) {
                                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r))) {
                                    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_allowed__54__command_type 
                                        = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_cmd_hi_r) 
                                            << 8U) 
                                           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o));
                                    __Vtemp_39 = VL_MATCHMASKED_I(16, (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_allowed__54__command_type), Vmilan_datapath__ConstPool__CONST_hca6ff4b2_0);
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____VlemCall_0__gdi_allowed 
                                        = Vmilan_datapath__ConstPool__TABLE_h90282f34_0
                                        [__Vtemp_39];
                                    if (((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____VlemCall_0__gdi_allowed))) 
                                         || ((0x0001ffffU 
                                              & ((IData)(1U) 
                                                 + 
                                                 ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_len_r)))) 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_total_r)))) {
                                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x02c0U;
                                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 1U;
                                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_r = 0U;
                                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 2U;
                                    } else {
                                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r 
                                            = (0x000007ffU 
                                               & ((IData)(1U) 
                                                  + 
                                                  ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r) 
                                                   + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_len_r))));
                                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r = 0U;
                                    }
                                } else {
                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r 
                                        = (0x000007ffU 
                                           & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r)));
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_cmd_hi_r 
                                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o;
                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r = 7U;
                                }
                            } else {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r 
                                    = ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r))
                                        ? (7U & ((IData)(1U) 
                                                 + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r)))
                                        : 5U);
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r 
                                    = (0x000007ffU 
                                       & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r)));
                            }
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r 
                                = (0x000007ffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r)));
                            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r))) {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r 
                                    = (7U & ((IData)(1U) 
                                             + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r)));
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r))) {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_len_r 
                                    = ((0xff00U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_len_r)) 
                                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o));
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r = 2U;
                            } else {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_len_r 
                                    = ((0x00ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_len_r)) 
                                       | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o) 
                                          << 8U));
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r = 1U;
                            }
                        }
                    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r) 
                                >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_total_r))) {
                        if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x02c0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 1U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 2U;
                        } else if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_total_r))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r = 0U;
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__status_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 0x0fU;
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_load_data_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r = 0ULL;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 0x0aU;
                        }
                    } else if (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r)) 
                                & (8U > (0x000007ffU 
                                         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_total_r) 
                                            - (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r)))))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x02c0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 2U;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pending_r = 1U;
                    }
                } else if ((0x020cU < (0x000007ffU 
                                       & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                          >> 0x0000000eU)))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x02c0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 1U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 2U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_started_r = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_total_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_trim_w;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_trim_w;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cmd_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_trim_w;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pending_r = 0U;
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 0U;
            }
        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r))) {
                    if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__uns_r)
                                ? ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__gnt_r) 
                                   >> 1U) : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__gnt_r)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 8U;
                    }
                } else {
                    if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__resp_cnt_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__resp_cnt_r 
                            = (0x0000ffffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__resp_cnt_r)));
                    }
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 7U;
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_fail_w) {
                    if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rerr_cnt_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rerr_cnt_r 
                            = (0x0000ffffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rerr_cnt_r)));
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__err_mode_r = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__status_r = 0x0aU;
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_r) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_pld_w;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__frame_len_r 
                            = ((0x003cU > (0x000007ffU 
                                           & ((IData)(0x0026U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_pld_w))))
                                ? 0x0000003cU : (0x000007ffU 
                                                 & ((IData)(0x0026U) 
                                                    + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_pld_w))));
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__frame_len_r = 0x0000003cU;
                    }
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r = 0U;
                } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__byte_ok_w) {
                    if (((0x000007ffU & ((IData)(1U) 
                                         + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))) 
                         >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__frame_len_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 6U;
                    }
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r 
                        = (0x000007ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r)));
                }
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_fail_w) {
                if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rerr_cnt_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rerr_cnt_r 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rerr_cnt_r)));
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__err_mode_r = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__status_r = 0x0aU;
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_pld_w;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__frame_len_r 
                        = ((0x003cU > (0x000007ffU 
                                       & ((IData)(0x0026U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_pld_w))))
                            ? 0x0000003cU : (0x000007ffU 
                                             & ((IData)(0x0026U) 
                                                + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_pld_w))));
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__frame_len_r = 0x0000003cU;
                }
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r = 0U;
            } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__alloc_gnt_r) 
                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_87))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__tx_slot_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__alloc_slot_r;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 5U;
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__resp_send_w) {
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_r) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_status_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__status_r;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_end_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sent_r = 1U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__status_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__status_r;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r 
                            = (0x000007ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_r)
                                               ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_pld_w)
                                               : ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r)
                                                   ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cmd_r)
                                                   : 
                                                  ((0x000cU 
                                                    < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r))
                                                    ? 
                                                   ((0x0244U 
                                                     < 
                                                     (0x000007ffU 
                                                      & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r) 
                                                         - (IData)(0x000cU))))
                                                     ? 0x0244U
                                                     : 
                                                    ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r) 
                                                     - (IData)(0x000cU)))
                                                    : 0U))));
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ucpu_done_w) {
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_r) {
                        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__resp_send_w)
                               ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r)
                               : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_end_r)) 
                             != (0x000007ffU & ((IData)(8U) 
                                                + ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_out_r) 
                                                   + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_rlen_r)))))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_shape_fault_r = 1U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 0x0fU;
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 0x0eU;
                        }
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__frame_len_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pad_len_w;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r 
                            = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sent_r) 
                                | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__resp_send_w))
                                ? 4U : 8U);
                        if (((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sent_r) 
                                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__resp_send_w))) 
                             & (0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__drop_cnt_r)))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__drop_cnt_r 
                                = (0x0000ffffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__drop_cnt_r)));
                        }
                    }
                }
            } else {
                if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__disp_valid_r)))) {
                    if (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_23) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__opd0_r 
                            = (((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r) 
                                                  << 0x00000010U) 
                                                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)))) 
                                << 0x00000010U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_cfg_r)));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__opd1_r 
                            = (((QData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_55)) 
                                << 0x00000020U) | (QData)((IData)(
                                                                  (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_ix_r) 
                                                                    << 0x00000010U) 
                                                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_cfg_r)))));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__opd2_r 
                            = (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_ix_r));
                    } else {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__opd0_r 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__tix_w)
                                ? ((QData)((IData)(
                                                   (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r) 
                                                     << 0x00000010U) 
                                                    | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)))) 
                                   << 0x00000010U) : 
                               ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gasp_r)
                                 ? (0x0000000000090000ULL 
                                    | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)) 
                                       << 0x00000020U))
                                 : ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__lockc_r)
                                     ? (QData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_55))
                                     : (((QData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_209)) 
                                         << 0x00000010U) 
                                        | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r))))));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__opd1_r 
                            = (QData)((IData)(((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_r)
                                                ? vlSelfRef.__VdfgRegularize_h6e95ff9d_0_209
                                                : ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__tix_w)
                                                    ? vlSelfRef.__VdfgRegularize_h6e95ff9d_0_55
                                                    : 
                                                   ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gasp_r)
                                                     ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)
                                                     : 
                                                    ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ty_r) 
                                                       & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_207)) 
                                                      << 0x00000010U) 
                                                     | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r)))))));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__opd2_r 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_r)
                                ? (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ty_r))
                                : ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssrate_r)
                                    ? (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r 
                                       >> 0x00000020U)
                                    : ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sclks_r)
                                        ? (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r 
                                           >> 0x00000030U)
                                        : ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sctrl_r)
                                            ? (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r 
                                               >> 0x00000038U)
                                            : ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__scfg_r)
                                                ? (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r))
                                                : ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssinfo_r)
                                                    ? (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__silat_r))
                                                    : vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r))))));
                    }
                }
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__disp_valid_r = 1U;
                if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__disp_valid_r) 
                     & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ms_r)))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__disp_valid_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 3U;
                }
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r))) {
            if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_trim_w;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cmd_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_trim_w;
            }
            if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                 < (0x000007ffU & ((IData)(2U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r))))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r 
                    = (0x000007ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r)));
            } else {
                if ((IData)(((((((0x0000000cU == (0x0000001cU 
                                                  & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[11U])) 
                                 & (0x001bU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__raw_ct_r))) 
                                & (0xc50aU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r))) 
                               & (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pid_lo_r))) 
                              & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ty_r))) 
                             & (8U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cmd_r))))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x02e0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                }
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 2U;
                if ((IData)((((8U == (0x0000001cU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[11U])) 
                              & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ty_r))) 
                             & (((0U == (0x0000000fU 
                                         & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[11U] 
                                             << 2U) 
                                            | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                               >> 0x0000001eU)))) 
                                 & (4U == (0x0000ffffU 
                                           & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[4U] 
                                               << 4U) 
                                              | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[3U] 
                                                 >> 0x0000001cU))))) 
                                & (0x0014U <= (0x000007ffU 
                                               & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                                  >> 0x0000000eU))))))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x0620U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                }
                if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_r) 
                     & (0x000fU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x03e4U;
                } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_r) 
                            & (0x000eU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x0230U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 1U;
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_r) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_rsp_count_r 
                        = (0x000000ffU & ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cmd_r) 
                                            - (IData)(8U)) 
                                           >> 3U) & 
                                          (- (IData)(
                                                     (8U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cmd_r))))));
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 1U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r 
                        = ((((((0x000007ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                               >> 0x0000000eU)) 
                               != (0x0007ffffU & ((IData)(0x00000014U) 
                                                  + 
                                                  ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ty_r) 
                                                   << 3U)))) 
                              | (0x0014U > (0x000007ffU 
                                            & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                               >> 0x0000000eU)))) 
                             | (0x020cU < (0x000007ffU 
                                           & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                              >> 0x0000000eU)))) 
                            | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cmd_r) 
                               != (0x000007ffU & ((
                                                   (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                                    << 0x00000012U) 
                                                   | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                                      >> 0x0000000eU)) 
                                                  - (IData)(0x000cU)))))
                            ? 0x02c0U : (((0x000eU 
                                           != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)) 
                                          & (0x000fU 
                                             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)))
                                          ? 0x0360U
                                          : ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_remove_r)
                                              ? 0x06e0U
                                              : 0x06b0U)));
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__regun_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r 
                        = ((0x10000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[3U])
                            ? 0x034cU : 0x0340U);
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__acq_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x0360U;
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__lockc_r) {
                    if ((0x001cU > (0x000007ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                                   >> 0x0000000eU)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x02c0U;
                    } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__lock_ent_ok_r) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x0368U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x0360U;
                    }
                }
                if ((((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ctrs_r) 
                        & (5U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r))) 
                       & (6U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r))) 
                      & (9U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r))) 
                     & (0x0024U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x031cU;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gstri_r) {
                    if ((0x0010U > (0x000007ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                                   >> 0x0000000eU)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x02c0U;
                    } else if (((5U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)) 
                                & (6U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x0360U;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x0390U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gavb_r) {
                    if ((0x0010U > (0x000007ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                                   >> 0x0000000eU)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x02c0U;
                    } else if ((9U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x0360U;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x03b0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gasp_r) {
                    if ((0x0010U > (0x000007ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                                   >> 0x0000000eU)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x02c0U;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x03d0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__eavl_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x03f0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gcfg_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x0400U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsfmt_r) {
                    if ((0x0010U > (0x000007ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                                   >> 0x0000000eU)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x02c0U;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r 
                            = (((5U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)) 
                                & (6U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)))
                                ? 0x04c0U : 0x0420U);
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsrate_r) {
                    if ((0x0010U > (0x000007ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                                   >> 0x0000000eU)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x02c0U;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r 
                            = ((2U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r))
                                ? 0x04c8U : 0x0440U);
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gclks_r) {
                    if ((0x0010U > (0x000007ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                                   >> 0x0000000eU)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x02c0U;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r 
                            = ((0x0024U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r))
                                ? 0x04c8U : 0x0460U);
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gname_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r 
                        = (((0x0014U > (0x000007ffU 
                                        & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                           >> 0x0000000eU))) 
                            | (8U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cmd_r)))
                            ? 0x0568U : 0x0540U);
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sname_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r 
                        = ((IData)(((0x00150000U != 
                                     (0x01ffc000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U])) 
                                    | (0x0048U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cmd_r))))
                            ? 0x0568U : 0x0570U);
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssrate_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r 
                        = ((0x0014U > (0x000007ffU 
                                       & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                          >> 0x0000000eU)))
                            ? 0x04d8U : ((2U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r))
                                          ? 0x04c8U
                                          : 0x0480U));
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sclks_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r 
                        = ((0x0014U > (0x000007ffU 
                                       & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                          >> 0x0000000eU)))
                            ? 0x04d8U : ((0x0024U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r))
                                          ? 0x04c8U
                                          : 0x04a0U));
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gctrl_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r 
                        = ((0x0010U > (0x000007ffU 
                                       & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                          >> 0x0000000eU)))
                            ? 0x0528U : ((0x001aU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r))
                                          ? 0x0530U
                                          : 0x04e0U));
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sctrl_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r 
                        = ((0x0011U > (0x000007ffU 
                                       & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                          >> 0x0000000eU)))
                            ? 0x0528U : ((0x001aU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r))
                                          ? 0x0530U
                                          : 0x0500U));
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__scfg_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r 
                        = ((0x0010U > (0x000007ffU 
                                       & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                          >> 0x0000000eU)))
                            ? 0x05e9U : (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_85) 
                                          | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_86) 
                                             | (0U 
                                                != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r))))
                                          ? 0x05d0U
                                          : 0x05b0U));
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strm_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r 
                        = ((0x0010U > (0x000007ffU 
                                       & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                          >> 0x0000000eU)))
                            ? 0x06a0U : ((5U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r))
                                          ? 0x0680U
                                          : ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strt_r)
                                              ? 0x0640U
                                              : 0x0660U)));
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssfmt_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r 
                        = (((0x0018U > (0x000007ffU 
                                        & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                           >> 0x0000000eU))) 
                            | (0x000cU > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cmd_r)))
                            ? 0x0778U : (((5U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)) 
                                          & (6U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)))
                                          ? 0x04c0U
                                          : ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__run_this_w)
                                              ? 0x0760U
                                              : ((5U 
                                                  == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r))
                                                  ? 0x0700U
                                                  : 0x0720U))));
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssinfo_r) {
                    if (((0x0060U > (0x000007ffU & 
                                     (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                      >> 0x0000000eU))) 
                         | (0x0054U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cmd_r)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0x0780U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r 
                            = ((6U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r))
                                ? 0x0360U : ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__run_this_w)
                                              ? 0x0790U
                                              : ((0x20000000U 
                                                  != (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r 
                                                              >> 0x20U)))
                                                  ? 0x0360U
                                                  : 
                                                 ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__silat_r 
                                                   >> 0x1fU)
                                                   ? 0x02c0U
                                                   : 0x0740U))));
                    }
                }
            }
            if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r))) {
                if ((1U & (~ (1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                     - (IData)(1U)) 
                                    >> 0x0000000aU))))) {
                    if ((1U & (~ (1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                         - (IData)(1U)) 
                                        >> 9U))))) {
                        if ((1U & (~ (1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                             - (IData)(1U)) 
                                            >> 8U))))) {
                            if ((1U & (~ (1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                 - (IData)(1U)) 
                                                >> 7U))))) {
                                if ((1U & (~ (1U & 
                                              (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                - (IData)(1U)) 
                                               >> 6U))))) {
                                    if ((1U & (~ (1U 
                                                  & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                      - (IData)(1U)) 
                                                     >> 5U))))) {
                                        if ((0x00000010U 
                                             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                - (IData)(1U)))) {
                                            if ((8U 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                    - (IData)(1U)))) {
                                                if (
                                                    (4U 
                                                     & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                        - (IData)(1U)))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            (1U 
                                                             & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                                 - (IData)(1U)) 
                                                                >> 1U))))) {
                                                        if (
                                                            (1U 
                                                             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                                - (IData)(1U)))) {
                                                            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssinfo_r) {
                                                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__silat_r 
                                                                    = 
                                                                    ((0xffffff00U 
                                                                      & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__silat_r) 
                                                                     | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o));
                                                            }
                                                        } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssinfo_r) {
                                                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__silat_r 
                                                                = 
                                                                ((0xffff00ffU 
                                                                  & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__silat_r) 
                                                                 | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o) 
                                                                    << 8U));
                                                        }
                                                    }
                                                } else if (
                                                           (2U 
                                                            & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                               - (IData)(1U)))) {
                                                    if (
                                                        (1U 
                                                         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                            - (IData)(1U)))) {
                                                        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssinfo_r) {
                                                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__silat_r 
                                                                = 
                                                                ((0xff00ffffU 
                                                                  & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__silat_r) 
                                                                 | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o) 
                                                                    << 0x00000010U));
                                                        }
                                                    } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssinfo_r) {
                                                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__silat_r 
                                                            = 
                                                            ((0x00ffffffU 
                                                              & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__silat_r) 
                                                             | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o) 
                                                                << 0x00000018U));
                                                    }
                                                }
                                            } else if (
                                                       (1U 
                                                        & (~ 
                                                           (1U 
                                                            & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                                - (IData)(1U)) 
                                                               >> 2U))))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        (1U 
                                                         & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                             - (IData)(1U)) 
                                                            >> 1U))))) {
                                                    if (
                                                        ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__lockc_r) 
                                                         & (0U 
                                                            != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)))) {
                                                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__lock_ent_ok_r = 0U;
                                                    }
                                                }
                                            }
                                        } else if (
                                                   (8U 
                                                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                       - (IData)(1U)))) {
                                            if ((4U 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                    - (IData)(1U)))) {
                                                if (
                                                    (2U 
                                                     & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                        - (IData)(1U)))) {
                                                    if (
                                                        ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__lockc_r) 
                                                         & (0U 
                                                            != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)))) {
                                                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__lock_ent_ok_r = 0U;
                                                    }
                                                } else if (
                                                           (1U 
                                                            & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                               - (IData)(1U)))) {
                                                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setc_r) {
                                                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r 
                                                            = 
                                                            ((0xffffffffffffff00ULL 
                                                              & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r) 
                                                             | (IData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)));
                                                    }
                                                } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setc_r) {
                                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r 
                                                        = 
                                                        ((0xffffffffffff00ffULL 
                                                          & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r) 
                                                         | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)) 
                                                            << 8U));
                                                }
                                            } else if (
                                                       (2U 
                                                        & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                           - (IData)(1U)))) {
                                                if (
                                                    (1U 
                                                     & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                        - (IData)(1U)))) {
                                                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setc_r) {
                                                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r 
                                                            = 
                                                            ((0xffffffffff00ffffULL 
                                                              & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r) 
                                                             | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)) 
                                                                << 0x00000010U));
                                                    }
                                                } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setc_r) {
                                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r 
                                                        = 
                                                        ((0xffffffff00ffffffULL 
                                                          & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r) 
                                                         | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)) 
                                                            << 0x00000018U));
                                                }
                                            } else if (
                                                       (1U 
                                                        & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                           - (IData)(1U)))) {
                                                if (
                                                    (1U 
                                                     & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ix26_w)) 
                                                        & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gasp_r))))) {
                                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r 
                                                        = 
                                                        ((0xff00U 
                                                          & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r)) 
                                                         | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o));
                                                }
                                                if (
                                                    ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gname_r) 
                                                     | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sname_r))) {
                                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_cfg_r 
                                                        = 
                                                        ((0xff00U 
                                                          & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_cfg_r)) 
                                                         | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o));
                                                }
                                                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setc_r) {
                                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r 
                                                        = 
                                                        ((0xffffff00ffffffffULL 
                                                          & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r) 
                                                         | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)) 
                                                            << 0x00000020U));
                                                }
                                            } else {
                                                if (
                                                    (1U 
                                                     & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ix26_w)) 
                                                        & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gasp_r))))) {
                                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r 
                                                        = 
                                                        ((0x00ffU 
                                                          & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r)) 
                                                         | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o) 
                                                            << 8U));
                                                }
                                                if (
                                                    ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gname_r) 
                                                     | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sname_r))) {
                                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_cfg_r 
                                                        = 
                                                        ((0x00ffU 
                                                          & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_cfg_r)) 
                                                         | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o) 
                                                            << 8U));
                                                }
                                                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setc_r) {
                                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r 
                                                        = 
                                                        ((0xffff00ffffffffffULL 
                                                          & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r) 
                                                         | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)) 
                                                            << 0x00000028U));
                                                }
                                            }
                                        } else if (
                                                   (4U 
                                                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                       - (IData)(1U)))) {
                                            if ((2U 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                    - (IData)(1U)))) {
                                                if (
                                                    (1U 
                                                     & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                        - (IData)(1U)))) {
                                                    if (
                                                        (1U 
                                                         & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ctrs_r)))) {
                                                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ty_r 
                                                            = 
                                                            ((0xff00U 
                                                              & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ty_r)) 
                                                             | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o));
                                                    }
                                                    if (
                                                        ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gname_r) 
                                                         | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sname_r))) {
                                                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_ix_r 
                                                            = 
                                                            ((0xff00U 
                                                              & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_ix_r)) 
                                                             | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o));
                                                    }
                                                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setc_r) {
                                                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r 
                                                            = 
                                                            ((0xff00ffffffffffffULL 
                                                              & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r) 
                                                             | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)) 
                                                                << 0x00000030U));
                                                    }
                                                } else {
                                                    if (
                                                        (1U 
                                                         & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ctrs_r)))) {
                                                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ty_r 
                                                            = 
                                                            ((0x00ffU 
                                                              & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ty_r)) 
                                                             | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o) 
                                                                << 8U));
                                                    }
                                                    if (
                                                        ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gname_r) 
                                                         | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sname_r))) {
                                                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_ix_r 
                                                            = 
                                                            ((0x00ffU 
                                                              & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_ix_r)) 
                                                             | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o) 
                                                                << 8U));
                                                    }
                                                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setc_r) {
                                                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r 
                                                            = 
                                                            ((0x00ffffffffffffffULL 
                                                              & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r) 
                                                             | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)) 
                                                                << 0x00000038U));
                                                    }
                                                }
                                            } else if (
                                                       (1U 
                                                        & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                           - (IData)(1U)))) {
                                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pid_lo_r 
                                                    = 
                                                    ((2U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pid_lo_r)) 
                                                     | (0U 
                                                        == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)));
                                                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ix26_w) {
                                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r 
                                                        = 
                                                        ((0xff00U 
                                                          & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r)) 
                                                         | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o));
                                                }
                                            } else {
                                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pid_lo_r 
                                                    = 
                                                    ((1U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pid_lo_r)) 
                                                     | ((0xc1U 
                                                         == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)) 
                                                        << 1U));
                                                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ix26_w) {
                                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r 
                                                        = 
                                                        ((0x00ffU 
                                                          & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r)) 
                                                         | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o) 
                                                            << 8U));
                                                }
                                            }
                                        } else if (
                                                   (2U 
                                                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                       - (IData)(1U)))) {
                                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r 
                                                = (
                                                   (1U 
                                                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                       - (IData)(1U)))
                                                    ? 
                                                   ((0xff00U 
                                                     & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)) 
                                                    | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o))
                                                    : 
                                                   ((0x00ffU 
                                                     & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)) 
                                                    | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o) 
                                                       << 8U)));
                                        } else {
                                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__raw_ct_r 
                                                = (
                                                   (1U 
                                                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                                       - (IData)(1U)))
                                                    ? 
                                                   ((0xff00U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__raw_ct_r)) 
                                                    | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o))
                                                    : 
                                                   ((0x00ffU 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__raw_ct_r)) 
                                                    | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o) 
                                                       << 8U)));
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_aecp__txn_valid_i) 
                     & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_busy_w))) 
                    & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_amap_busy_w)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[0U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[0U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[1U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[1U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[2U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[2U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[3U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[4U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[5U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[5U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[6U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[6U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[7U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[7U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[8U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[8U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[9U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[9U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[10U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[11U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[11U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[12U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[12U];
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__drop_w) {
                if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__drop_cnt_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__drop_cnt_r 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__drop_cnt_r)));
                }
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 8U;
            } else {
                if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_cnt_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_cnt_r 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_cnt_r)));
                }
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_w;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_w;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ctrs_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ctrs_w;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_w;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_r 
                    = (((0x002cU == (0x0000ffffU & 
                                     ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                       << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                 >> 0x0000001cU)))) 
                        | (0x002dU == (0x0000ffffU 
                                       & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                           << 4U) | 
                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                           >> 0x0000001cU))))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_remove_r 
                    = ((0x002dU == (0x0000ffffU & (
                                                   (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                                    << 4U) 
                                                   | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                      >> 0x0000001cU)))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_uns_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__regun_r 
                    = (((0x0024U == (0x0000ffffU & 
                                     ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                       << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                 >> 0x0000001cU)))) 
                        | (0x0025U == (0x0000ffffU 
                                       & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                           << 4U) | 
                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                           >> 0x0000001cU))))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__acq_r 
                    = ((0U == (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                               << 4U) 
                                              | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                 >> 0x0000001cU)))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__lockc_r 
                    = ((1U == (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                               << 4U) 
                                              | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                 >> 0x0000001cU)))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gstri_r 
                    = ((0x000fU == (0x0000ffffU & (
                                                   (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                                    << 4U) 
                                                   | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                      >> 0x0000001cU)))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gavb_r 
                    = ((0x0027U == (0x0000ffffU & (
                                                   (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                                    << 4U) 
                                                   | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                      >> 0x0000001cU)))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gasp_r 
                    = ((0x0028U == (0x0000ffffU & (
                                                   (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                                    << 4U) 
                                                   | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                      >> 0x0000001cU)))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__eavl_r 
                    = ((2U == (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                               << 4U) 
                                              | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                 >> 0x0000001cU)))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gcfg_r 
                    = ((7U == (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                               << 4U) 
                                              | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                 >> 0x0000001cU)))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsfmt_r 
                    = ((9U == (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                               << 4U) 
                                              | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                 >> 0x0000001cU)))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsrate_r 
                    = ((0x0015U == (0x0000ffffU & (
                                                   (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                                    << 4U) 
                                                   | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                      >> 0x0000001cU)))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gclks_r 
                    = ((0x0017U == (0x0000ffffU & (
                                                   (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                                    << 4U) 
                                                   | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                      >> 0x0000001cU)))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssrate_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssrate_w;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sclks_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sclks_w;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssfmt_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssfmt_w;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssinfo_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssinfo_w;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gctrl_r 
                    = ((0x0019U == (0x0000ffffU & (
                                                   (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                                    << 4U) 
                                                   | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                      >> 0x0000001cU)))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sctrl_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sctrl_w;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gname_r 
                    = ((0x0011U == (0x0000ffffU & (
                                                   (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                                    << 4U) 
                                                   | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                      >> 0x0000001cU)))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sname_r 
                    = ((0x0010U == (0x0000ffffU & (
                                                   (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                                    << 4U) 
                                                   | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                      >> 0x0000001cU)))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__scfg_r 
                    = ((6U == (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                               << 4U) 
                                              | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                 >> 0x0000001cU)))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strt_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strt_w;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__stop_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__stop_w;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strm_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__stop_w) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strt_w));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setc_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssrate_w) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sclks_w) 
                          | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sctrl_w) 
                             | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssinfo_w) 
                                | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssfmt_w)))));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_w;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r = 0ULL;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__silat_r = 0U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__lock_ent_ok_r = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__uns_r = 0U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__err_mode_r = 0U;
                if ((7U == (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[1U] 
                                  >> 0x00000019U)))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cmd_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r = 0U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cmd_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cap_w;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cap_w;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_rsp_count_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ty_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_ix_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_cfg_r = 0U;
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_w) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__raw_ct_r 
                        = (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                           << 4U) | 
                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                           >> 0x0000001cU)));
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 9U;
                } else {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__raw_ct_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r 
                        = ((7U == (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[1U] 
                                         >> 0x00000019U)))
                            ? 2U : 1U);
                }
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r = 0U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pid_lo_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sent_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_started_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pending_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_load_data_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r = 0U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_wr_phase_r = 0U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_total_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_out_r = 0x000cU;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_rlen_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_end_r = 0U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_cmd_status_r = 0U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_shape_fault_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r = 0ULL;
            }
        } else if (((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__n_st_r)) 
                    & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_busy_w)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[12U] 
                = (0x00000100U | (0x0000007fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[12U]));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__uns_upc_w;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r 
                = (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_kind_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ctrs_r 
                = (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_kind_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_remove_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_amap_remove_r;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_uns_r 
                = (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_kind_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__regun_r 
                = (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_kind_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__acq_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__lockc_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gstri_r 
                = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_kind_r)) 
                   | (0x0bU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_kind_r)));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gavb_r 
                = (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_kind_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gasp_r 
                = (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_kind_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__eavl_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gcfg_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsfmt_r 
                = (0x0aU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_kind_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsrate_r 
                = (7U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_kind_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gclks_r 
                = (0x0dU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_kind_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssrate_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sclks_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssfmt_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssinfo_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gctrl_r 
                = (0x0cU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_kind_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sctrl_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gname_r 
                = (8U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_kind_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sname_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__scfg_r 
                = (9U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_kind_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strt_r 
                = ((0x0eU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_kind_r)) 
                   & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_arg0_r)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__stop_r 
                = ((0x0eU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_kind_r)) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_arg0_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strm_r 
                = (0x0eU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_kind_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setc_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_r = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_shape_fault_r = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__lock_ent_ok_r = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__uns_r = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__err_mode_r = 0U;
            if ((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_kind_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cmd_r 
                    = (0x000007ffU & ((IData)(8U) + 
                                      ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_amap_count_r) 
                                       << 3U)));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r 
                    = (0x000007ffU & ((IData)(8U) + 
                                      ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_amap_count_r) 
                                       << 3U)));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ty_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_amap_count_r;
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cmd_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ty_r = 0U;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_rsp_count_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r 
                = ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_kind_r))
                    ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_di_r)
                    : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_dt_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r 
                = ((9U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_kind_r))
                    ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_arg0_r)
                    : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_di_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_ix_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_arg0_r;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_cfg_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_arg1_r;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__raw_ct_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__uns_ct_w;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pid_lo_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sent_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 2U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                = (0x3fffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U]);
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[11U] 
                = (8U | (0xffffffe0U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[11U]));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[4U] 
                = ((0x3fffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[4U]) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id) 
                      << 0x0000001eU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[5U] 
                = (((IData)(vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id) 
                    >> 2U) | ((IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                                       >> 0x00000020U)) 
                              << 0x0000001eU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[6U] 
                = (((IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                             >> 0x00000020U)) >> 2U) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__hold_eid_r) 
                      << 0x0000001eU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[7U] 
                = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__hold_eid_r) 
                    >> 2U) | ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__hold_eid_r 
                                       >> 0x00000020U)) 
                              << 0x0000001eU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[8U] 
                = (((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__hold_eid_r 
                             >> 0x00000020U)) >> 2U) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__hold_mac_r) 
                      << 0x0000001eU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[9U] 
                = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__hold_mac_r) 
                    >> 2U) | ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__hold_mac_r 
                                       >> 0x00000020U)) 
                              << 0x0000001eU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                = (0x00030000U | ((0xfe000000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U]) 
                                  | ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__hold_mac_r 
                                              >> 0x00000020U)) 
                                     >> 2U)));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[4U] 
                = ((0xc0003fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[4U]) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__hold_seq_r) 
                      << 0x0000000eU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[3U] 
                = ((0x0fffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[3U]) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__uns_ct_w) 
                      << 0x0000001cU));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[4U] 
                = ((0xfffff000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[4U]) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__uns_ct_w) 
                      >> 4U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[1U] 
                = (0x0e000000U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[1U]);
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p1_d_r 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w;
        if (vlSelfRef.milan_datapath__DOT__lb_tap_tvalid_w) {
            if (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__stash_open_w) {
                vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__stash_strm_r 
                    = vlSelfRef.milan_datapath__DOT__lb_tap_tuser_w;
            }
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_fed_r = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ext_wr_ok_w) {
            if ((0U == (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r)))) {
                if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__wing_stg_hit_w)))) {
                    vlSelfRef.milan_datapath__DOT__wing_sid_hi_r = 0U;
                }
                vlSelfRef.milan_datapath__DOT__wing_sid_lo_r 
                    = vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_data_r;
            } else if ((1U == (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r)))) {
                vlSelfRef.milan_datapath__DOT__wing_sid_hi_r 
                    = vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_data_r;
                if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__wing_stg_hit_w)))) {
                    vlSelfRef.milan_datapath__DOT__wing_sid_lo_r = 0U;
                }
            }
            vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_p_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_disc_arm_w) {
            VL_ASSIGNSEL_WQ(128, 64, (0x0000007fU & 
                                      ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r) 
                                       << 6U)), vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_disc_eid_w);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r) 
                   | (3U & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r))));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_disc_disarm_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_vld_r) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__accept_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_vld_r = 0U;
        }
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cp_r))) {
            if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_vld_r) 
                 & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__accept_w)))) {
                if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_drop_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_drop_r 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_drop_r)));
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_vld_r = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_protocol_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_msg_type_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_msg_type_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_status_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_status_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_cdl_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_cdl_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_src_mac_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_src_mac_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_ctlr_eid_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_target_eid_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_target_eid_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_seq_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_seq_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_opcode_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_opcode_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_u_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_u_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_cr_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_cr_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_operands_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_operands_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_rx_slot_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_rx_slot_r;
            }
        }
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_bin_r 
            = vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_bin_n;
        vlSelfRef.milan_datapath__DOT__rsp_pop_p_w = 0U;
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_take_w) 
             & (0U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))) {
            vlSelfRef.milan_datapath__DOT__rsp_pop_p_w = 1U;
        }
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__tick_d_r 
            = (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__sched_r) 
                & (3U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__beat_r))) 
               & (0U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)));
        if (((~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__sched_r)) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__media_tick_p) 
                | (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__tick_q_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__render_setpoint__DOT__sched_r = 1U;
            vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__tick_q_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__render_setpoint__DOT__slot_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__render_setpoint__DOT__beat_r = 0U;
        } else if (vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__sched_r) {
            if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__beat_r))) {
                vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ev_ok_r 
                    = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_take_w;
                vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ev_row_r 
                    = (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_pop_w));
            }
            if (vlSelfRef.milan_datapath__DOT__media_tick_p) {
                vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__tick_q_r = 1U;
            }
            if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__beat_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__render_setpoint__DOT__beat_r = 0U;
                if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__render_setpoint__DOT__sched_r = 0U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__render_setpoint__DOT__slot_r 
                        = (0x0000000fU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)));
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__render_setpoint__DOT__beat_r 
                    = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__beat_r)));
            }
        }
        if ((((9U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_arm_r)) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_taint_r = 0U;
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_wr_w) 
                     & ((0x0aU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
                        | ((0x0eU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
                           | ((0x0fU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
                              | ((0x0bU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
                                 | ((0x0cU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
                                    | (0x0dU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)))))))) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r) 
                       == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sink_r)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_taint_r = 1U;
        }
        vlSelfRef.milan_datapath__DOT__csr__DOT__stats_rst_p = 0U;
        vlSelfRef.milan_datapath__DOT__speed_q = vlSelfRef.milan_datapath__DOT__speed_sync;
        if (vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__aaf_tx_acc_w) {
            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__aaf_tx_inframe_r 
                = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_tx_tlast)));
        }
        if (vlSelfRef.s_axis_mac_rx_tvalid) {
            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__mac_rx_inframe_r 
                = (1U & (~ (IData)(vlSelfRef.s_axis_mac_rx_tlast)));
        }
        if (vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_go_w) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_side_r 
                = (1U & (vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_sel 
                         >> 8U));
            vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r 
                = (0x0000003fU & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_sel);
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__frame_bytes_r 
            = (0x0001ffffU & ((IData)(0x00000014U) 
                              + ((0x00000044U > vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__f_raw_w)
                                  ? 0x00000044U : vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__f_raw_w)));
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_r 
            = (1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_r)) 
                     & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_r))));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_q1_r 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_r;
        if (vlSelfRef.s_axi_arready) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q 
                = vlSelfRef.s_axi_araddr;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reg_we_w) {
            if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w) 
                          >> 4U)))) {
                if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w) 
                              >> 3U)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w) 
                                  >> 2U)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w) 
                                      >> 1U)))) {
                            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w)))) {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_base_r 
                                    = vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_wdata_r;
                            }
                            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))) {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_len_r 
                                    = vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_wdata_r;
                            }
                        }
                    }
                }
            }
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_txop_done_w = 0U;
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_la_msrp_r) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__laown_pend_r = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__laown_pend_r = 1U;
        }
        if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r))) {
            if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_join_fsm_r) 
                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tick_pend_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tick_pend_r = 0U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wtxla_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__laown_pend_r;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__laown_pend_r = 0U;
            }
        } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r))) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_join_fsm_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tick_pend_r = 1U;
            }
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_grant_w) {
                if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wmsg_w) 
                              >> 3U) & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                                        >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r))))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_code_r 
                        = (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wmsg_w));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_fp_r 
                        = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r) 
                                 >> (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r) 
                                           << 1U))));
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r = 2U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r[0U] = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r[1U] = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r[2U] = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r[3U] = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r[4U] = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r[5U] = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r[6U] 
                        = ((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r
                                                     [
                                                     (((IData)(0x0000003fU) 
                                                       + 
                                                       ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r) 
                                                        << 6U)) 
                                                      >> 5U)])) 
                                     << 0x00000020U) 
                                    | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r
                                                      [
                                                      (0x07fffffeU 
                                                       & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r) 
                                                          << 1U))])))) 
                           << 0x00000010U);
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r[7U] 
                        = (((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r
                                                      [
                                                      (((IData)(0x0000003fU) 
                                                        + 
                                                        ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r) 
                                                         << 6U)) 
                                                       >> 5U)])) 
                                      << 0x00000020U) 
                                     | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r
                                                       [
                                                       (0x07fffffeU 
                                                        & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r) 
                                                           << 1U))])))) 
                            >> 0x00000010U) | ((IData)(
                                                       ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r
                                                                          [
                                                                          (((IData)(0x0000003fU) 
                                                                            + 
                                                                            ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r) 
                                                                             << 6U)) 
                                                                           >> 5U)])) 
                                                          << 0x00000020U) 
                                                         | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r
                                                                           [
                                                                           (0x07fffffeU 
                                                                            & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r) 
                                                                               << 1U))]))) 
                                                        >> 0x00000020U)) 
                                               << 0x00000010U));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r[8U] 
                        = ((IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r
                                                      [
                                                      (((IData)(0x0000003fU) 
                                                        + 
                                                        ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r) 
                                                         << 6U)) 
                                                       >> 5U)])) 
                                      << 0x00000020U) 
                                     | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r
                                                       [
                                                       (0x07fffffeU 
                                                        & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r) 
                                                           << 1U))]))) 
                                    >> 0x00000020U)) 
                           >> 0x00000010U);
                } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r = 3U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r 
                        = (1U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)));
                }
            }
        } else if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r))) {
            if (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_238) 
                 & ((2U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r)) 
                    & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r))))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r = 3U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r 
                        = (1U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)));
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r = 1U;
                }
            }
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_join_fsm_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tick_pend_r = 1U;
            }
        } else {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_join_fsm_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tick_pend_r = 1U;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_txop_done_w = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r = 0U;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_txop_done_w = 0U;
        if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r))) {
            if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_join_fsm_r) 
                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tick_pend_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tick_pend_r = 0U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wtxla_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__laown_pend_r;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__laown_pend_r = 0U;
            }
        } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r))) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_join_fsm_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tick_pend_r = 1U;
            }
            if (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_19)
                  ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_13)
                  : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_33)
                      ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_13)
                      : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_32)
                          ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_13)
                          : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_27)
                              ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_13)
                              : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_31)
                                  ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_13)
                                  : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_57) 
                                     | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_13)))))))) {
                if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wmsg_w) 
                              >> 3U) & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                        >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r))))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_code_r 
                        = (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wmsg_w));
                    if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r) 
                               >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r)))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_type_r = 2U;
                        __Vtemp_46[0U] = (1U | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w) 
                                                << 8U));
                        __Vtemp_46[1U] = (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w) 
                                           >> 0x00000018U) 
                                          | ((IData)(
                                                     (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                      >> 0x00000020U)) 
                                             << 8U));
                        __Vtemp_46[2U] = ((IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                   >> 0x00000020U)) 
                                          >> 0x00000018U);
                    } else {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_type_r = 1U;
                        __Vtemp_46[0U] = 0U;
                        __Vtemp_46[1U] = 0U;
                        __Vtemp_46[2U] = 0U;
                    }
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r = 2U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[0U] 
                        = __Vtemp_46[0U];
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[1U] 
                        = __Vtemp_46[1U];
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[2U] 
                        = ((0xffffff00U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[2U]) 
                           | __Vtemp_46[2U]);
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[2U] 
                        = ((0x000000ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[2U]) 
                           | ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lat_r 
                                       >> ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r) 
                                           << 5U))) 
                              << 8U));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[3U] 
                        = ((0xffffff00U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[3U]) 
                           | ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lat_r 
                                       >> ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r) 
                                           << 5U))) 
                              >> 0x00000018U));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[3U] 
                        = ((0x000000ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[3U]) 
                           | (((0x00ffff00U & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__mif_r 
                                                >> (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_221)) 
                                               << 8U)) 
                               | ((0x000000e0U & ((
                                                   ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__prio_r) 
                                                    >> (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_97)) 
                                                   & (- (IData)(
                                                                (5U 
                                                                 >= (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_97))))) 
                                                  << 5U)) 
                                  | (0x00000010U & 
                                     (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rank_r) 
                                       >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r)) 
                                      << 4U)))) << 8U));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[4U] 
                        = ((0x0fff0000U & (((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vid_r 
                                             >> (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_96)) 
                                            & (- (IData)(
                                                         (0x17U 
                                                          >= (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_96))))) 
                                           << 0x00000010U)) 
                           | (0x0000ffffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__mfs_r 
                                             >> (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_221))));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[5U] 
                        = (IData)((0x0000ffffffffffffULL 
                                   & ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r
                                                        [
                                                        (((IData)(0x0000002fU) 
                                                          + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95)) 
                                                         >> 5U)])) 
                                        << ((0U == 
                                             (0x0000001fU 
                                              & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95)))
                                             ? 0x00000020U
                                             : ((IData)(0x00000040U) 
                                                - (0x0000001fU 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95))))) 
                                       | (((0U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95)))
                                            ? 0ULL : 
                                           ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r
                                                            [
                                                            (((IData)(0x0000001fU) 
                                                              + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95)) 
                                                             >> 5U)])) 
                                            << ((IData)(0x00000020U) 
                                                - (0x0000001fU 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95))))) 
                                          | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r
                                                             [
                                                             ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95) 
                                                              >> 5U)])) 
                                             >> (0x0000001fU 
                                                 & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95))))) 
                                      & (- (QData)((IData)(
                                                           (0x5fU 
                                                            >= (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95))))))));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[6U] 
                        = ((0xffff0000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[6U]) 
                           | (IData)(((0x0000ffffffffffffULL 
                                       & ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r
                                                            [
                                                            (((IData)(0x0000002fU) 
                                                              + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95)) 
                                                             >> 5U)])) 
                                            << ((0U 
                                                 == 
                                                 (0x0000001fU 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95)))
                                                 ? 0x00000020U
                                                 : 
                                                ((IData)(0x00000040U) 
                                                 - 
                                                 (0x0000001fU 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95))))) 
                                           | (((0U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95)))
                                                ? 0ULL
                                                : ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r
                                                                   [
                                                                   (((IData)(0x0000001fU) 
                                                                     + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95)) 
                                                                    >> 5U)])) 
                                                   << 
                                                   ((IData)(0x00000020U) 
                                                    - 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95))))) 
                                              | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r
                                                                 [
                                                                 ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95) 
                                                                  >> 5U)])) 
                                                 >> 
                                                 (0x0000001fU 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95))))) 
                                          & (- (QData)((IData)(
                                                               (0x5fU 
                                                                >= (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95))))))) 
                                      >> 0x00000020U)));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[6U] 
                        = ((0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[6U]) 
                           | ((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__sid_r
                                                        [
                                                        (((IData)(0x0000003fU) 
                                                          + 
                                                          ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r) 
                                                           << 6U)) 
                                                         >> 5U)])) 
                                        << 0x00000020U) 
                                       | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__sid_r
                                                         [
                                                         (0x07fffffeU 
                                                          & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r) 
                                                             << 1U))])))) 
                              << 0x00000010U));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[7U] 
                        = (((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__sid_r
                                                      [
                                                      (((IData)(0x0000003fU) 
                                                        + 
                                                        ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r) 
                                                         << 6U)) 
                                                       >> 5U)])) 
                                      << 0x00000020U) 
                                     | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__sid_r
                                                       [
                                                       (0x07fffffeU 
                                                        & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r) 
                                                           << 1U))])))) 
                            >> 0x00000010U) | ((IData)(
                                                       ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__sid_r
                                                                          [
                                                                          (((IData)(0x0000003fU) 
                                                                            + 
                                                                            ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r) 
                                                                             << 6U)) 
                                                                           >> 5U)])) 
                                                          << 0x00000020U) 
                                                         | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__sid_r
                                                                           [
                                                                           (0x07fffffeU 
                                                                            & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r) 
                                                                               << 1U))]))) 
                                                        >> 0x00000020U)) 
                                               << 0x00000010U));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[8U] 
                        = ((IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__sid_r
                                                      [
                                                      (((IData)(0x0000003fU) 
                                                        + 
                                                        ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r) 
                                                         << 6U)) 
                                                       >> 5U)])) 
                                      << 0x00000020U) 
                                     | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__sid_r
                                                       [
                                                       (0x07fffffeU 
                                                        & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r) 
                                                           << 1U))]))) 
                                    >> 0x00000020U)) 
                           >> 0x00000010U);
                } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r = 3U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r 
                        = (1U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r)));
                }
            }
        } else if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r))) {
            if (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_238) 
                 & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r)))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r = 3U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r 
                        = (1U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r)));
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r = 1U;
                }
            }
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_join_fsm_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tick_pend_r = 1U;
            }
        } else {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_join_fsm_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tick_pend_r = 1U;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_txop_done_w = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_open_w) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_open_r = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_s_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__seal_pend_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__served_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rvalid_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__roff_r = 4U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__fault_r = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__fcode_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__len_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_valid_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__bix_r = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wr_ready_r = 1U;
        } else {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__accept_w) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_valid_r = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__bix_r = 0U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wr_ready_r = 0U;
            } else if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_valid_r)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wr_ready_r 
                    = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r)) 
                       | (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r)));
            }
            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r))) {
                if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rvalid_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_valid_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wr_ready_r = 1U;
                } else if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r)))) {
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__beat_w) {
                        if (((IData)(vlSelfRef.i_resp_mem_rsp_last) 
                             | (IData)(vlSelfRef.i_resp_mem_rsp_err))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rbusy_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r = 5U;
                        }
                    } else if ((0x1000U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__tmo_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rbusy_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r = 5U;
                    }
                }
            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r))) {
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__beat_w) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rlane_r 
                            = vlSelfRef.i_resp_mem_rsp_data;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rvalid_r = 1U;
                        if (vlSelfRef.i_resp_mem_rsp_last) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rbusy_r = 0U;
                        }
                        if (vlSelfRef.i_resp_mem_rsp_err) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rvalid_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rbusy_r = 0U;
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__fault_r = 1U;
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__fcode_r = 4U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r = 6U;
                        }
                    }
                    if ((((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r)) 
                          & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pay_w) 
                             & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r)) 
                                & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_r)) 
                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_rd_valid_w))))) 
                         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rvalid_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__served_r 
                            = (0x000007ffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__served_r)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__roff_r 
                            = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__roff_r)));
                        if ((7U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__roff_r))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rvalid_r = 0U;
                        }
                        if (((0x000007ffU & ((IData)(1U) 
                                             + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__served_r))) 
                             >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__len_r))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rvalid_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r 
                                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rbusy_r)
                                    ? 4U : 5U);
                        }
                    }
                    if ((0x1000U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__tmo_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rbusy_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rvalid_r = 0U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__fault_r = 1U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__fcode_r = 3U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r = 6U;
                    }
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__seal_pend_r = 0U;
                    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__len_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r = 5U;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rreq_r = 1U;
                        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rreq_r) 
                             & (IData)(vlSelfRef.i_resp_mem_req_ready))) {
                            if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__burst_r))) {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__burst_r 
                                    = (0x0000ffffU 
                                       & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__burst_r)));
                            }
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rreq_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rbusy_r = 1U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__roff_r = 4U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r = 3U;
                        } else if ((0x1000U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__tmo_r))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rreq_r = 0U;
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__fault_r = 1U;
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__fcode_r = 3U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r = 6U;
                        }
                    }
                }
            } else {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r))) {
                    if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wreq_r) 
                         & (IData)(vlSelfRef.i_resp_mem_wr_ready))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wreq_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wbusy_r = 1U;
                    }
                    if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wbusy_r) 
                         & (IData)(vlSelfRef.i_resp_mem_wr_done))) {
                        if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lanewr_r))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lanewr_r 
                                = (0x0000ffffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lanewr_r)));
                        }
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wbusy_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_open_r = 0U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_s_r = 0U;
                        if (vlSelfRef.i_resp_mem_wr_err) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__fault_r = 1U;
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__fcode_r = 2U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r = 6U;
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r 
                                = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__seal_pend_r) 
                                    & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_valid_r)))
                                    ? 2U : 0U);
                        }
                    } else if ((0x1000U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__tmo_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wreq_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wbusy_r = 0U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__fault_r = 1U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__fcode_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r = 6U;
                    }
                } else {
                    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__need_flush_w)) 
                         & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_110))) {
                        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__keep_w) 
                             & (0U != Vmilan_datapath__ConstPool__TABLE_h1b26f04f_0
                                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_strb_r]))) {
                            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_open_r)))) {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_open_r = 1U;
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_ix_r 
                                    = (0x0000007fU 
                                       & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__babs_w) 
                                          >> 3U));
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_d_r = 0ULL;
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_s_r = 0U;
                            }
                            if ((0U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__babs_w)))) {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_d_r 
                                    = ((0x00ffffffffffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_d_r) 
                                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__bval_w)) 
                                          << 0x00000038U));
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_s_r 
                                    = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_s_r));
                            }
                            if ((1U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__babs_w)))) {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_d_r 
                                    = ((0xff00ffffffffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_d_r) 
                                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__bval_w)) 
                                          << 0x00000030U));
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_s_r 
                                    = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_s_r));
                            }
                            if ((2U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__babs_w)))) {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_d_r 
                                    = ((0xffff00ffffffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_d_r) 
                                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__bval_w)) 
                                          << 0x00000028U));
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_s_r 
                                    = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_s_r));
                            }
                            if ((3U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__babs_w)))) {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_d_r 
                                    = ((0xffffff00ffffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_d_r) 
                                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__bval_w)) 
                                          << 0x00000020U));
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_s_r 
                                    = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_s_r));
                            }
                            if ((4U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__babs_w)))) {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_d_r 
                                    = ((0xffffffff00ffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_d_r) 
                                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__bval_w)) 
                                          << 0x00000018U));
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_s_r 
                                    = (0x00000010U 
                                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_s_r));
                            }
                            if ((5U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__babs_w)))) {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_d_r 
                                    = ((0xffffffffff00ffffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_d_r) 
                                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__bval_w)) 
                                          << 0x00000010U));
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_s_r 
                                    = (0x00000020U 
                                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_s_r));
                            }
                            if ((6U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__babs_w)))) {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_d_r 
                                    = ((0xffffffffffff00ffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_d_r) 
                                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__bval_w)) 
                                          << 8U));
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_s_r 
                                    = (0x00000040U 
                                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_s_r));
                            }
                            if ((7U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__babs_w)))) {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_d_r 
                                    = ((0xffffffffffffff00ULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_d_r) 
                                       | (IData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__bval_w)));
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_s_r 
                                    = (0x00000080U 
                                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_s_r));
                            }
                        } else if (((0U != Vmilan_datapath__ConstPool__TABLE_h1b26f04f_0
                                     [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_strb_r]) 
                                    & (0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__drop_r)))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__drop_r 
                                = (0x0000ffffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__drop_r)));
                        }
                        if (((7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__bix_r))) 
                             >= Vmilan_datapath__ConstPool__TABLE_h1b26f04f_0
                             [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_strb_r])) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_valid_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__bix_r = 0U;
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wr_ready_r = 1U;
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__bix_r 
                                = (3U & ((IData)(1U) 
                                         + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__bix_r)));
                        }
                    }
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__need_flush_w) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wreq_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r = 1U;
                    } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__seal_pend_r) 
                                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_seal_w)) 
                                & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_valid_r)))) {
                        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_open_r) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wreq_r = 1U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r = 1U;
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r = 2U;
                        }
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_seal_w) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__len_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_seal_len_w;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__seal_pend_r = 1U;
                }
            }
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ucpu_done_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_we_r = 0U;
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ms_r))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ms_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ms_r = 0U;
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ms_r))) {
                if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w)) 
                           & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__raw_d_w))))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rom_q_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rom_r
                        [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__upc_r];
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_d_r = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__upc_r 
                        = (0x000007ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__upc_r)));
                }
                if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w)))) {
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__raw_d_w) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_e_r = 0U;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_e_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_d_r;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rom_q_r;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rf_r
                            [(0x0000000fU & (IData)(
                                                    (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rom_q_r 
                                                     >> 0x00000023U)))];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opb_e_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rf_r
                            [(0x0000000fU & (IData)(
                                                    (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rom_q_r 
                                                     >> 0x0000001fU)))];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opd_e_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rf_r
                            [(0x0000000fU & (IData)(
                                                    (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rom_q_r 
                                                     >> 0x00000027U)))];
                    }
                }
                if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_e_r) 
                     & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rb_hold_w)))) {
                    if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                       >> 0x0000002fU)))) {
                        if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                           >> 0x0000002eU)))) {
                            if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                               >> 0x0000002dU)))) {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r = 0U;
                            } else if ((1U & (IData)(
                                                     (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                      >> 0x0000002cU)))) {
                                if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                   >> 0x0000002bU)))) {
                                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__is_q_field_w) {
                                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r 
                                            = ((1U 
                                                == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r))
                                                ? 0U
                                                : 1U);
                                    }
                                } else {
                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r 
                                        = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r))
                                            ? 0U : 
                                           (0x0000000fU 
                                            & ((IData)(1U) 
                                               + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r))));
                                }
                            } else {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r = 0U;
                            }
                        } else if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                  >> 0x0000002dU)))) {
                            if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                               >> 0x0000002cU)))) {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r = 0U;
                            } else if ((1U & (IData)(
                                                     (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                      >> 0x0000002bU)))) {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r = 0U;
                            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__is_q_field_w) {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r 
                                    = ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r))
                                        ? 0U : 1U);
                            }
                        } else if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                  >> 0x0000002cU)))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r = 0U;
                        } else if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                  >> 0x0000002bU)))) {
                            if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxr_valid_r) 
                                 & (4U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r)))) {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r 
                                    = (0x0000000fU 
                                       & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r)));
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cursor_r 
                                    = (0x000003ffU 
                                       & ((IData)(4U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cursor_r)));
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r 
                                    = (0x000007ffU 
                                       & ((IData)(4U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r)));
                            } else if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r))) {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r = 0U;
                            }
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r = 0U;
                        }
                    } else if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                              >> 0x0000002eU)))) {
                        if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                           >> 0x0000002dU)))) {
                            if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                               >> 0x0000002cU)))) {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r = 0U;
                            } else if ((1U & (IData)(
                                                     (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                      >> 0x0000002bU)))) {
                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r = 0U;
                            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_go_r) {
                                if ((((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r)) 
                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_rvalid_w)) 
                                     & (0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_left_r)))) {
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_lane_r 
                                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_rdata_w;
                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r = 1U;
                                } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r))) {
                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cursor_r 
                                        = (0x000003ffU 
                                           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cursor_r) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_adv1_w)));
                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r 
                                        = (0x000007ffU 
                                           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_adv1_w)));
                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r = 2U;
                                } else if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r))) {
                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cursor_r 
                                        = (0x000003ffU 
                                           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cursor_r) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_adv2_w)));
                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r 
                                        = (0x000007ffU 
                                           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_adv2_w)));
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_left_r 
                                        = ((8U < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_left_r))
                                            ? (0x0000ffffU 
                                               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_left_r) 
                                                  - (IData)(8U)))
                                            : 0U);
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_idx_r 
                                        = (0x00001fffU 
                                           & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_idx_r)));
                                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_left_r 
                                    = (0x0000ffffU 
                                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r));
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_idx_r = 0U;
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_go_r = 1U;
                            }
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r = 0U;
                        }
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r = 0U;
                    }
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__advance_e_w) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_go_r = 0U;
                        if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                           >> 0x0000002fU)))) {
                            if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                               >> 0x0000002eU)))) {
                                if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                   >> 0x0000002dU)))) {
                                    if ((1U & (~ (IData)(
                                                         (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                          >> 0x0000002cU))))) {
                                        if ((1U & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                           >> 0x0000002bU)))) {
                                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_we_r = 1U;
                                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_rd_r 
                                                = (0x0000000fU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                              >> 0x00000027U)));
                                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_data_r 
                                                = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r 
                                                   >> 
                                                   (0x0000003fU 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r)));
                                        }
                                    }
                                }
                                if ((1U & (~ (IData)(
                                                     (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                      >> 0x0000002dU))))) {
                                    if ((1U & (IData)(
                                                      (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                       >> 0x0000002cU)))) {
                                        if ((1U & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                           >> 0x0000002bU)))) {
                                            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__append_skip_w) {
                                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ovf_r = 1U;
                                            } else {
                                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cursor_r 
                                                    = 
                                                    (0x000003ffU 
                                                     & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cursor_r) 
                                                        + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__fld_len_w)));
                                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r 
                                                    = 
                                                    (0x000007ffU 
                                                     & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r) 
                                                        + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__fld_len_w)));
                                            }
                                        }
                                    } else if ((1U 
                                                & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                           >> 0x0000002bU)))) {
                                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r 
                                            = (0x000007ffU 
                                               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r));
                                    } else {
                                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__status_r 
                                            = (0x0000001fU 
                                               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r));
                                    }
                                }
                            } else {
                                if ((1U & (~ (IData)(
                                                     (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                      >> 0x0000002dU))))) {
                                    if ((1U & (~ (IData)(
                                                         (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                          >> 0x0000002cU))))) {
                                        if ((1U & (~ (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                              >> 0x0000002bU))))) {
                                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_we_r = 1U;
                                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_rd_r 
                                                = (0x0000000fU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                              >> 0x00000027U)));
                                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_data_r 
                                                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxr_data_r;
                                        }
                                    }
                                }
                                if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                   >> 0x0000002dU)))) {
                                    if ((1U & (~ (IData)(
                                                         (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                          >> 0x0000002cU))))) {
                                        if ((1U & (~ (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                              >> 0x0000002bU))))) {
                                            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__append_skip_w) {
                                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ovf_r = 1U;
                                            } else {
                                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cursor_r 
                                                    = 
                                                    (0x000003ffU 
                                                     & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cursor_r) 
                                                        + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__fld_len_w)));
                                                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r 
                                                    = 
                                                    (0x000007ffU 
                                                     & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r) 
                                                        + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__fld_len_w)));
                                            }
                                        }
                                    }
                                } else if ((1U & (IData)(
                                                         (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                          >> 0x0000002cU)))) {
                                    if ((1U & (IData)(
                                                      (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                       >> 0x0000002bU)))) {
                                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__iter_idx_r 
                                            = (0x000000ffU 
                                               & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__iter_idx_r)));
                                    } else {
                                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__iter_cnt_r 
                                            = (0x000000ffU 
                                               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r));
                                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__iter_idx_r = 0U;
                                    }
                                }
                            }
                        } else if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                  >> 0x0000002eU)))) {
                            if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                  >> 0x0000002dU))))) {
                                if ((1U & (~ (IData)(
                                                     (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                      >> 0x0000002bU))))) {
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_we_r = 1U;
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_rd_r 
                                        = (0x0000000fU 
                                           & (IData)(
                                                     (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                      >> 0x00000027U)));
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_data_r 
                                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_rdata_w;
                                }
                            }
                            if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                               >> 0x0000002dU)))) {
                                if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                   >> 0x0000002cU)))) {
                                    if ((1U & (IData)(
                                                      (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                       >> 0x0000002bU)))) {
                                        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__br_taken_w) {
                                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__status_r = 7U;
                                        }
                                    } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__br_taken_w) {
                                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__status_r 
                                            = ((1U 
                                                & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                           >> 0x0000001bU)))
                                                ? 0x0bU
                                                : 7U);
                                    }
                                } else if ((1U & (IData)(
                                                         (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                          >> 0x0000002bU)))) {
                                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__br_taken_w) {
                                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__status_r = 3U;
                                    }
                                }
                            } else if ((1U & (~ (IData)(
                                                        (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                         >> 0x0000002cU))))) {
                                if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                   >> 0x0000002bU)))) {
                                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_err_w) {
                                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__status_r = 0x0aU;
                                    }
                                } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_err_w) {
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__status_r = 7U;
                                }
                            }
                        } else if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                  >> 0x0000002dU)))) {
                            if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                               >> 0x0000002cU)))) {
                                if ((1U & (~ (IData)(
                                                     (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                      >> 0x0000002bU))))) {
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_we_r = 1U;
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_rd_r 
                                        = (0x0000000fU 
                                           & (IData)(
                                                     (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                      >> 0x00000027U)));
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_data_r 
                                        = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r 
                                            & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opb_e_r) 
                                           | ((~ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opb_e_r) 
                                              & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opd_e_r));
                                }
                                if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                   >> 0x0000002bU)))) {
                                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_err_w) {
                                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__status_r = 2U;
                                    } else {
                                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__desc_base_r 
                                            = (0x000fffffU 
                                               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_rdata_w));
                                    }
                                }
                            } else {
                                if ((1U & (~ (IData)(
                                                     (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                      >> 0x0000002bU))))) {
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_we_r = 1U;
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_rd_r 
                                        = (0x0000000fU 
                                           & (IData)(
                                                     (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                      >> 0x00000027U)));
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_data_r 
                                        = ((0U == (0x0000000fU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                              >> 0x00000023U))))
                                            ? (QData)((IData)(
                                                              (0x00ffffffU 
                                                               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r))))
                                            : vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__a_fmt_w);
                                }
                                if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                   >> 0x0000002bU)))) {
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__z_r 
                                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cmp_z_w;
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__lt_r 
                                        = (1U & (IData)(
                                                        (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_113 
                                                         >> 0x00000020U)));
                                }
                            }
                        }
                        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__end_op_w) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ms_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_d_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_e_r = 0U;
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ucpu_done_w = 1U;
                        } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__br_taken_w) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__upc_r 
                                = (0x000007ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r));
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_d_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_e_r = 0U;
                        }
                    }
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ms_r = 5U;
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ms_r))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ms_r 
                = ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ms_r))
                    ? 4U : 3U);
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ms_r))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ms_r = 2U;
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_d_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_e_r = 0U;
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__disp_valid_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__upc_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r;
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cursor_r 
                        = (0x000003ffU & ((IData)(8U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_out_r)));
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r 
                        = (0x000003ffU & ((IData)(8U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_out_r)));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__iter_idx_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_left_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ms_r = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__status_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__z_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__lt_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ovf_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__batch_r = 1U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cursor_r = 0x0000000cU;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r = 0x000cU;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__iter_idx_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_left_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ms_r = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__status_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__z_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__lt_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ovf_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__batch_r = 0U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__iter_cnt_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r = 0U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_go_r = 0U;
            }
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__tone_ctrl 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.s_axi_awaddr) 
                                                     >> 7U)))) {
                                                if (
                                                    (0x00000040U 
                                                     & (IData)(vlSelfRef.s_axi_awaddr))) {
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs 
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
                                                                                = 
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__eth_guard)
                                                                                 ? 
                                                                                (0xfffffffdU 
                                                                                & vlSelfRef.s_axi_wdata)
                                                                                 : vlSelfRef.s_axi_wdata);
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
                                } else if ((1U & (~ 
                                                  ((IData)(vlSelfRef.s_axi_awaddr) 
                                                   >> 9U)))) {
                                    if ((0x00000100U 
                                         & (IData)(vlSelfRef.s_axi_awaddr))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.s_axi_awaddr) 
                                                    >> 7U)))) {
                                            if ((1U 
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
                                                                        if (
                                                                            (1U 
                                                                             & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__eth_guard)))) {
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__phy_rst 
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
                                                    (0x00000040U 
                                                     & (IData)(vlSelfRef.s_axi_awaddr))) {
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
                                                                            if (
                                                                                (1U 
                                                                                & vlSelfRef.s_axi_wdata)) {
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__ltap_clr_p = 1U;
                                                                            }
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__ltap_en_r 
                                                                                = 
                                                                                (1U 
                                                                                & (vlSelfRef.s_axi_wdata 
                                                                                >> 1U));
                                                                        }
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
                                                                                ((1U 
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
                                                                            ((1U 
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
                                                                        (1U 
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
                                                                            (1U 
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
                                                                        (1U 
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
                                                                        (1U 
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
                                                                    (1U 
                                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r))) {
                                                                    if (vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r) {
                                                                        if (
                                                                            (0U 
                                                                             == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r))) {
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
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
                                                                    vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
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
            if ((0x0920U != (IData)(vlSelfRef.s_axi_awaddr))) {
                if ((0x0934U == (IData)(vlSelfRef.s_axi_awaddr))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_sel_r 
                        = (0x0000003fU & vlSelfRef.s_axi_wdata);
                }
            }
        }
    } else {
        vlSelfRef.milan_datapath__DOT__avtprx_mr_bit = 0U;
        vlSelfRef.milan_datapath__DOT__link_guard__DOT__tx_armed_r = 0U;
        vlSelfRef.milan_datapath__DOT__tkd_crfq_r = 0U;
        vlSelfRef.milan_datapath__DOT__link_guard__DOT__rx_armed_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__cur_slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__cur_slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__cur_slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__cur_slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__tone_ctrl = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__tick_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__talker_diag__DOT__tick_p_r = 0U;
        vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__ptp_sync__DOT__snap_ret_s = 0U;
        vlSelfRef.milan_datapath__DOT__ptp_sync__DOT__tod_rd_reg = 0ULL;
        vlSelfRef.milan_datapath__DOT__ptp_sync__DOT__tod_rd_valid_reg = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__cur_slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_sid_frame = 0ULL;
        vlSelfRef.milan_datapath__DOT__avtprx_match = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_parse_p = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_subtype = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_idx = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_valid_w = 0U;
        VL_ASSIGN_W(1504, vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r, Vmilan_datapath__ConstPool__CONST_hbff50867_0);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_cancel_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_owner_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_deadline_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_pair_w = 0ULL;
        vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_sel_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_aecp_dyn_dirty_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__dirty_r = 0U;
        vlSelfRef.milan_datapath__DOT__src_recentre_q_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__media_grid_align__DOT__quiet_r = 0U;
        vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__tst_r = 0U;
        vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__ref_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__media_grid_align__DOT__slip_r = 0U;
        vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__engaged_r = 0U;
        vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__err_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__media_grid_align__DOT__acc_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__mnco_servo_trim_w = 0U;
        vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__rollover_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_txp_q_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__ltap_clr_p = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__ltap_en_r = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_rxp_q_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_la_mvrp_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r = 0U;
        vlSelfRef.milan_datapath__DOT__cmap_rd_valid_w = 0U;
        vlSelfRef.milan_datapath__DOT__cmap_rd_data_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_q2_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__iv_bytes_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r 
            = (0x0000ffffU & (0xace1U ^ ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w) 
                                         ^ (IData)(
                                                   (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                    >> 0x00000010U)))));
        vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__is_maap_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_msg_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_start_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_conf_start_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_conf_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_done_p = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ctrl_scratch_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_src_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_rel_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit_q = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux_q = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__shadow_qq = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux_q = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__rds_busy_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__rds_dir_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__rds_cyc_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__rds_word_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__rds_idx_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__strm_hit_q = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__rd_in_window_q = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__byte_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__done_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__err_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__was_write_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_valid_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_addr_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_data_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__op_region_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__op_mut_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__op_full_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_la_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__rnd_act_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__td_tk_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__td_ls_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_join_r = 0U;
        vlSelfRef.milan_datapath__DOT__tctx_rd_data_w = 0U;
        vlSelfRef.milan_datapath__DOT__tctx_rd_valid_w = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_q_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_fresh_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__declaring_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl = 0x00000010U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__fph_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__eiss_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__ecap_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__esmp_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__eo_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v1 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__est_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ebank_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eseq_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ets_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__etu_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__emr_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__edmac_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__euid_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__evid_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__tsw_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tsw_t_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tsw_val_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v1 = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_frames_w = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_frame_p_w = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_frame_idx_w = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_frame_tu_w = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_frame_mr_w = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v2 = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__gslope_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__alarm_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__over_acc_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__over_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__acc_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__sum_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__barrier_pend_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__miss_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__fetch_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rowr_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__cksum_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__key_type_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_rd_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_cmp_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_base_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_byte_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_load_lane_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__img_valid_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__fault_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_valid_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_addr_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_beats_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mem_busy_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_ix_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_b0_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_b0_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_config_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_entries_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_names_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_desc_max_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_index_off_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_names_off_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__key_cfg_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__key_index_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_len_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_nbase_r = 0xffffU;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_off_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_err_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_data_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_reg_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_pipe_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_kind_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_rdy_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_pend_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_kind_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_answer_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_name_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__disp_valid_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__resp_cnt_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__drop_cnt_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rerr_cnt_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 0U;
        VL_ASSIGN_W(393, vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r, Vmilan_datapath__ConstPool__CONST_hb995d365_0);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__raw_ct_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ty_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_ix_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_cfg_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cmd_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_rsp_count_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pid_lo_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ctrs_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_remove_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_uns_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__regun_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__acq_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__lockc_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gstri_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gavb_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gasp_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__eavl_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gcfg_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsfmt_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsrate_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gclks_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssrate_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sclks_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssfmt_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssinfo_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gctrl_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sctrl_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gname_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sname_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__scfg_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strt_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__stop_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strm_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setc_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__silat_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__opd2_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__lock_ent_ok_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__uns_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__status_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__frame_len_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__err_mode_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__tx_slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__opd0_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__opd1_r = 0ULL;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sent_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_started_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pending_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_load_data_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_wr_phase_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_total_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_start_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_next_pos_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_out_r = 0x000cU;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_rlen_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_end_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_len_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_cmd_hi_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_len_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_cmd_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_cmd_status_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_exec_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_status_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_shape_fault_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p1_d_r = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__stash_strm_r = 0U;
        vlSelfRef.milan_datapath__DOT__wing_sid_hi_r = 0U;
        vlSelfRef.milan_datapath__DOT__wing_sid_lo_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_vld_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_msg_type_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_status_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_cdl_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_src_mac_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_ctlr_eid_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_target_eid_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_seq_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_opcode_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_u_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_cr_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_operands_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_rx_slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_drop_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_bin_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__render_setpoint__DOT__sched_r = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__tick_q_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__render_setpoint__DOT__slot_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__render_setpoint__DOT__beat_r = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__tick_d_r = 0U;
        vlSelfRef.milan_datapath__DOT__rsp_pop_p_w = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ev_ok_r = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ev_row_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__phy_rst = 1U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__link_ctrl = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_taint_r = 0U;
        vlSelfRef.milan_datapath__DOT__speed_q = 2U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__aaf_tx_inframe_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__mac_rx_inframe_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_side_r = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_fed_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__frame_bytes_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_q1_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_base_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_len_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__laown_pend_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wtxla_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tick_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_code_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_fp_r = 0U;
        VL_ASSIGN_W(272, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r, Vmilan_datapath__ConstPool__CONST_hc5471b50_0);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_txop_done_w = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__laown_pend_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wtxla_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tick_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_code_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_type_r = 0U;
        VL_ASSIGN_W(272, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r, Vmilan_datapath__ConstPool__CONST_hc5471b50_0);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_txop_done_w = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rvalid_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lanewr_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__burst_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__bix_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wbusy_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rreq_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_d_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_s_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_ix_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_open_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__seal_pend_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__len_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__served_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rlane_r = 0ULL;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__roff_r = 4U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__fault_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__fcode_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__drop_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_valid_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wr_ready_r = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wreq_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rbusy_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__upc_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_d_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_e_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__iter_idx_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cursor_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_left_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_idx_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ms_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_we_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_rd_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_data_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__status_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__z_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__lt_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ovf_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__desc_base_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__iter_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__batch_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_go_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_lane_r = 0ULL;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rom_q_r = 0ULL;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r = 0ULL;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r = 0ULL;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opb_e_r = 0ULL;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opd_e_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ucpu_done_w = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl = 0x00020000U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_dmlo = 0xf000fe01U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_dmhi = 0x000091e0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_p_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_data_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_p_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_data_r = 0U;
    }
    vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__to_cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__to_cnt_r;
    vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__sel_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__sel_r;
    vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__locked_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__locked_r;
    vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__to_cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__crf_dp_mux__DOT__to_cnt_r;
    vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__sel_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__crf_dp_mux__DOT__sel_r;
    vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__locked_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__crf_dp_mux__DOT__locked_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__mem_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__mem_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__mem_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_idx_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_idx_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_st_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_st_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r[8U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r[9U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r[10U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r[11U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r[12U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r[13U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r[14U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r[15U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__alloc_wait_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__alloc_wait_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r__v0][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r__v0[0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r__v0][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r__v0[1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r__v0][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r__v0[2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r__v0][3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r__v0[3U];
    }
    vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w = 0U;
    milan_datapath__DOT__tdm_lane_streams__DOT__rword 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__rmap_flat_w[0U] 
                          >> 0x00000010U));
    if ((IData)((0x80U == (0xc0U & (IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword))))) {
        if ((0U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w = 1U;
        }
    }
    milan_datapath__DOT__tdm_lane_streams__DOT__rword 
        = (vlSelfRef.milan_datapath__DOT__rmap_flat_w[0U] 
           >> 0x00000018U);
    if ((IData)((0x80U == (0xc0U & (IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword))))) {
        if ((0U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w = 1U;
        }
    }
    milan_datapath__DOT__tdm_lane_streams__DOT__rword 
        = (0x000000ffU & vlSelfRef.milan_datapath__DOT__rmap_flat_w[1U]);
    if ((IData)((0x80U == (0xc0U & (IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword))))) {
        if ((0U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w = 1U;
        }
    }
    milan_datapath__DOT__tdm_lane_streams__DOT__rword 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__rmap_flat_w[1U] 
                          >> 8U));
    if ((IData)((0x80U == (0xc0U & (IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword))))) {
        if ((0U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w = 1U;
        }
    }
    milan_datapath__DOT__tdm_lane_streams__DOT__rword 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__rmap_flat_w[1U] 
                          >> 0x00000010U));
    if ((IData)((0x80U == (0xc0U & (IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword))))) {
        if ((0U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w = 1U;
        }
    }
    milan_datapath__DOT__tdm_lane_streams__DOT__rword 
        = (vlSelfRef.milan_datapath__DOT__rmap_flat_w[1U] 
           >> 0x00000018U);
    if ((IData)((0x80U == (0xc0U & (IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword))))) {
        if ((0U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w = 1U;
        }
    }
    milan_datapath__DOT__tdm_lane_streams__DOT__rword 
        = (0x000000ffU & vlSelfRef.milan_datapath__DOT__rmap_flat_w[2U]);
    if ((IData)((0x80U == (0xc0U & (IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword))))) {
        if ((0U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w = 1U;
        }
    }
    milan_datapath__DOT__tdm_lane_streams__DOT__rword 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__rmap_flat_w[2U] 
                          >> 8U));
    if ((IData)((0x80U == (0xc0U & (IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword))))) {
        if ((0U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w = 1U;
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_req_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_req_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U] = 3U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v2) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v3) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v4) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U] = 2U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v5) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v6) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v7) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v8) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v9) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__cap_vld_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__cap_vld_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_valid_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_valid_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_valid_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_slot_w = 0U;
    if ((1U & (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__free_mask_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_slot_w = 0U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
               & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__free_mask_w) 
                  >> 1U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_slot_w = 1U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
               & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__free_mask_w) 
                  >> 2U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_slot_w = 2U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
         & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__free_mask_w) 
            >> 3U))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_slot_w = 3U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_valid_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_slot_w = 0U;
    if ((1U & (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__free_mask_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_slot_w = 0U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
               & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__free_mask_w) 
                  >> 1U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_slot_w = 1U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
               & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__free_mask_w) 
                  >> 2U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_slot_w = 2U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
         & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__free_mask_w) 
            >> 3U))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_slot_w = 3U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_valid_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_slot_w = 0U;
    if ((1U & (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__free_mask_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_slot_w = 0U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
               & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__free_mask_w) 
                  >> 1U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_slot_w = 1U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
               & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__free_mask_w) 
                  >> 2U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_slot_w = 2U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
         & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__free_mask_w) 
            >> 3U))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_slot_w = 3U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_valid_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_slot_w = 0U;
    if ((1U & (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__free_mask_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_slot_w = 0U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
               & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__free_mask_w) 
                  >> 1U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_slot_w = 1U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
               & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__free_mask_w) 
                  >> 2U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_slot_w = 2U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
         & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__free_mask_w) 
            >> 3U))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_slot_w = 3U;
    }
    vlSelfRef.milan_datapath__DOT__talker_diag__DOT__tick_cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__tick_cnt_r;
    vlSelfRef.milan_datapath__DOT__ptp_sync__DOT__snap_ret_s 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_sync__DOT__snap_ret_s;
    __Vilp1 = 0U;
    while ((__Vilp1 <= 0x0000002eU)) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[__Vilp1] 
            = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r
            [__Vilp1];
        __Vilp1 = ((IData)(1U) + __Vilp1);
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r;
    vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_ren_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_ren_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__rd_en_w 
        = ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__cnt_r)) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_valid_r)) 
              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__maap_txn_ready_w)));
    vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__quiet_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__media_grid_align__DOT__quiet_r;
    vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__acc_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__media_grid_align__DOT__acc_r;
    vlSelfRef.milan_datapath__DOT__mnco_servo_trim_w 
        = vlSelfRef.__Vdly__milan_datapath__DOT__mnco_servo_trim_w;
    vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__slip_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__media_grid_align__DOT__slip_r;
    vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__counters[0U] 
        = vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__0__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__counters[1U] 
        = vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__1__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__counters[2U] 
        = vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__2__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__counters[3U] 
        = vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__3__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__counters[4U] 
        = vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__4__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__counters[5U] 
        = vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__5__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__counters[6U] 
        = vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__6__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__counters[7U] 
        = vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__7__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__counters[8U] 
        = vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__8__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__aafcap_pv_w = vlSelfRef.__Vdly__milan_datapath__DOT__aafcap_pv_w;
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w 
        = (0x0000ffffU & (milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__diff_w 
                          | (- (IData)((0U != (milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__diff_w 
                                               >> 0x00000010U))))));
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w 
        = (0x0000ffffU & (milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__diff_w 
                          | (- (IData)((0U != (milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__diff_w 
                                               >> 0x00000010U))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_266 = (7U 
                                                  & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
                                                      >> 3U) 
                                                     - 
                                                     (1U 
                                                      & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_285))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_283 = (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_285) 
                                                   << 1U) 
                                                  | (0U 
                                                     != 
                                                     (7U 
                                                      & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__scan_ix_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__scan_ix_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ridx_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ridx_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vlan_user_valid_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vu_sel_ls_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w)) 
              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vrr_r)));
    vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_busy_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__cmrd_busy_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__map_r__v0) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__map_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__map_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__map_r__v1) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[7U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r;
    vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__is_maap_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__is_maap_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_data_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_data_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r__v1] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r__v2) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r[7U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r;
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_89 = (0U 
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_235 = ((1ULL 
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__td_tk_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__td_tk_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__td_ls_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__td_ls_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__rnd_act_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__rnd_act_r;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_q_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_q_r;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__stg_q_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__stg_q_r;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eiss_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__eiss_r;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eo_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__eo_r;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ecap_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__ecap_r;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tsw_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__tsw_pend_r;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__fph_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__wbank_r[0U] 
            = __VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v1) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__wbank_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v1) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r[0U] 
            = __VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v0] 
            = __VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v2) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r__v0] 
            = __VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v1) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v2) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[8U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[9U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[10U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[11U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[12U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[13U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[14U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[15U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[16U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[17U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[18U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[19U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[20U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[21U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[22U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[23U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v1) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v2) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[8U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[9U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[10U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[11U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[12U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[13U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[14U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[15U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[16U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[17U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[18U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[19U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[20U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[21U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[22U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[23U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__pend_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r[__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__pend_r__v0] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r[0U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v2) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v1) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r[0U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__est_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__over_acc_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__over_acc_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__acc_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__acc_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__miss_cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__miss_cnt_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_pend_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_kind_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_kind_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_len_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_len_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_beats_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_beats_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_valid_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_valid_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_load_lane_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_load_lane_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_ix_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_ix_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_nbase_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_nbase_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mem_busy_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mem_busy_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__key_type_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__key_type_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_load_data_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_load_data_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__acq_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__acq_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gcfg_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gcfg_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssrate_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssrate_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sclks_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sclks_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sctrl_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sctrl_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cmd_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cmd_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rerr_cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rerr_cnt_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_end_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_end_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__drop_cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__drop_cnt_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_cfg_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_cfg_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_ix_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_ix_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sent_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sent_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_rlen_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_rlen_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ctrs_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ctrs_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsrate_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsrate_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gclks_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gclks_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gctrl_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gctrl_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setc_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setc_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__frame_len_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__frame_len_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gname_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gname_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__eavl_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__eavl_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__regun_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__regun_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gasp_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gasp_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__lockc_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__lockc_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__scfg_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__scfg_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gstri_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gstri_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gavb_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gavb_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsfmt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsfmt_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssfmt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssfmt_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssinfo_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssinfo_r;
    vlSelfRef.milan_datapath__DOT__csr__DOT__sweep_wr 
        = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__sweep_busy) 
           & ((1U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__sweep_cnt)) 
              & (0x0200U >= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__sweep_cnt))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__v_mrp_last_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__od_last_r) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__v_mrp_valid_w));
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__rd_fire_w) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__od_data_r 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mrp_mem_r
               [(0x0000003fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__rptr_r))]);
    }
    vlSelfRef.milan_datapath__DOT__render_recentre_p_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_adj_p) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_load_p) 
              | ((IData)(vlSelfRef.milan_datapath__DOT__gm_recentre_p_r) 
                 | (IData)(vlSelfRef.milan_datapath__DOT__src_recentre_p_r))));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[0U]) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
              < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[1U]));
    __VdfgRegularize_h6e95ff9d_0_295 = (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_primed_r) 
                                         >> (3U & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r))) 
                                        & ((1U == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__st_r)) 
                                           & (4U > (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_take_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pick_vld_w) 
           & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r)));
    vlSelfRef.milan_datapath__DOT__pp_cd_adp_avail_index_w 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r[0U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_done_avail_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_dep_r)) 
           & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_v_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_ix_w = 0U;
    if ((0U != (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_ix_w = 0U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_v_w)) 
         & (0U != (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r) 
                         >> 2U))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_ix_w = 1U;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_241 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w) 
                                                  | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_187 = ((
                                                   (2U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r))
                                                    ? 2U
                                                    : 1U) 
                                                  & (- (IData)(
                                                               (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r) 
                                                                 >> 1U) 
                                                                & (0U 
                                                                   != 
                                                                   (3U 
                                                                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r) 
                                                                       >> 2U)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_49 = (((1U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r))
                                                   ? 2U
                                                   : 1U) 
                                                 & (- (IData)(
                                                              ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r) 
                                                               & (0U 
                                                                  != 
                                                                  (3U 
                                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_v_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_ix_w = 0U;
    if ((0U != (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_ix_w = 0U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_v_w)) 
         & (0U != (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r) 
                         >> 2U))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_ix_w = 1U;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_30 = (3U 
                                                 & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r) 
                                                     >> 2U) 
                                                    & (- (IData)(
                                                                 (0U 
                                                                  != 
                                                                  (3U 
                                                                   & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r) 
                                                                      >> 2U)))))));
    vlSelfRef.milan_datapath__DOT__lwsrp_listener_decl 
        = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r) 
                 & (- (IData)((0U != (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r)))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__request_w = 0U;
    if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_release_valid_w) 
         & (5U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_release_slot_w)))) {
        if ((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_release_slot_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__request_w 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__request_w) 
                   | (0x1fU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_release_slot_w))));
        }
    }
    if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_cancel_release_valid_w) 
         & (5U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_cancel_release_slot_w)))) {
        if ((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_cancel_release_slot_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__request_w 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__request_w) 
                   | (0x1fU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_cancel_release_slot_w))));
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_need_kind_w 
        = ((1U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U])
            ? ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_startup_r)
                ? 1U : 2U) : 2U);
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_have_slot_w 
        = ((7U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_slot_r)) 
           & (4U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_slot_r)));
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__rd_en_w) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[0U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__rd_ptr_r][0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[1U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__rd_ptr_r][1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[2U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__rd_ptr_r][2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[3U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__rd_ptr_r][3U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[4U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__rd_ptr_r][4U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[5U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__rd_ptr_r][5U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[6U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__rd_ptr_r][6U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[7U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__rd_ptr_r][7U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[8U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__rd_ptr_r][8U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[9U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__rd_ptr_r][9U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[10U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__rd_ptr_r][10U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[11U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__rd_ptr_r][11U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[12U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__rd_ptr_r][12U];
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_dom_ok_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_dom_r)) 
           & (0ULL == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_gm_r));
    if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxp_rd_data_w__BRA__7__03a0__KET__ 
            = ((0x08ffU >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__rd_maddr_w))
                ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__mem_r
               [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__rd_maddr_w]
                : 0U);
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_210 = (IData)(
                                                         ((0x00000014U 
                                                           == 
                                                           (0x0000001cU 
                                                            & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[11U])) 
                                                          & (2U 
                                                             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__cnt_r))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_211 = (IData)(
                                                         ((4U 
                                                           == 
                                                           (0x0000001cU 
                                                            & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[11U])) 
                                                          & (4U 
                                                             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__cnt_r))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_212 = (IData)(
                                                         ((0U 
                                                           == 
                                                           (0x0000001cU 
                                                            & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[11U])) 
                                                          & (4U 
                                                             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__cnt_r))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_213 = ((0U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[11U] 
                                                       >> 2U))) 
                                                  | ((1U 
                                                      == 
                                                      (7U 
                                                       & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[11U] 
                                                          >> 2U))) 
                                                     | (5U 
                                                        == 
                                                        (7U 
                                                         & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[11U] 
                                                            >> 2U)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_maddr_w 
        = (0x00000fffU & (((IData)(0x0240U) * (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__cur_slot_r)) 
                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_ptr_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_maddr_w 
        = (0x00000fffU & (((IData)(0x0240U) * (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__cur_slot_r)) 
                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_ptr_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_maddr_w 
        = (0x00000fffU & (((IData)(0x0240U) * (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__cur_slot_r)) 
                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_ptr_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_maddr_w 
        = (0x00000fffU & (((IData)(0x0240U) * (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__cur_slot_r)) 
                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_ptr_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_maddr_w 
        = (0x00000fffU & (((IData)(0x0240U) * (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__cur_slot_r)) 
                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_ptr_r)));
    vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_rempty_w 
        = ((1U & (~ (IData)(vlSelfRef.axis_resetn))) 
           || ((IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_gray_n) 
               == (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wgray_r2_r)));
    vlSelfRef.milan_datapath__DOT__mga_engaged_w = vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__engaged_r;
    vlSelfRef.milan_datapath__DOT__mga_err_w = vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__err_r;
    vlSelfRef.milan_datapath__DOT__crf_clk_selected_r 
        = ((IData)(vlSelfRef.axis_resetn) && (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_aecp_clk_src_index_w)));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_pair_valid_i 
        = vlSelfRef.milan_datapath__DOT__aafcap_pv_w;
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_frame_ev_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__aafcap_pv_w) 
           & (0ULL == (0x000f000000000000ULL & vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_pair_w)));
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w = 0U;
    milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run0_v = 1U;
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_txp_q_r))) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w 
            = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w)));
    } else {
        milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run0_v = 0U;
    }
    if (milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run0_v) {
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_txp_q_r))) {
            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w)));
        } else {
            milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run0_v = 0U;
        }
    }
    if (milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run0_v) {
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_txp_q_r))) {
            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w)));
        } else {
            milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run0_v = 0U;
        }
    }
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w = 0U;
    milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run_v = 1U;
    if ((1U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_txp_q_r))) {
            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w)));
        } else {
            milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run_v = 0U;
        }
    }
    if (((2U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r)) 
         & (IData)(milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run_v))) {
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_txp_q_r))) {
            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w)));
        } else {
            milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run_v = 0U;
        }
    }
    if (milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run_v) {
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_txp_q_r))) {
            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w)));
        } else {
            milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run_v = 0U;
        }
    }
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w = 0U;
    milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run0_v = 1U;
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_rxp_q_r))) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w 
            = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w)));
    } else {
        milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run0_v = 0U;
    }
    if (milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run0_v) {
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_rxp_q_r))) {
            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w)));
        } else {
            milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run0_v = 0U;
        }
    }
    if (milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run0_v) {
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_rxp_q_r))) {
            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w)));
        } else {
            milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run0_v = 0U;
        }
    }
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w = 0U;
    milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run_v = 1U;
    if ((1U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_rxp_q_r))) {
            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w)));
        } else {
            milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run_v = 0U;
        }
    }
    if (((2U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r)) 
         & (IData)(milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run_v))) {
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_rxp_q_r))) {
            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w)));
        } else {
            milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run_v = 0U;
        }
    }
    if (milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run_v) {
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_rxp_q_r))) {
            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w)));
        } else {
            milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run_v = 0U;
        }
    }
    __VdfgRegularize_h6e95ff9d_0_284 = ((0U != (7U 
                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
                                                   >> 6U))) 
                                        & (0U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_283)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_we_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_wdat_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_wix_w = 0U;
    if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r))) {
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__op_join_r) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_v_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_we_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_wdat_w 
                = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__op_vid_r) 
                    << 5U) | ((0x1fU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_cnt_r))
                               ? 0x0000001fU : (0x0000001fU 
                                                & ((IData)(1U) 
                                                   + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_cnt_r)))));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_wix_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_ix_r;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__op_join_r) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__free_v_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_we_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_wdat_w 
                = (1U | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__op_vid_r) 
                         << 5U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_wix_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__free_ix_r;
        } else if ((((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__op_join_r)) 
                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_v_r)) 
                    & (1U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_cnt_r)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_we_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_wdat_w 
                = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__op_vid_r) 
                    << 5U) | (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_cnt_r) 
                                             - (IData)(1U))));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_wix_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_ix_r;
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vlan_ev_valid_w 
        = ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r)) 
           | (7U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_ready_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vu_sel_ls_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_ready_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r)) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vu_sel_ls_w)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w)));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 0U;
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[0U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[0U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[1U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[1U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[2U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[2U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[3U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[3U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[4U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[4U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[5U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[5U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[6U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[6U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[7U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[7U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    __VdfgRegularize_h6e95ff9d_0_51 = (7U & ((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                              [(1U 
                                                | ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                   << 1U))] 
                                              >> 8U) 
                                             & (- (IData)(
                                                          (1U 
                                                           & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                                              [
                                                              (1U 
                                                               | ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                                  << 1U))] 
                                                              >> 0x0000000cU))))));
    __VdfgRegularize_h6e95ff9d_0_52 = (7U & ((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                              [((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                << 1U)] 
                                              >> 8U) 
                                             & (- (IData)(
                                                          (1U 
                                                           & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                                              [
                                                              ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                               << 1U)] 
                                                              >> 0x0000000cU))))));
    __VdfgRegularize_h6e95ff9d_0_179 = (4U > (0x0000000fU 
                                              & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                              [((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                << 1U)]));
    __VdfgRegularize_h6e95ff9d_0_182 = (4U > (0x0000000fU 
                                              & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                              [(1U 
                                                | ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                   << 1U))]));
    __VdfgRegularize_h6e95ff9d_0_185 = (3U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                        [(1U | ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                << 1U))]);
    __VdfgRegularize_h6e95ff9d_0_186 = (3U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                        [((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                          << 1U)]);
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[0U] 
        = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[2U])) 
                    << 0x0000001aU) | (QData)((IData)(
                                                      (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[1U]) 
                                                        << 0x0000000dU) 
                                                       | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[0U])))));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[1U] 
        = ((0xffffff80U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[1U]) 
           | (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[2U])) 
                        << 0x0000001aU) | (QData)((IData)(
                                                          (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[1U]) 
                                                            << 0x0000000dU) 
                                                           | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[0U])))) 
                      >> 0x00000020U)));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[1U] 
        = ((0x0000007fU & vlSelfRef.milan_datapath__DOT__cmap_flat_w[1U]) 
           | ((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[5U])) 
                        << 0x0000001aU) | (QData)((IData)(
                                                          (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[4U]) 
                                                            << 0x0000000dU) 
                                                           | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[3U]))))) 
              << 7U));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[2U] 
        = ((0xffffc000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[2U]) 
           | (((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[5U])) 
                         << 0x0000001aU) | (QData)((IData)(
                                                           (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[4U]) 
                                                             << 0x0000000dU) 
                                                            | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[3U]))))) 
               >> 0x00000019U) | ((IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[5U])) 
                                             << 0x0000001aU) 
                                            | (QData)((IData)(
                                                              (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[4U]) 
                                                                << 0x0000000dU) 
                                                               | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[3U])))) 
                                           >> 0x00000020U)) 
                                  << 7U)));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[2U] 
        = ((0x00003fffU & vlSelfRef.milan_datapath__DOT__cmap_flat_w[2U]) 
           | ((((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[7U]) 
                << 0x0000000dU) | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[6U]) 
              << 0x0000000eU));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[3U] 
        = (0x000000ffU & ((((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[7U]) 
                            << 0x0000000dU) | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[6U]) 
                          >> 0x00000012U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p1_l_r 
        = ((IData)(vlSelfRef.axis_resetn) && ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__wr_en_w) 
                                              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cdl_known_r) 
                                                 & ((0x00000fffU 
                                                     & ((IData)(0x000bU) 
                                                        + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cdl_r))) 
                                                    == 
                                                    (0x000007ffU 
                                                     & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r) 
                                                        - (IData)(0x000eU)))))));
    vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_next_w 
        = ((0x0000fffeU & ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r) 
                           << 1U)) | (1U & VL_REDXOR_16(
                                                        (0xd008U 
                                                         & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r)))));
    vlSelfRef.milan_datapath__DOT__csr__DOT__shadow_q 
        = vlSelfRef.milan_datapath__DOT__csr__DOT__shadow_ram
        [(0x000001ffU & ((IData)(vlSelfRef.s_axi_araddr) 
                         >> 2U))];
    milan_datapath__DOT__csr_tctx_rd_addr_w = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_170)
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
    vlSelfRef.milan_datapath__DOT__csr__DOT__rd_pend 
        = ((IData)(vlSelfRef.axis_resetn) && ((IData)(vlSelfRef.s_axi_arready) 
                                              & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_is_slow_w))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_close_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__done_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__op_mut_r) 
              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__was_write_r) 
                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__op_full_r))));
    vlSelfRef.o_nvm_mem_wr_strb = (0x000000ffU & ((IData)(1U) 
                                                  << 
                                                  (7U 
                                                   & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r)));
    vlSelfRef.o_nvm_mem_req_addr = (0xfffffff8U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r);
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_hit_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_valid_r) 
           & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_addr_r 
              == (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r 
                  >> 3U)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_plen_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r[4U]) 
            << 8U) | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r[5U]);
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w = 0U;
    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w = 0x000aU;
    } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w = 0x0000000aU;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w = 0x0010U;
    } else if (((2U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (3U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((IData)(0x0000001aU) 
                              + ((IData)(0x0000000cU) 
                                 * (0x0003ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r) 
                                                   - (IData)(2U))))));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w = 0x000cU;
    } else if (((0x0aU <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0x0bU > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((IData)(0x00000026U) 
                              + ((IData)(0x0000000aU) 
                                 * (0x0003ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r) 
                                                   - (IData)(0x0000000aU))))));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w = 0x000aU;
    } else if (((0x12U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0x13U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((IData)(0x00000030U) 
                              + ((IData)(0x0000004aU) 
                                 * (0x0003ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r) 
                                                   - (IData)(0x00000012U))))));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w = 0x004aU;
    } else if (((0x20U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0x22U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((IData)(0x0000007aU) 
                              + ((IData)(0x0000001cU) 
                                 * (0x0003ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r) 
                                                   - (IData)(0x00000020U))))));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w = 0x001cU;
    } else if (((0x30U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0x32U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((IData)(0x000000b2U) 
                              + (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r) 
                                  - (IData)(0x00000030U)) 
                                 << 4U)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w = 0x0010U;
    } else if (((0x40U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0x42U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((IData)(0x000000d2U) 
                              + (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r) 
                                  - (IData)(0x00000040U)) 
                                 << 4U)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w = 0x0010U;
    } else if (((0x50U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0x52U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((IData)(0x000000f2U) 
                              + ((IData)(0x0000000cU) 
                                 * (0x0003ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r) 
                                                   - (IData)(0x00000050U))))));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w = 0x000cU;
    } else if (((0x60U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0x61U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((IData)(0x0000010aU) 
                              + ((0U >= (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))
                                  ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_pref_r
                                 [(1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r))]
                                  : 0U)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w 
            = ((0U >= (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))
                ? (0x00000fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_len_r
                   [(1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r))])
                : 0U);
    } else if (((0x70U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0x71U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__b_mapo_w 
                              + ((0U >= (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))
                                  ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r
                                 [(1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r))]
                                  : 0U)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w 
            = ((0U >= (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))
                ? (0x00000fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r
                   [(1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r))])
                : 0U);
    } else if (((0x80U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0xa6U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__b_mapo_w 
                               + (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r[0U] 
                                  + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r[0U])) 
                              + ((IData)(0x00000048U) 
                                 * (0x0003ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r) 
                                                   - (IData)(0x00000080U))))));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w = 0x0048U;
    }
    vlSelfRef.o_nvm_mem_rsp_ready = (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r));
    vlSelfRef.o_nvm_mem_wr_valid = ((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r)) 
                                    | (9U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r)));
    vlSelfRef.o_nvm_mem_wr_data = ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__byte_r)) 
                                     << 0x00000038U) 
                                    | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__byte_r)) 
                                        << 0x00000030U) 
                                       | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__byte_r)) 
                                           << 0x00000028U) 
                                          | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__byte_r)) 
                                              << 0x00000020U) 
                                             | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__byte_r)) 
                                                 << 0x00000018U) 
                                                | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__byte_r)) 
                                                    << 0x00000010U) 
                                                   | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__byte_r)) 
                                                       << 8U) 
                                                      | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__byte_r))))))))) 
                                   | (- (QData)((IData)(
                                                        (9U 
                                                         == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_rdata_w 
        = (0x000000ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__byte_r) 
                          | (- (IData)((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_237 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_join_r) 
                                                  | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__join_pend_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__hw_full_q_r 
        = ((IData)(vlSelfRef.axis_resetn) && (0x0cU 
                                              == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_msrp_r)));
    vlSelfRef.milan_datapath__DOT__pp_cd_acmp_declaring_w 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__declaring_r;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_q_r 
        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tctx_r
        [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w];
    vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i 
        = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_p_w)
            ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_idx_w)
            : 1U);
    vlSelfRef.milan_datapath__DOT__tkd_crf_p_w = ((~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_p_w)) 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__tkd_crf_pend_r));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w 
        = (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r
           [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r] 
           & (- (IData)((0U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r)))));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w 
        = (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_170) 
            | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_busy_r) 
               & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_dir_r))) 
           & ((3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)) 
              | ((~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r[0U])) 
                 & (0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__len_lanes_w 
        = (0x00001fffU & (((IData)(7U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_len_r)) 
                          >> 3U));
    vlSelfRef.o_desc_mem_req_addr = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_addr_r;
    vlSelfRef.o_desc_mem_req_beats = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_beats_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rel_w 
        = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__key_index_r) 
                          - (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_base_r)));
    vlSelfRef.o_desc_mem_req_valid = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_valid_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__accept_w 
        = ((IData)(vlSelfRef.i_desc_mem_req_ready) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_valid_r));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_111 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__img_valid_r) 
                                                  & (0xffffU 
                                                     != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_nbase_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__last_w 
        = ((0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_cmp_r))) 
           >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_entries_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_w 
        = ((IData)(vlSelfRef.i_desc_mem_rsp_valid) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mem_busy_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_total_lanes_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_names_r) 
           << 3U);
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_lanes_left_w 
        = (0x000fffffU & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_names_r) 
                           << 3U) - vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_load_lane_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_ok_w = 0U;
    if ((0x41454d49U == (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_b0_r 
                                 >> 0x20U)))) {
        if ((1U == (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_b0_r 
                                           >> 0x10U))))) {
            if ((0xffffffffU == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__cksum_r)) {
                if ((1U & (~ (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_entries_r)) 
                               | (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_config_r))) 
                              | (0x0020U < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_entries_r)))))) {
                    if ((0x0026U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_names_r))) {
                        if ((1U & (~ ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_desc_max_r)) 
                                      | (0x0240U < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_desc_max_r)))))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_ok_w = 1U;
                        }
                    }
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_fault_w = 0U;
    if ((0x41454d49U != (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_b0_r 
                                 >> 0x20U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_fault_w = 1U;
    } else if ((1U != (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_b0_r 
                                              >> 0x10U))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_fault_w = 2U;
    } else if ((0xffffffffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__cksum_r)) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_fault_w = 3U;
    } else if ((((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_entries_r)) 
                 | (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_config_r))) 
                | (0x0020U < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_entries_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_fault_w = 4U;
    } else if ((0x0026U < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_names_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_fault_w = 5U;
    } else if (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_desc_max_r)) 
                | (0x0240U < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_desc_max_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_fault_w = 6U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_q_r 
        = ((0x47U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_raddr_w))
            ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_r
           [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_raddr_w]
            : 0ULL);
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_abs_byte_w 
        = (0x0000ffffU & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__key_type_r))
                            ? ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_name_r)
                                ? 0x00b4U : 0x0030U)
                            : 4U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_byte_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_q_r[0U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r
        [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_rd_r][0U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_q_r[1U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r
        [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_rd_r][1U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_q_r[2U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r
        [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_rd_r][2U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_q_r[3U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r
        [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_rd_r][3U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_q_r 
        = ((0x012fU >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_raddr_w))
            ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r
           [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_raddr_w]
            : 0ULL);
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_112 = ((0x0bU 
                                                   == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r)) 
                                                  | (0x0cU 
                                                     == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__store_rvalid_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_pend_r) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_pipe_r)) 
              & (0x0dU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__store_ready_w 
        = ((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r)) 
           | (7U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_pld_w 
        = (0x000007ffU & ((IData)(8U) + ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_rsp_count_r) 
                                         << 3U)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_41 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__regun_r) 
                                                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__lockc_r));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_207 = (0x0000ffffU 
                                                  & (- (IData)(
                                                               (1U 
                                                                & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__scfg_r))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_205 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssfmt_r) 
                                                  | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssinfo_r));
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__rd_en_w) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[0U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__rd_ptr_r][0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[1U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__rd_ptr_r][1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[2U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__rd_ptr_r][2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__rd_ptr_r][3U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__rd_ptr_r][4U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[5U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__rd_ptr_r][5U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[6U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__rd_ptr_r][6U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[7U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__rd_ptr_r][7U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[8U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__rd_ptr_r][8U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[9U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__rd_ptr_r][9U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[10U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__rd_ptr_r][10U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[11U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__rd_ptr_r][11U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[12U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__rd_ptr_r][12U];
    }
    if ((((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r)) 
          & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r) 
             & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_r)) 
                & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_uns_r)) 
                   & ((0x0026U <= (0x000007ffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r)))) 
                      & ((0x000007ffU & ((IData)(1U) 
                                         + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))) 
                         < (0x000007ffU & ((IData)(0x0026U) 
                                           + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r))))))))) 
         | (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r)) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                < (0x000007ffU & ((IData)(2U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r))))) 
            | (((9U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r)) 
                & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_started_r) 
                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_203))) 
               | (((0x0dU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r)) 
                   & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pending_r)) 
                      & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r) 
                         < (0x000007ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_len_r))))) 
                  | ((0x0aU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r)) 
                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_203))))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o 
            = ((0x08ffU >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__rd_maddr_w))
                ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__mem_r
               [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__rd_maddr_w]
                : 0U);
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mrp_mem_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mrp_mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mrp_mem_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mrp_mem_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__rptr_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__rptr_r;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w 
        = (3U & (((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
                  - vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[0U]) 
                 & (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w)))));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__dup_sum_w 
        = (0x0001ffffU & (((IData)(__VdfgRegularize_h6e95ff9d_0_295) 
                           & (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r) 
                               >> (3U & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r))) 
                              & (0U == vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r
                                 [(3U & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r))]))) 
                          + (IData)(vlSelfRef.milan_datapath__DOT__lb_dup_cnt_w)));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_act_w 
        = ((0U != vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r
            [(3U & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r))]) 
           & (IData)(__VdfgRegularize_h6e95ff9d_0_295));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_tk_reg_state_w 
        = (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_187) 
            << 2U) | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_49));
    vlSelfRef.milan_datapath__DOT__lwsrp_ta_fail_code 
        = (0x000000ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r) 
                          & (- (IData)((2U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_49))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w 
        = (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_30) 
            << 2U) | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_decl));
    vlSelfRef.milan_datapath__DOT__lwsrp_listener_ready 
        = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_decl)) 
           | (3U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_decl)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__request_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__pending_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__rd_ptr_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__rd_ptr_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0][3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[3U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0][4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[4U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0][5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[5U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0][6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[6U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0][7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[7U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0][8U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[8U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0][9U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[9U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0][10U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[10U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0][11U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[11U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0][12U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[12U];
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__rd_maddr_w 
        = (0x00000fffU & (((IData)(0x0240U) * (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_slot_r))) 
                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rd_ptr_r)));
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__mem_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__mem_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__mem_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__push_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_valid_r) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_210));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__push_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_valid_r) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_211));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__push_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_valid_r) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_212));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_260 = (1U 
                                                  & (~ 
                                                     ((4U 
                                                       == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__cnt_r)) 
                                                      | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_213))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_vld_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_vld_r;
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__sched_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__render_setpoint__DOT__sched_r;
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__beat_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__render_setpoint__DOT__beat_r;
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__render_setpoint__DOT__slot_r;
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_267 = (7U 
                                                  & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
                                                      >> 6U) 
                                                     - 
                                                     (1U 
                                                      & (- (IData)((IData)(__VdfgRegularize_h6e95ff9d_0_284))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_281 = (((IData)(__VdfgRegularize_h6e95ff9d_0_284) 
                                                   << 2U) 
                                                  | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_283));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_183 = (0x0000ffffffffffffULL 
                                                  & ((4U 
                                                      & (IData)(__VdfgRegularize_h6e95ff9d_0_51))
                                                      ? 
                                                     (((1U 
                                                        & (IData)(__VdfgRegularize_h6e95ff9d_0_51))
                                                        ? 
                                                       (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r
                                                        [__VdfgRegularize_h6e95ff9d_0_185] 
                                                        & (- (QData)((IData)(
                                                                             ((1U 
                                                                               > 
                                                                               (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                                                                [
                                                                                (1U 
                                                                                | ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                                                << 1U))] 
                                                                                >> 4U))) 
                                                                              & (IData)(__VdfgRegularize_h6e95ff9d_0_182))))))
                                                        : 
                                                       (((QData)((IData)(vlSelfRef.milan_datapath__DOT__tone_smp_media)) 
                                                         << 0x00000018U) 
                                                        | (QData)((IData)(vlSelfRef.milan_datapath__DOT__tone_smp_media)))) 
                                                      & (- (QData)((IData)(
                                                                           (1U 
                                                                            & (~ 
                                                                               ((IData)(__VdfgRegularize_h6e95ff9d_0_51) 
                                                                                >> 1U)))))))
                                                      : 
                                                     ((2U 
                                                       & (IData)(__VdfgRegularize_h6e95ff9d_0_51))
                                                       ? 
                                                      (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r
                                                       [__VdfgRegularize_h6e95ff9d_0_185] 
                                                       & (- (QData)((IData)(
                                                                            ((~ (IData)(__VdfgRegularize_h6e95ff9d_0_51)) 
                                                                             & (IData)(__VdfgRegularize_h6e95ff9d_0_182))))))
                                                       : 
                                                      (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__i2s_hold_r 
                                                       & (- (QData)((IData)(
                                                                            (1U 
                                                                             & (IData)(__VdfgRegularize_h6e95ff9d_0_51)))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_181 = (0x0000ffffffffffffULL 
                                                  & ((4U 
                                                      & (IData)(__VdfgRegularize_h6e95ff9d_0_52))
                                                      ? 
                                                     (((1U 
                                                        & (IData)(__VdfgRegularize_h6e95ff9d_0_52))
                                                        ? 
                                                       (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r
                                                        [__VdfgRegularize_h6e95ff9d_0_186] 
                                                        & (- (QData)((IData)(
                                                                             ((1U 
                                                                               > 
                                                                               (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                                                                [
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                                                << 1U)] 
                                                                                >> 4U))) 
                                                                              & (IData)(__VdfgRegularize_h6e95ff9d_0_179))))))
                                                        : 
                                                       (((QData)((IData)(vlSelfRef.milan_datapath__DOT__tone_smp_media)) 
                                                         << 0x00000018U) 
                                                        | (QData)((IData)(vlSelfRef.milan_datapath__DOT__tone_smp_media)))) 
                                                      & (- (QData)((IData)(
                                                                           (1U 
                                                                            & (~ 
                                                                               ((IData)(__VdfgRegularize_h6e95ff9d_0_52) 
                                                                                >> 1U)))))))
                                                      : 
                                                     ((2U 
                                                       & (IData)(__VdfgRegularize_h6e95ff9d_0_52))
                                                       ? 
                                                      (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r
                                                       [__VdfgRegularize_h6e95ff9d_0_186] 
                                                       & (- (QData)((IData)(
                                                                            ((~ (IData)(__VdfgRegularize_h6e95ff9d_0_52)) 
                                                                             & (IData)(__VdfgRegularize_h6e95ff9d_0_179))))))
                                                       : 
                                                      (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__i2s_hold_r 
                                                       & (- (QData)((IData)(
                                                                            (1U 
                                                                             & (IData)(__VdfgRegularize_h6e95ff9d_0_52)))))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__shadow_ram__v0) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__shadow_ram[vlSelfRef.__VdlyDim0__milan_datapath__DOT__csr__DOT__shadow_ram__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__shadow_ram__v0;
    }
    vlSelfRef.o_nvm_mem_wr_addr = vlSelfRef.o_nvm_mem_req_addr;
    vlSelfRef.o_nvm_mem_req_valid = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_hit_w)) 
                                     & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_ok_w 
        = ((0x17U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r[0U]) 
           & ((0x22U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r[1U]) 
              & (0x0400U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_plen_w))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_msrp_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_msrp_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__laown_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__laown_pend_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__laown_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__laown_pend_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__tctx_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tctx_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__tctx_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__tctx_r__v0;
    }
    vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_p_i 
        = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_p_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__tkd_crf_p_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_178 = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                  == 
                                                  (0x0000001fU 
                                                   & ((IData)(5U) 
                                                      + 
                                                      ((IData)(6U) 
                                                       * 
                                                       (7U 
                                                        & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                           >> 1U))))));
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__302__t 
        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__302__Vfuncout 
        = (3U | ((IData)(__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__302__t) 
                 << 4U));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
        = __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__302__Vfuncout;
    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w)
                    ? (0x0000001fU & (IData)(milan_datapath__DOT__csr_tctx_rd_addr_w))
                    : 3U);
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr;
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__304__t 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__304__Vfuncout 
                = (5U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__304__t) 
                         << 4U));
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__304__Vfuncout;
        } else {
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__305__t 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__305__Vfuncout 
                = (5U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__305__t) 
                         << 4U));
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__305__Vfuncout;
        }
    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w)
                    ? (0x0000001fU & (IData)(milan_datapath__DOT__csr_tctx_rd_addr_w))
                    : 3U);
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr;
        } else {
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__307__w 
                = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))
                    ? 4U : 3U);
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__307__t 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__307__Vfuncout 
                = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__307__t) 
                    << 4U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__307__w));
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__307__Vfuncout;
        }
    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__308__w 
            = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))
                ? 1U : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))
                         ? 2U : 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__308__t 
            = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__308__Vfuncout 
            = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__308__t) 
                << 4U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__308__w));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__308__Vfuncout;
    } else {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
            = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w)
                ? (0x0000001fU & (IData)(milan_datapath__DOT__csr_tctx_rd_addr_w))
                : 3U);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
            = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_25 = ((5U 
                                                  == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r)) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_w));
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_waddr_w 
        = (0x0000007fU & ((0x0cU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r))
                           ? ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_abs_byte_w) 
                              >> 3U) : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_ix_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_rd_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_rd_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r__v0][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r__v0[0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r__v0][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r__v0[1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r__v0][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r__v0[2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r__v0][3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r__v0[3U];
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v0] 
            = ((0xffffffffffffff00ULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r
                [vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v0]) 
               | (IData)((IData)(vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v0)));
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v1] 
            = ((0xffffffffffff00ffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r
                [vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v1]) 
               | ((QData)((IData)(vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v1)) 
                  << 8U));
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v2) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v2] 
            = ((0xffffffffff00ffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r
                [vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v2]) 
               | ((QData)((IData)(vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v2)) 
                  << 0x00000010U));
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v3) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v3] 
            = ((0xffffffff00ffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r
                [vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v3]) 
               | ((QData)((IData)(vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v3)) 
                  << 0x00000018U));
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v4) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v4] 
            = ((0xffffff00ffffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r
                [vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v4]) 
               | ((QData)((IData)(vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v4)) 
                  << 0x00000020U));
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v5) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v5] 
            = ((0xffff00ffffffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r
                [vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v5]) 
               | ((QData)((IData)(vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v5)) 
                  << 0x00000028U));
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v6) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v6] 
            = ((0xff00ffffffffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r
                [vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v6]) 
               | ((QData)((IData)(vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v6)) 
                  << 0x00000030U));
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v7) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v7] 
            = ((0x00ffffffffffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r
                [vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v7]) 
               | ((QData)((IData)(vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v7)) 
                  << 0x00000038U));
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_206 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsfmt_r) 
                                                  | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_205));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__rd_ptr_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__rd_ptr_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0][3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[3U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0][4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[4U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0][5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[5U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0][6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[6U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0][7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[7U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0][8U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[8U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0][9U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[9U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0][10U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[10U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0][11U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[11U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0][12U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[12U];
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_started_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_started_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__mem_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__mem_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__mem_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_len_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_len_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pending_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pending_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_uns_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_uns_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__seal_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__seal_pend_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__served_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__served_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__tmo_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__tmo_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__len_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__len_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_open_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_open_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_valid_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_valid_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__bix_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__bix_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__roff_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__roff_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rvalid_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rvalid_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wbusy_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wbusy_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rreq_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rreq_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rbusy_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rbusy_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opd_e_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opd_e_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__disp_valid_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__disp_valid_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rf_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rf_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rf_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rf_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_out_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_out_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rom_q_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rom_q_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_d_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_d_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ms_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ms_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxr_valid_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxr_valid_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cursor_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cursor_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opb_e_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opb_e_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_e_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_e_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__rd_fire_w 
        = (1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__retire_w) 
                    | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vwptr_r) 
                        == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vrptr_r)) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__wptr_r) 
                          == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__rptr_r))))));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__own_last_w 
        = ((3U & ((vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[0U] 
                   >> 1U) - (IData)(1U))) == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__push_same_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__push_ram_w) 
           & ((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_addr_r
               [vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_rp_r] 
               == (3U & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r))) 
              & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_act_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_snk_fail_code_w 
        = ((0x0000ff00U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r) 
                           & ((- (IData)((2U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_187)))) 
                              << 8U))) | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_ta_fail_code));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__rd_en_w 
        = ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__cnt_r)) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_valid_r)) 
              | (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__st_set_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rec_wr_en_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__st_clr_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ev_dep_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ev_disc_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_arm_w = 0U;
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
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ev_dep_w = 1U;
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
            if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r) 
                  >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r)) 
                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_ifx_r) 
                    == (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_q_r 
                                               >> 0x00000020U)))))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__st_clr_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ev_dep_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_cancel_w = 1U;
            }
        }
    }
}
