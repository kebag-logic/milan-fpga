// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

extern const VlWide<13>/*415:0*/ Vmilan_datapath__ConstPool__CONST_hb995d365_0;
extern const VlUnpacked<CData/*2:0*/, 256> Vmilan_datapath__ConstPool__TABLE_h9276b836_0;
extern const VlWide<28>/*895:0*/ Vmilan_datapath__ConstPool__CONST_hca6ff4b2_0;
extern const VlUnpacked<CData/*0:0*/, 14> Vmilan_datapath__ConstPool__TABLE_h90282f34_0;
extern const VlWide<48>/*1535:0*/ Vmilan_datapath__ConstPool__CONST_h22f5c49d_0;
extern const VlWide<8>/*255:0*/ Vmilan_datapath__ConstPool__CONST_h7f3586b3_0;
extern const VlWide<9>/*287:0*/ Vmilan_datapath__ConstPool__CONST_h9a2fc1c8_0;

void Vmilan_datapath___024root___nba_sequent__TOP__3(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___nba_sequent__TOP__3\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    QData/*63:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_allowed__61__command_type;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_allowed__61__command_type = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s = 0;
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
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__202__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__202__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__203__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__203__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__204__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__204__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__205__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__205__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__206__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__206__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__207__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__207__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__208__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__208__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__209__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__209__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__210__w;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__210__w = 0;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__chan_map_render__DOT__chwrap__219__ch;
    __Vfunc_milan_datapath__DOT__chan_map_render__DOT__chwrap__219__ch = 0;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__chan_map_render__DOT__chwrap__219__chans;
    __Vfunc_milan_datapath__DOT__chan_map_render__DOT__chwrap__219__chans = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_acc__267__Vfuncout;
    __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_acc__267__Vfuncout = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_acc__267__v;
    __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_acc__267__v = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_u__268__Vfuncout;
    __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_u__268__Vfuncout = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_u__268__v;
    __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_u__268__v = 0;
    QData/*63:0*/ __Vfunc_reorder_endian_func__269__Vfuncout;
    __Vfunc_reorder_endian_func__269__Vfuncout = 0;
    QData/*63:0*/ __Vfunc_reorder_endian_func__269__data_in;
    __Vfunc_reorder_endian_func__269__data_in = 0;
    IData/*31:0*/ __Vfunc_reorder_endian_func__269__width;
    __Vfunc_reorder_endian_func__269__width = 0;
    IData/*31:0*/ __Vfunc_reorder_endian_func__269__unnamedblk1__DOT__i;
    __Vfunc_reorder_endian_func__269__unnamedblk1__DOT__i = 0;
    QData/*63:0*/ __Vfunc_reorder_endian_func__269__data_out;
    __Vfunc_reorder_endian_func__269__data_out = 0;
    VlWide<4>/*127:0*/ __Vtemp_4;
    VlWide<14>/*447:0*/ __Vtemp_41;
    VlWide<9>/*287:0*/ __Vtemp_47;
    IData/*31:0*/ __Vtemp_48;
    // Body
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__b_mapo_w 
        = (0x0003ffffU & ((IData)(0x00000302U) + (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_len_r[7U] 
                                                  + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_pref_r[7U])));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txs_free_w = 0U;
    if ((0U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[0U])) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txs_free_w 
            = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txs_free_w)));
    }
    if ((0U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[1U])) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txs_free_w 
            = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txs_free_w)));
    }
    if ((0U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[2U])) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txs_free_w 
            = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txs_free_w)));
    }
    if ((0U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[3U])) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txs_free_w 
            = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txs_free_w)));
    }
    if ((0U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[4U])) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txs_free_w 
            = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txs_free_w)));
    }
    if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_st_r)) 
         & (8U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_idx_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__rd_data_o 
            = ((0x08ffU >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__rd_maddr_w))
                ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__mem_r
               [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__rd_maddr_w]
                : 0U);
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
    vlSelfRef.milan_datapath__DOT__pcm_route__DOT__render_active_o = 0U;
    if ((2U & vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[7U])) {
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__render_active_o = 1U;
    }
    if ((2U & vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[6U])) {
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__render_active_o = 1U;
    }
    if ((2U & vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[5U])) {
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__render_active_o = 1U;
    }
    if ((2U & vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[4U])) {
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__render_active_o = 1U;
    }
    if ((2U & vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[3U])) {
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__render_active_o = 1U;
    }
    if ((2U & vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[2U])) {
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__render_active_o = 1U;
    }
    if ((2U & vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[1U])) {
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__render_active_o = 1U;
    }
    if ((2U & vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[0U])) {
        vlSelfRef.milan_datapath__DOT__route_render_sel_w = 0U;
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__render_active_o = 1U;
    }
    vlSelfRef.milan_datapath__DOT__rsp_converged_w 
        = ((((((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[7U]) 
               << 1U) | vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[6U]) 
             << 6U) | ((((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[5U]) 
                         << 1U) | vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[4U]) 
                       << 4U)) | (((((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[3U]) 
                                     << 1U) | vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[2U]) 
                                   << 2U) | (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[1U]) 
                                              << 1U) 
                                             | vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[0U])));
    vlSelfRef.milan_datapath__DOT__rsp_prefill_w = 
        ((((((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[7U]) 
             << 1U) | vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[6U]) 
           << 6U) | ((((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[5U]) 
                       << 1U) | vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[4U]) 
                     << 4U)) | (((((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[3U]) 
                                   << 1U) | vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[2U]) 
                                 << 2U) | (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[1U]) 
                                            << 1U) 
                                           | vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[0U])));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_s_w[0U] 
        = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[0U]) 
                          - (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[0U])));
    vlSelfRef.milan_datapath__DOT__rsp_fill_w = ((0xffffffffffffff00ULL 
                                                  & vlSelfRef.milan_datapath__DOT__rsp_fill_w) 
                                                 | (IData)((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_s_w[0U])));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_s_w[1U] 
        = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[1U]) 
                          - (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[1U])));
    vlSelfRef.milan_datapath__DOT__rsp_fill_w = ((0xffffffffffff00ffULL 
                                                  & vlSelfRef.milan_datapath__DOT__rsp_fill_w) 
                                                 | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_s_w[1U])) 
                                                    << 8U));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_s_w[2U] 
        = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[2U]) 
                          - (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[2U])));
    vlSelfRef.milan_datapath__DOT__rsp_fill_w = ((0xffffffffff00ffffULL 
                                                  & vlSelfRef.milan_datapath__DOT__rsp_fill_w) 
                                                 | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_s_w[2U])) 
                                                    << 0x00000010U));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_s_w[3U] 
        = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[3U]) 
                          - (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[3U])));
    vlSelfRef.milan_datapath__DOT__rsp_fill_w = ((0xffffffff00ffffffULL 
                                                  & vlSelfRef.milan_datapath__DOT__rsp_fill_w) 
                                                 | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_s_w[3U])) 
                                                    << 0x00000018U));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_s_w[4U] 
        = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[4U]) 
                          - (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[4U])));
    vlSelfRef.milan_datapath__DOT__rsp_fill_w = ((0xffffff00ffffffffULL 
                                                  & vlSelfRef.milan_datapath__DOT__rsp_fill_w) 
                                                 | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_s_w[4U])) 
                                                    << 0x00000020U));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_s_w[5U] 
        = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[5U]) 
                          - (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[5U])));
    vlSelfRef.milan_datapath__DOT__rsp_fill_w = ((0xffff00ffffffffffULL 
                                                  & vlSelfRef.milan_datapath__DOT__rsp_fill_w) 
                                                 | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_s_w[5U])) 
                                                    << 0x00000028U));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_s_w[6U] 
        = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[6U]) 
                          - (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[6U])));
    vlSelfRef.milan_datapath__DOT__rsp_fill_w = ((0xff00ffffffffffffULL 
                                                  & vlSelfRef.milan_datapath__DOT__rsp_fill_w) 
                                                 | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_s_w[6U])) 
                                                    << 0x00000030U));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_s_w[7U] 
        = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[7U]) 
                          - (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[7U])));
    vlSelfRef.milan_datapath__DOT__rsp_fill_w = ((0x00ffffffffffffffULL 
                                                  & vlSelfRef.milan_datapath__DOT__rsp_fill_w) 
                                                 | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_s_w[7U])) 
                                                    << 0x00000038U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__link_q_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__eff_link_w));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__under_meta_r 
        = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__underrun_a_r;
    __Vfunc_reorder_endian_func__269__width = 0x00000040U;
    __Vfunc_reorder_endian_func__269__data_in = vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__s_tdata_q;
    __Vfunc_reorder_endian_func__269__data_out = 0;
    __Vfunc_reorder_endian_func__269__unnamedblk1__DOT__i = 0U;
    if (vlSelfRef.axis_resetn) {
        vlSelfRef.milan_datapath__DOT____Vcellout__adp_tx_mux__abort_evt_o = 0U;
        vlSelfRef.milan_datapath__DOT____Vcellout__adp_tx_mux__stall_evt_o = 0U;
        if ((((~ (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__locked_r)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__beat_accepted)) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__flush_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__locked_r = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__sel_r 
                = vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__gsel;
        }
        if (vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__flush_r) {
            if (vlSelfRef.m_axis_mac_tx_tready) {
                vlSelfRef.__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__flush_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__locked_r = 0U;
                vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__last_grant_r 
                    = vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__sel_r;
            }
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__active) 
                     & (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__beat_accepted)) 
                    & (IData)(vlSelfRef.m_axis_mac_tx_tlast))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__locked_r = 0U;
            vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__last_grant_r 
                = vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__gsel;
        }
        if ((1U & (((~ (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__locked_r)) 
                    & (~ (IData)(vlSelfRef.m_axis_mac_tx_tvalid))) 
                   | (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__beat_accepted)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__to_cnt_r = 0U;
        } else if ((0x00020000U & vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__to_cnt_r)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__to_cnt_r = 0U;
            if ((((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__locked_r) 
                  & (~ (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__flush_r))) 
                 & (~ (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__src_tvalid_w)))) {
                vlSelfRef.milan_datapath__DOT____Vcellout__adp_tx_mux__abort_evt_o = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__flush_r = 1U;
            } else {
                vlSelfRef.milan_datapath__DOT____Vcellout__adp_tx_mux__stall_evt_o = 1U;
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__to_cnt_r 
                = (0x0003ffffU & ((IData)(1U) + vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__to_cnt_r));
        }
        vlSelfRef.milan_datapath__DOT____Vcellout__ctl_tx_mux__abort_evt_o = 0U;
        vlSelfRef.milan_datapath__DOT____Vcellout__ctl_tx_mux__stall_evt_o = 0U;
        if ((((~ (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__locked_r)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__ctl_ifg__DOT__beat_acc)) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__flush_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__locked_r = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__sel_r 
                = vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__gsel;
        }
        if (vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__flush_r) {
            if (vlSelfRef.milan_datapath__DOT__ctlh_tx_tready) {
                vlSelfRef.__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__flush_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__locked_r = 0U;
                vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__last_grant_r 
                    = vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__sel_r;
            }
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__active) 
                     & (IData)(vlSelfRef.milan_datapath__DOT__ctl_ifg__DOT__beat_acc)) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__ctlh_tx_tlast))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__locked_r = 0U;
            vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__last_grant_r 
                = vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__gsel;
        }
        if ((1U & (((~ (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__locked_r)) 
                    & (~ (IData)(vlSelfRef.milan_datapath__DOT__ctlh_tx_tvalid))) 
                   | (IData)(vlSelfRef.milan_datapath__DOT__ctl_ifg__DOT__beat_acc)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__to_cnt_r = 0U;
        } else if ((0x00008000U & (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__to_cnt_r))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__to_cnt_r = 0U;
            if ((((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__locked_r) 
                  & (~ (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__flush_r))) 
                 & (~ (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__src_tvalid_w)))) {
                vlSelfRef.milan_datapath__DOT____Vcellout__ctl_tx_mux__abort_evt_o = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__flush_r = 1U;
            } else {
                vlSelfRef.milan_datapath__DOT____Vcellout__ctl_tx_mux__stall_evt_o = 1U;
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__to_cnt_r 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__to_cnt_r)));
        }
        vlSelfRef.milan_datapath__DOT____Vcellout__crf_dp_mux__abort_evt_o = 0U;
        vlSelfRef.milan_datapath__DOT____Vcellout__crf_dp_mux__stall_evt_o = 0U;
        if ((((~ (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__locked_r)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__beat_accepted)) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__flush_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__crf_dp_mux__DOT__locked_r = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__crf_dp_mux__DOT__sel_r 
                = vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__gsel;
        }
        if (vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__flush_r) {
            if (vlSelfRef.milan_datapath__DOT__dpcrf_tready) {
                vlSelfRef.__Vdly__milan_datapath__DOT__crf_dp_mux__DOT__flush_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__crf_dp_mux__DOT__locked_r = 0U;
                vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__last_grant_r 
                    = vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__sel_r;
            }
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__active) 
                     & (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__beat_accepted)) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__dpcrf_tlast))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__crf_dp_mux__DOT__locked_r = 0U;
            vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__last_grant_r 
                = vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__gsel;
        }
        if ((1U & (((~ (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__locked_r)) 
                    & (~ (IData)(vlSelfRef.milan_datapath__DOT__dpcrf_tvalid))) 
                   | (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__beat_accepted)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__crf_dp_mux__DOT__to_cnt_r = 0U;
        } else if ((0x00010000U & vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__to_cnt_r)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__crf_dp_mux__DOT__to_cnt_r = 0U;
            if ((((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__locked_r) 
                  & (~ (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__flush_r))) 
                 & (~ (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__src_tvalid_w)))) {
                vlSelfRef.milan_datapath__DOT____Vcellout__crf_dp_mux__abort_evt_o = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__crf_dp_mux__DOT__flush_r = 1U;
            } else {
                vlSelfRef.milan_datapath__DOT____Vcellout__crf_dp_mux__stall_evt_o = 1U;
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__crf_dp_mux__DOT__to_cnt_r 
                = (0x0001ffffU & ((IData)(1U) + vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__to_cnt_r));
        }
        vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_we_r = 0U;
        if (vlSelfRef.s_axi_awready) {
            if ((0x0920U != (IData)(vlSelfRef.s_axi_awaddr))) {
                if ((0x0934U != (IData)(vlSelfRef.s_axi_awaddr))) {
                    if ((0x0938U == (IData)(vlSelfRef.s_axi_awaddr))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_we_r = 1U;
                    } else if ((0x093cU == (IData)(vlSelfRef.s_axi_awaddr))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_we_r = 1U;
                    }
                }
            }
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_hold_valid_w = 0U;
        if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_rsp_w)))) {
            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_cancel_w)))) {
                if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_accept_w)))) {
                    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_exp_w)))) {
                        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_iss_w) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_hold_valid_w = 1U;
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_hold_slot_w 
                                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__slot_r;
                        }
                    }
                }
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__ser_start_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__cur_slot_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__slot_r;
        }
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wptr_bin_r 
            = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wptr_bin_n;
        if (vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_drain_w) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fifo_r__v0 
                = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r
                [vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_rp_r];
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fifo_r__v0 
                = (0x000001ffU & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wptr_r));
            vlSelfRef.__VdlySet__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fifo_r__v0 = 1U;
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_rp_r 
                = (3U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_rp_r)));
            vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wptr_r 
                = (0x000003ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wptr_r)));
        }
        if (vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_drop_w) {
            vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__was_filled_r = 0U;
        }
        if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fill_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__was_filled_r = 1U;
        }
        if ((((~ (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__prefill_r)) 
              & (0U == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fill_w))) 
             & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__was_filled_r))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__prefill_r = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__was_filled_r = 0U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__prefill_r) 
                    & (0x0010U <= (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fill_w)))) {
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
        if ((0x0001869fU == vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__ms_div_r)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__ms_div_r = 0U;
            if (((4U < (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fill_w)) 
                 & (0x001cU > (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fill_w)))) {
                if ((0x64U != (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__conv_ms_r))) {
                    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__conv_ms_r 
                        = (0x0000007fU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__conv_ms_r)));
                }
            } else if ((0x0028U < (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fill_w))) {
                vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__conv_ms_r = 0U;
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__ms_div_r 
                = (0x0001ffffU & ((IData)(1U) + vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__ms_div_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__gm_recentre_p_r) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__prefill_r))) 
             & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__was_filled_r))) {
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rptr_r 
                = (0x000003ffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wptr_r) 
                                  - (IData)(0x0010U)));
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__conv_ms_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__rsp_tvalid_w) {
            if (vlSelfRef.milan_datapath__DOT__rsp_tlast_w) {
                vlSelfRef.milan_datapath__DOT__chan_map_render__DOT____VlemCond_1 = 0U;
            } else {
                __Vfunc_milan_datapath__DOT__chan_map_render__DOT__chwrap__219__chans 
                    = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__eff_chans_w;
                __Vfunc_milan_datapath__DOT__chan_map_render__DOT__chwrap__219__ch 
                    = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__ch1_w;
                vlSelfRef.milan_datapath__DOT__chan_map_render__DOT____VlemCall_0__chwrap 
                    = (((0x0000000fU & ((IData)(1U) 
                                        + (IData)(__Vfunc_milan_datapath__DOT__chan_map_render__DOT__chwrap__219__ch))) 
                        == (IData)(__Vfunc_milan_datapath__DOT__chan_map_render__DOT__chwrap__219__chans))
                        ? 0U : (0x0000000fU & ((IData)(1U) 
                                               + (IData)(__Vfunc_milan_datapath__DOT__chan_map_render__DOT__chwrap__219__ch))));
                vlSelfRef.milan_datapath__DOT__chan_map_render__DOT____VlemCond_1 
                    = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT____VlemCall_0__chwrap;
            }
            vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__chpos_r 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT____VlemCond_1;
        }
        vlSelfRef.milan_datapath__DOT__wing_route_we_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_abort_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_cancel_release_valid_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_cancel_release_slot_w = 0U;
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r = 0U;
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r = 0U;
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__cancel_hit_w) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_abort_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_cancel_release_valid_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_cancel_release_slot_w 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__slot_r;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r = 0U;
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_iss_w) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r = 0U;
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__cancel_hit_w) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_abort_w = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_cancel_release_valid_w = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_cancel_release_slot_w 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__slot_r;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r = 0U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r = 4U;
                }
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__cancel_hit_w) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_abort_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_cancel_release_valid_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_cancel_release_slot_w 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__slot_r;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r = 0U;
            } else if ((0x3bU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r = 3U;
            } else {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r 
                    = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r)));
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r))) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__cancel_hit_w) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_abort_w = 1U;
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_gnt_w) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_cancel_release_valid_w = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_cancel_release_slot_w 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__alloc_slot_r;
                }
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__alloc_wait_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r = 0U;
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_gnt_w) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__slot_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__alloc_slot_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__seq_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r
                    [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__owner_r];
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__alloc_wait_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r = 2U;
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__alloc_wait_r 
                    = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__alloc_wait_r)));
            }
        } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ca_pick_ok_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__owner_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ca_pick_ix_w;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__ctlr_eid_r 
                = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r
                                    [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ca_pick_ix_w][3U])) 
                    << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r
                                                      [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ca_pick_ix_w][2U])));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__ctlr_mac_r 
                = (0x0000ffffffffffffULL & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r
                                                             [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ca_pick_ix_w][1U])) 
                                             << 0x00000010U) 
                                            | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r
                                                               [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ca_pick_ix_w][0U])) 
                                               >> 0x00000010U)));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__alloc_wait_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r = 1U;
        }
        vlSelfRef.milan_datapath__DOT__wing_tbl_we_r = 0U;
        if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ext_wr_ok_w) {
            if ((0U != (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r)))) {
                if ((1U != (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r)))) {
                    if ((4U == (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r)))) {
                        vlSelfRef.milan_datapath__DOT__wing_route_we_r = 1U;
                        vlSelfRef.milan_datapath__DOT__wing_route_r 
                            = (3U & (vlSelfRef.milan_datapath__DOT__lctx_wr_data_sane_w 
                                     >> 1U));
                        vlSelfRef.milan_datapath__DOT__wing_idx_r 
                            = (7U & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r) 
                                     >> 5U));
                        vlSelfRef.milan_datapath__DOT__wing_en_r 
                            = (1U & vlSelfRef.milan_datapath__DOT__lctx_wr_data_sane_w);
                        vlSelfRef.milan_datapath__DOT__wing_tbl_we_r 
                            = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__wing_stg_hit_w) 
                                     | (~ vlSelfRef.milan_datapath__DOT__lctx_wr_data_sane_w)));
                        vlSelfRef.milan_datapath__DOT__wing_sid_r 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__wing_stg_hit_w)
                                ? (((QData)((IData)(vlSelfRef.milan_datapath__DOT__wing_sid_hi_r)) 
                                    << 0x00000020U) 
                                   | (QData)((IData)(vlSelfRef.milan_datapath__DOT__wing_sid_lo_r)))
                                : 0ULL);
                    }
                }
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_v_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_slot_w 
                = (0x0000007fU & ((IData)(0x4eU) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_ix_w)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_owner_w 
                = (0x000000ffU & ((IData)(0x40U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_ix_w)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_dl_w 
                = ((IData)(0x00001388U) + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_cancel_w 
                = (2U == ((0x11U >= (0x0000001fU & 
                                     ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_ix_w) 
                                      << 1U))) ? (3U 
                                                  & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                                                     >> 
                                                     (0x0000001fU 
                                                      & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_ix_w) 
                                                         << 1U))))
                           : 0U));
            if ((0x11U >= (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_ix_w) 
                                          << 1U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                    = ((~ ((IData)(3U) << (0x0000001fU 
                                           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_ix_w) 
                                              << 1U)))) 
                       & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r);
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_v_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_slot_w 
                = (0x0000007fU & ((IData)(0x57U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_ix_w)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_owner_w 
                = (0x000000ffU & ((IData)(0x60U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_ix_w)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_dl_w 
                = ((IData)(0x00001388U) + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_cancel_w 
                = (2U == ((0x11U >= (0x0000001fU & 
                                     ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_ix_w) 
                                      << 1U))) ? (3U 
                                                  & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                                                     >> 
                                                     (0x0000001fU 
                                                      & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_ix_w) 
                                                         << 1U))))
                           : 0U));
            if ((0x11U >= (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_ix_w) 
                                          << 1U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                    = ((~ ((IData)(3U) << (0x0000001fU 
                                           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_ix_w) 
                                              << 1U)))) 
                       & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r);
            }
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w = 0U;
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            if ((2U == (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                    = (2U | (0x0003fffcU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (1U | (0x0003fffcU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r));
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
                    & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)))) {
            if ((1U == (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                    = (0x0003fffcU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w 
                    = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w));
            }
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__leaveall_any_w) 
                    & (1U == (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (2U | (0x0003fffcU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                = (1U | (0x0003fffcU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
        } else if (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w) 
                      & (0U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                - (IData)(0x00000057U)))) 
                     & (2U == (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))) 
                    & (1U != (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x0003fffcU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (0U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            if ((2U == (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                    = (2U | (0x0003fffcU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x0003fffcU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 1U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 2U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                    = (8U | (0x0003fff3U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (4U | (0x0003fff3U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
                     >> 1U) & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)))) {
            if ((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 2U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                    = (0x0003fff3U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w 
                    = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w));
            }
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__leaveall_any_w) 
                    & (4U == (0x0000000cU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (8U | (0x0003fff3U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                = (4U | (0x0003fff3U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w) 
                     & (8U == (0x0000000cU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))) 
                    & ((1U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                               - (IData)(0x00000057U))) 
                       & (1U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                                       >> 2U)))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x0003fff3U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (1U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 2U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                    = (8U | (0x0003fff3U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x0003fff3U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 2U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 4U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                    = (0x00000020U | (0x0003ffcfU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x00000010U | (0x0003ffcfU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
                     >> 2U) & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)))) {
            if ((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 4U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                    = (0x0003ffcfU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w 
                    = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w));
            }
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__leaveall_any_w) 
                    & (0x00000010U == (0x00000030U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x00000020U | (0x0003ffcfU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                = (0x00000010U | (0x0003ffcfU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w) 
                     & (0x00000020U == (0x00000030U 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))) 
                    & ((2U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                               - (IData)(0x00000057U))) 
                       & (1U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                                       >> 4U)))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x0003ffcfU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (2U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 4U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                    = (0x00000020U | (0x0003ffcfU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x0003ffcfU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 3U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 6U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                    = (0x00000080U | (0x0003ff3fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x00000040U | (0x0003ff3fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
                     >> 3U) & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)))) {
            if ((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 6U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                    = (0x0003ff3fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w 
                    = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w));
            }
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__leaveall_any_w) 
                    & (0x00000040U == (0x000000c0U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x00000080U | (0x0003ff3fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                = (0x00000040U | (0x0003ff3fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w) 
                     & (0x00000080U == (0x000000c0U 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))) 
                    & ((3U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                               - (IData)(0x00000057U))) 
                       & (1U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                                       >> 6U)))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x0003ff3fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (3U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 6U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                    = (0x00000080U | (0x0003ff3fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x0003ff3fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 4U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 8U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                    = (0x00000200U | (0x0003fcffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x00000100U | (0x0003fcffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
                     >> 4U) & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)))) {
            if ((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 8U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                    = (0x0003fcffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w 
                    = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w));
            }
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__leaveall_any_w) 
                    & (0x00000100U == (0x00000300U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x00000200U | (0x0003fcffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                = (0x00000100U | (0x0003fcffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w) 
                     & (0x00000200U == (0x00000300U 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))) 
                    & ((4U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                               - (IData)(0x00000057U))) 
                       & (1U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                                       >> 8U)))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x0003fcffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w 
                = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (4U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 8U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                    = (0x00000200U | (0x0003fcffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x0003fcffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 5U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 0x0aU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                    = (0x00000800U | (0x0003f3ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x00000400U | (0x0003f3ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
                     >> 5U) & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)))) {
            if ((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 0x0aU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                    = (0x0003f3ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w 
                    = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w));
            }
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__leaveall_any_w) 
                    & (0x00000400U == (0x00000c00U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x00000800U | (0x0003f3ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                = (0x00000400U | (0x0003f3ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w) 
                     & (0x00000800U == (0x00000c00U 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))) 
                    & ((5U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                               - (IData)(0x00000057U))) 
                       & (1U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                                       >> 0x0aU)))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x0003f3ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w 
                = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (5U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 0x0aU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                    = (0x00000800U | (0x0003f3ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x0003f3ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 6U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 0x0cU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                    = (0x00002000U | (0x0003cfffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x00001000U | (0x0003cfffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
                     >> 6U) & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)))) {
            if ((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 0x0cU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                    = (0x0003cfffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w 
                    = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w));
            }
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__leaveall_any_w) 
                    & (0x00001000U == (0x00003000U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x00002000U | (0x0003cfffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                = (0x00001000U | (0x0003cfffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w) 
                     & (0x00002000U == (0x00003000U 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))) 
                    & ((6U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                               - (IData)(0x00000057U))) 
                       & (1U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                                       >> 0x0cU)))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x0003cfffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w 
                = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (6U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 0x0cU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                    = (0x00002000U | (0x0003cfffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x0003cfffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 7U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 0x0eU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                    = (0x00008000U | (0x00033fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x00004000U | (0x00033fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
                     >> 7U) & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)))) {
            if ((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 0x0eU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                    = (0x00033fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w 
                    = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w));
            }
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__leaveall_any_w) 
                    & (0x00004000U == (0x0000c000U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x00008000U | (0x00033fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                = (0x00004000U | (0x00033fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w) 
                     & (0x00008000U == (0x0000c000U 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))) 
                    & ((7U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                               - (IData)(0x00000057U))) 
                       & (1U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                                       >> 0x0eU)))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x00033fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w 
                = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (7U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 0x0eU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                    = (0x00008000U | (0x00033fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x00033fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 8U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 0x10U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                    = (0x00020000U | (0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x00010000U | (0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
                     >> 8U) & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)))) {
            if ((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 0x10U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                    = (0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w 
                    = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w));
            }
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__leaveall_any_w) 
                    & (0x00010000U == (0x00030000U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x00020000U | (0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                = (0x00010000U | (0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w) 
                     & (0x00020000U == (0x00030000U 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))) 
                    & ((8U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                               - (IData)(0x00000057U))) 
                       & (1U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                                       >> 0x10U)))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w 
                = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (8U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                              >> 0x10U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                    = (0x00020000U | (0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                = (0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r);
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
             & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                 | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            if ((2U == (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                    = (2U | (0x0003fffcU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (1U | (0x0003fffcU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r));
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
                    & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)))) {
            if ((1U == (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                    = (0x0003fffcU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
            }
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__leaveall_any_w) 
                    & (1U == (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (2U | (0x0003fffcU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                = (1U | (0x0003fffcU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
        } else if (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__exp_hit_w) 
                      & (0U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                - (IData)(0x0000004eU)))) 
                     & (2U == (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r))) 
                    & (1U != (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x0003fffcU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (0U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            if ((2U == (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                    = (2U | (0x0003fffcU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x0003fffcU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
              >> 1U) & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                         | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                        | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 2U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                    = (8U | (0x0003fff3U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (4U | (0x0003fff3U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
                     >> 1U) & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)))) {
            if ((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 2U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                    = (0x0003fff3U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
            }
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__leaveall_any_w) 
                    & (4U == (0x0000000cU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (8U | (0x0003fff3U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                = (4U | (0x0003fff3U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__exp_hit_w) 
                     & (8U == (0x0000000cU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r))) 
                    & ((1U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                               - (IData)(0x0000004eU))) 
                       & (1U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                                       >> 2U)))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x0003fff3U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (1U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 2U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                    = (8U | (0x0003fff3U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x0003fff3U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
              >> 2U) & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                         | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                        | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 4U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                    = (0x00000020U | (0x0003ffcfU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x00000010U | (0x0003ffcfU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
                     >> 2U) & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)))) {
            if ((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 4U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                    = (0x0003ffcfU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
            }
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__leaveall_any_w) 
                    & (0x00000010U == (0x00000030U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x00000020U | (0x0003ffcfU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                = (0x00000010U | (0x0003ffcfU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__exp_hit_w) 
                     & (0x00000020U == (0x00000030U 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r))) 
                    & ((2U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                               - (IData)(0x0000004eU))) 
                       & (1U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                                       >> 4U)))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x0003ffcfU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (2U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 4U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                    = (0x00000020U | (0x0003ffcfU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x0003ffcfU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
              >> 3U) & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                         | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                        | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 6U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                    = (0x00000080U | (0x0003ff3fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x00000040U | (0x0003ff3fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
                     >> 3U) & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)))) {
            if ((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 6U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                    = (0x0003ff3fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
            }
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__leaveall_any_w) 
                    & (0x00000040U == (0x000000c0U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x00000080U | (0x0003ff3fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                = (0x00000040U | (0x0003ff3fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__exp_hit_w) 
                     & (0x00000080U == (0x000000c0U 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r))) 
                    & ((3U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                               - (IData)(0x0000004eU))) 
                       & (1U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                                       >> 6U)))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x0003ff3fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (3U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 6U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                    = (0x00000080U | (0x0003ff3fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x0003ff3fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
              >> 4U) & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                         | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                        | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 8U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                    = (0x00000200U | (0x0003fcffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x00000100U | (0x0003fcffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
                     >> 4U) & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)))) {
            if ((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 8U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                    = (0x0003fcffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
            }
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__leaveall_any_w) 
                    & (0x00000100U == (0x00000300U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x00000200U | (0x0003fcffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                = (0x00000100U | (0x0003fcffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__exp_hit_w) 
                     & (0x00000200U == (0x00000300U 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r))) 
                    & ((4U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                               - (IData)(0x0000004eU))) 
                       & (1U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                                       >> 8U)))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x0003fcffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (4U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 8U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                    = (0x00000200U | (0x0003fcffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x0003fcffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
              >> 5U) & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                         | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                        | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 0x0aU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                    = (0x00000800U | (0x0003f3ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x00000400U | (0x0003f3ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
                     >> 5U) & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)))) {
            if ((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 0x0aU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                    = (0x0003f3ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
            }
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__leaveall_any_w) 
                    & (0x00000400U == (0x00000c00U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x00000800U | (0x0003f3ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                = (0x00000400U | (0x0003f3ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__exp_hit_w) 
                     & (0x00000800U == (0x00000c00U 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r))) 
                    & ((5U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                               - (IData)(0x0000004eU))) 
                       & (1U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                                       >> 0x0aU)))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x0003f3ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (5U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 0x0aU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                    = (0x00000800U | (0x0003f3ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x0003f3ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
              >> 6U) & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                         | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                        | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 0x0cU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                    = (0x00002000U | (0x0003cfffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x00001000U | (0x0003cfffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
                     >> 6U) & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)))) {
            if ((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 0x0cU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                    = (0x0003cfffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
            }
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__leaveall_any_w) 
                    & (0x00001000U == (0x00003000U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x00002000U | (0x0003cfffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                = (0x00001000U | (0x0003cfffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__exp_hit_w) 
                     & (0x00002000U == (0x00003000U 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r))) 
                    & ((6U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                               - (IData)(0x0000004eU))) 
                       & (1U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                                       >> 0x0cU)))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x0003cfffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (6U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 0x0cU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                    = (0x00002000U | (0x0003cfffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x0003cfffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
              >> 7U) & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                         | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                        | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 0x0eU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                    = (0x00008000U | (0x00033fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x00004000U | (0x00033fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
                     >> 7U) & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)))) {
            if ((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 0x0eU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                    = (0x00033fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
            }
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__leaveall_any_w) 
                    & (0x00004000U == (0x0000c000U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x00008000U | (0x00033fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                = (0x00004000U | (0x00033fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__exp_hit_w) 
                     & (0x00008000U == (0x0000c000U 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r))) 
                    & ((7U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                               - (IData)(0x0000004eU))) 
                       & (1U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                                       >> 0x0eU)))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x00033fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (7U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 0x0eU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                    = (0x00008000U | (0x00033fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x00033fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
              >> 8U) & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                         | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                        | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 0x10U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                    = (0x00020000U | (0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x00010000U | (0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
                     >> 8U) & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)))) {
            if ((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 0x10U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                    = (0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
            }
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__leaveall_any_w) 
                    & (0x00010000U == (0x00030000U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x00020000U | (0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                = (0x00010000U | (0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__exp_hit_w) 
                     & (0x00020000U == (0x00030000U 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r))) 
                    & ((8U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                               - (IData)(0x0000004eU))) 
                       & (1U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                                       >> 0x10U)))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (8U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                              >> 0x10U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r 
                    = (0x00020000U | (0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r 
                = (0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r);
        }
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_req_r = 0U;
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_act_r) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_prng_valid_w) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_act_r = 0U;
            }
        } else if ((((1U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U]) 
                     & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_prng_busy_w))) 
                    & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_req_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_req_r = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_req_kind_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_need_kind_w;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_if_r = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_kind_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_need_kind_w;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_act_r = 1U;
        }
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__cap_vld_r = 0U;
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r = 0U;
        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r = 0U;
                } else if ((8U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r = 7U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r 
                        = (0x0000000fU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r)));
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r = 3U;
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r 
                    = ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r))
                        ? 6U : (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ev_dep_w) 
                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ev_disc_w))
                                 ? 5U : 6U));
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r 
                    = (((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r)) 
                        && (1U & ((((((0x03fffffcU 
                                       & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r) 
                                           >> 6U) & 
                                          ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_eid_r 
                                            == (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[17U])) 
                                                 << 0x00000020U) 
                                                | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[16U])))) 
                                           << 2U))) 
                                      | ((0x03fffffeU 
                                          & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r) 
                                              >> 6U) 
                                             & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_eid_r 
                                                 == 
                                                 (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[15U])) 
                                                   << 0x00000020U) 
                                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[14U])))) 
                                                << 1U))) 
                                         | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r) 
                                             >> 6U) 
                                            & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_eid_r 
                                               == (
                                                   ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[13U])) 
                                                    << 0x00000020U) 
                                                   | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[12U]))))))) 
                                     << 6U) | (((0x0ffffffeU 
                                                 & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r) 
                                                     >> 4U) 
                                                    & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_eid_r 
                                                        == 
                                                        (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[11U])) 
                                                          << 0x00000020U) 
                                                         | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[10U])))) 
                                                       << 1U))) 
                                                | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r) 
                                                    >> 4U) 
                                                   & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_eid_r 
                                                      == 
                                                      (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[9U])) 
                                                        << 0x00000020U) 
                                                       | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[8U])))))) 
                                               << 4U)) 
                                   | ((((0x3ffffffeU 
                                         & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r) 
                                             >> 2U) 
                                            & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_eid_r 
                                                == 
                                                (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[7U])) 
                                                  << 0x00000020U) 
                                                 | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[6U])))) 
                                               << 1U))) 
                                        | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r) 
                                            >> 2U) 
                                           & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_eid_r 
                                              == (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[5U])) 
                                                   << 0x00000020U) 
                                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[4U])))))) 
                                       << 2U) | ((0xfffffffeU 
                                                  & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r) 
                                                     & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_eid_r 
                                                         == 
                                                         (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[3U])) 
                                                           << 0x00000020U) 
                                                          | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[2U])))) 
                                                        << 1U))) 
                                                 | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r) 
                                                    & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_eid_r 
                                                       == 
                                                       (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[1U])) 
                                                         << 0x00000020U) 
                                                        | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r[0U])))))))) 
                                  >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r))))
                        ? 4U : 6U);
            } else {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__cap_vld_r) {
                    if ((0x27U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__cap_idx_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_aidx_r 
                            = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_aidx_r 
                                << 8U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxp_rd_data_w__BRA__7__03a0__KET__));
                    } else if ((0x2fU >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__cap_idx_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_gm_r 
                            = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_gm_r 
                                << 8U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxp_rd_data_w__BRA__7__03a0__KET__)));
                    } else if ((0x30U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__cap_idx_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_dom_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxp_rd_data_w__BRA__7__03a0__KET__;
                    } else if ((0x36U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__cap_idx_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_ifx_r 
                            = ((0x0000ff00U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_ifx_r) 
                                               << 8U)) 
                               | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxp_rd_data_w__BRA__7__03a0__KET__));
                    }
                    if ((0x37U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__cap_idx_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r = 3U;
                    }
                }
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__cap_vld_r = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__cap_idx_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rd_ptr_r;
                if ((0x37U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rd_ptr_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rd_ptr_r 
                        = (0x0000003fU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rd_ptr_r)));
                }
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r))) {
            if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__txn_in_valid_q_r) 
                  & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_msg_r)) 
                     | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_msg_r)))) 
                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_have_slot_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rd_ptr_r = 0x24U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r = 2U;
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r = 7U;
            }
        } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_valid_r) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_msg_r 
                = (0x0000000fU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[11U] 
                                   << 2U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[10U] 
                                             >> 0x0000001eU)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_eid_r 
                = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[6U])) 
                    << 0x00000022U) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[5U])) 
                                        << 2U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[4U])) 
                                                  >> 0x0000001eU)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_vt_r 
                = (0x0000001fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[10U] 
                                  >> 0x00000019U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_if_r 
                = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[12U] 
                         >> 5U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_slot_r 
                = (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[1U] 
                         >> 0x00000019U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__txn_in_valid_q_r 
                = (0U == (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r[11U] 
                                >> 2U)));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__accept_w) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_vld_r) {
                __Vtemp_4[0U] = (IData)((((QData)((IData)(
                                                          (7U 
                                                           | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_rx_slot_r) 
                                                               << 0x00000017U) 
                                                              | ((((1U 
                                                                    == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r))
                                                                    ? 2U
                                                                    : 
                                                                   (3U 
                                                                    & (- (IData)(
                                                                                ((2U 
                                                                                == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r)) 
                                                                                & ((0x002cU 
                                                                                == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_opcode_r)) 
                                                                                | (0x002dU 
                                                                                == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_opcode_r)))))))) 
                                                                  << 0x00000013U) 
                                                                 | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r) 
                                                                    << 3U)))))) 
                                          << 0x00000022U) 
                                         | (((QData)((IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r 
                                                              + 
                                                              ((0U 
                                                                == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r))
                                                                ? 0x00000fa0U
                                                                : 
                                                               ((1U 
                                                                 == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r))
                                                                 ? 0x00000032U
                                                                 : 0x00000064U))))) 
                                             << 2U) 
                                            | (QData)((IData)(
                                                              (1U 
                                                               & (- (IData)(
                                                                            ((1U 
                                                                              == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r)) 
                                                                             | (0U 
                                                                                == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r)))))))))));
                __Vtemp_4[1U] = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_operands_r) 
                                  << 0x0000001cU) | (IData)(
                                                            ((((QData)((IData)(
                                                                               (7U 
                                                                                | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_rx_slot_r) 
                                                                                << 0x00000017U) 
                                                                                | ((((1U 
                                                                                == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r))
                                                                                 ? 2U
                                                                                 : 
                                                                                (3U 
                                                                                & (- (IData)(
                                                                                ((2U 
                                                                                == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r)) 
                                                                                & ((0x002cU 
                                                                                == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_opcode_r)) 
                                                                                | (0x002dU 
                                                                                == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_opcode_r)))))))) 
                                                                                << 0x00000013U) 
                                                                                | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r) 
                                                                                << 3U)))))) 
                                                               << 0x00000022U) 
                                                              | (((QData)((IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r 
                                                                                + 
                                                                                ((0U 
                                                                                == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r))
                                                                                 ? 0x00000fa0U
                                                                                 : 
                                                                                ((1U 
                                                                                == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r))
                                                                                 ? 0x00000032U
                                                                                 : 0x00000064U))))) 
                                                                  << 2U) 
                                                                 | (QData)((IData)(
                                                                                (1U 
                                                                                & (- (IData)(
                                                                                ((1U 
                                                                                == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r)) 
                                                                                | (0U 
                                                                                == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r)))))))))) 
                                                             >> 0x00000020U)));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[0U] 
                    = __Vtemp_4[0U];
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[1U] 
                    = __Vtemp_4[1U];
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[2U] 
                    = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_operands_r) 
                        >> 4U) | ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_operands_r 
                                           >> 0x00000020U)) 
                                  << 0x0000001cU));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[3U] 
                    = (((IData)((((QData)((IData)((
                                                   ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_seq_r) 
                                                    << 1U) 
                                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_u_r)))) 
                                  << 0x00000011U) | (QData)((IData)(
                                                                    (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_cr_r) 
                                                                      << 0x00000010U) 
                                                                     | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_opcode_r)))))) 
                        << 0x0000001cU) | ((IData)(
                                                   (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_operands_r 
                                                    >> 0x00000020U)) 
                                           >> 4U));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[4U] 
                    = (((IData)((((QData)((IData)((
                                                   ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_seq_r) 
                                                    << 1U) 
                                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_u_r)))) 
                                  << 0x00000011U) | (QData)((IData)(
                                                                    (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_cr_r) 
                                                                      << 0x00000010U) 
                                                                     | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_opcode_r)))))) 
                        >> 4U) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_target_eid_r) 
                                   << 0x0000001eU) 
                                  | ((IData)(((((QData)((IData)(
                                                                (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_seq_r) 
                                                                  << 1U) 
                                                                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_u_r)))) 
                                                << 0x00000011U) 
                                               | (QData)((IData)(
                                                                 (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_cr_r) 
                                                                   << 0x00000010U) 
                                                                  | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_opcode_r))))) 
                                              >> 0x00000020U)) 
                                     << 0x0000001cU)));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[5U] 
                    = (((0x0fffffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_target_eid_r) 
                                        >> 2U)) | ((IData)(
                                                           ((((QData)((IData)(
                                                                              (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_seq_r) 
                                                                                << 1U) 
                                                                               | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_u_r)))) 
                                                              << 0x00000011U) 
                                                             | (QData)((IData)(
                                                                               (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_cr_r) 
                                                                                << 0x00000010U) 
                                                                                | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_opcode_r))))) 
                                                            >> 0x00000020U)) 
                                                   >> 4U)) 
                       | ((0x30000000U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_target_eid_r) 
                                          >> 2U)) | 
                          ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_target_eid_r 
                                    >> 0x00000020U)) 
                           << 0x0000001eU)));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[6U] 
                    = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_ctlr_eid_r) 
                        << 0x0000001eU) | ((0x0fffffffU 
                                            & ((IData)(
                                                       (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_target_eid_r 
                                                        >> 0x00000020U)) 
                                               >> 2U)) 
                                           | (0x30000000U 
                                              & ((IData)(
                                                         (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_target_eid_r 
                                                          >> 0x00000020U)) 
                                                 >> 2U))));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[7U] 
                    = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_ctlr_eid_r) 
                        >> 2U) | ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_ctlr_eid_r 
                                           >> 0x00000020U)) 
                                  << 0x0000001eU));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[8U] 
                    = (((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_ctlr_eid_r 
                                 >> 0x00000020U)) >> 2U) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_src_mac_r) 
                          << 0x0000001eU));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[9U] 
                    = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_src_mac_r) 
                        >> 2U) | ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_src_mac_r 
                                           >> 0x00000020U)) 
                                  << 0x0000001eU));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[10U] 
                    = (((0x3fffc000U & ((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r)) 
                                                  << 0x00000017U) 
                                                 | (QData)((IData)(
                                                                   (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r) 
                                                                     << 0x00000014U) 
                                                                    | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_msg_type_r) 
                                                                        << 0x00000010U) 
                                                                       | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_status_r) 
                                                                           << 0x0000000bU) 
                                                                          | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_cdl_r)))))))) 
                                        << 0x0000000eU)) 
                        | ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_src_mac_r 
                                    >> 0x00000020U)) 
                           >> 2U)) | (0xc0000000U & 
                                      ((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r)) 
                                                 << 0x00000017U) 
                                                | (QData)((IData)(
                                                                  (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r) 
                                                                    << 0x00000014U) 
                                                                   | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_msg_type_r) 
                                                                       << 0x00000010U) 
                                                                      | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_status_r) 
                                                                          << 0x0000000bU) 
                                                                         | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_cdl_r)))))))) 
                                       << 0x0000000eU)));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[11U] 
                    = ((((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r)) 
                                   << 0x00000017U) 
                                  | (QData)((IData)(
                                                    (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r) 
                                                      << 0x00000014U) 
                                                     | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_msg_type_r) 
                                                         << 0x00000010U) 
                                                        | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_status_r) 
                                                            << 0x0000000bU) 
                                                           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_cdl_r)))))))) 
                         >> 0x00000012U) | (0x3fffc000U 
                                            & ((IData)(
                                                       ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r)) 
                                                          << 0x00000017U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r) 
                                                                             << 0x00000014U) 
                                                                            | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_msg_type_r) 
                                                                                << 0x00000010U) 
                                                                               | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_status_r) 
                                                                                << 0x0000000bU) 
                                                                                | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_cdl_r))))))) 
                                                        >> 0x00000020U)) 
                                               << 0x0000000eU))) 
                       | (0xc0000000U & ((IData)(((
                                                   ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r)) 
                                                    << 0x00000017U) 
                                                   | (QData)((IData)(
                                                                     (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r) 
                                                                       << 0x00000014U) 
                                                                      | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_msg_type_r) 
                                                                          << 0x00000010U) 
                                                                         | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_status_r) 
                                                                             << 0x0000000bU) 
                                                                            | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_cdl_r))))))) 
                                                  >> 0x00000020U)) 
                                         << 0x0000000eU)));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[12U] 
                    = ((IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r)) 
                                  << 0x00000017U) | (QData)((IData)(
                                                                    (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r) 
                                                                      << 0x00000014U) 
                                                                     | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_msg_type_r) 
                                                                         << 0x00000010U) 
                                                                        | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_status_r) 
                                                                            << 0x0000000bU) 
                                                                           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_cdl_r))))))) 
                                >> 0x00000020U)) >> 0x00000012U);
            } else {
                VL_ASSIGN_W(393, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r, Vmilan_datapath__ConstPool__CONST_hb995d365_0);
            }
        }
    } else {
        vlSelfRef.__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__locked_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__sel_r = 0U;
        vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__last_grant_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__flush_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__to_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT____Vcellout__adp_tx_mux__abort_evt_o = 0U;
        vlSelfRef.milan_datapath__DOT____Vcellout__adp_tx_mux__stall_evt_o = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__locked_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__sel_r = 0U;
        vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__last_grant_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__flush_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__to_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT____Vcellout__ctl_tx_mux__abort_evt_o = 0U;
        vlSelfRef.milan_datapath__DOT____Vcellout__ctl_tx_mux__stall_evt_o = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__crf_dp_mux__DOT__locked_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__crf_dp_mux__DOT__sel_r = 0U;
        vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__last_grant_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__crf_dp_mux__DOT__flush_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__crf_dp_mux__DOT__to_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT____Vcellout__crf_dp_mux__abort_evt_o = 0U;
        vlSelfRef.milan_datapath__DOT____Vcellout__crf_dp_mux__stall_evt_o = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_we_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_hold_valid_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_hold_slot_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__cur_slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wptr_bin_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rptr_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wen_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wptr_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_rp_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wdata_r = 0ULL;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__ms_div_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__conv_ms_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__was_filled_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__prefill_r = 1U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__chpos_r = 0U;
        vlSelfRef.milan_datapath__DOT__wing_route_we_r = 0U;
        vlSelfRef.milan_datapath__DOT__wing_route_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__owner_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__ctlr_eid_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__ctlr_mac_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__seq_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__alloc_wait_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_abort_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_cancel_release_valid_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_cancel_release_slot_w = 0U;
        vlSelfRef.milan_datapath__DOT__wing_idx_r = 0U;
        vlSelfRef.milan_datapath__DOT__wing_en_r = 0U;
        vlSelfRef.milan_datapath__DOT__wing_tbl_we_r = 0U;
        vlSelfRef.milan_datapath__DOT__wing_sid_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_slot_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_owner_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_slot_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_owner_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_dl_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_dl_w = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_cancel_w = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_cancel_w = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_req_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_act_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_if_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_kind_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_req_kind_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rd_ptr_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__cap_vld_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_msg_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_eid_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_vt_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_if_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_slot_r = 7U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__cap_idx_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_aidx_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_gm_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_dom_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_ifx_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__txn_in_valid_q_r = 0U;
        VL_ASSIGN_W(393, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r, Vmilan_datapath__ConstPool__CONST_hb995d365_0);
    }
    if ((1U & (~ (IData)(vlSelfRef.axis_resetn)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_svc_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_svc_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_svc_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_svc_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_svc_r[4U] = 0U;
    }
    while (VL_LTS_III(32, __Vfunc_reorder_endian_func__269__unnamedblk1__DOT__i, 
                      VL_DIVS_III(32, __Vfunc_reorder_endian_func__269__width, (IData)(8U)))) {
        __Vfunc_reorder_endian_func__269__data_out 
            = (((~ (0x00000000000000ffULL << (0x0000003fU 
                                              & VL_MULS_III(32, (IData)(8U), __Vfunc_reorder_endian_func__269__unnamedblk1__DOT__i)))) 
                & __Vfunc_reorder_endian_func__269__data_out) 
               | ((QData)((IData)((0x000000ffU & (IData)(
                                                         (__Vfunc_reorder_endian_func__269__data_in 
                                                          >> 
                                                          (0x0000003fU 
                                                           & (__Vfunc_reorder_endian_func__269__width 
                                                              - 
                                                              VL_MULS_III(32, (IData)(8U), 
                                                                          ((IData)(1U) 
                                                                           + __Vfunc_reorder_endian_func__269__unnamedblk1__DOT__i))))))))) 
                  << (0x0000003fU & VL_MULS_III(32, (IData)(8U), __Vfunc_reorder_endian_func__269__unnamedblk1__DOT__i))));
        __Vfunc_reorder_endian_func__269__unnamedblk1__DOT__i 
            = ((IData)(1U) + __Vfunc_reorder_endian_func__269__unnamedblk1__DOT__i);
    }
    if ((1U & (~ (IData)(vlSelfRef.axis_resetn)))) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_status_q_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_probing_q_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_state_q_r = 0U;
    }
    __Vfunc_reorder_endian_func__269__Vfuncout = __Vfunc_reorder_endian_func__269__data_out;
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__beat_be 
        = __Vfunc_reorder_endian_func__269__Vfuncout;
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp0_w 
        = ((0x00ff0000U & ((IData)(vlSelfRef.milan_datapath__DOT__rsp_tdata_w) 
                           << 0x00000010U)) | ((0x0000ff00U 
                                                & ((IData)(
                                                           (vlSelfRef.milan_datapath__DOT__rsp_tdata_w 
                                                            >> 8U)) 
                                                   << 8U)) 
                                               | (0x000000ffU 
                                                  & (IData)(
                                                            (vlSelfRef.milan_datapath__DOT__rsp_tdata_w 
                                                             >> 0x00000010U)))));
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp1_w 
        = ((0x00ff0000U & ((IData)((vlSelfRef.milan_datapath__DOT__rsp_tdata_w 
                                    >> 0x00000020U)) 
                           << 0x00000010U)) | ((0x0000ff00U 
                                                & ((IData)(
                                                           (vlSelfRef.milan_datapath__DOT__rsp_tdata_w 
                                                            >> 0x00000028U)) 
                                                   << 8U)) 
                                               | (0x000000ffU 
                                                  & (IData)(
                                                            (vlSelfRef.milan_datapath__DOT__rsp_tdata_w 
                                                             >> 0x00000030U)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__retire_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__out_valid_r) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__od_last_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_full_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vwptr_r) 
           == (0x10U ^ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vrptr_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_pick_ix_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_slot_w = 0U;
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_pick_ix_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_slot_w 
            = (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_slot_r));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r) 
                  >> 1U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_pick_ix_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_slot_w 
            = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_slot_r) 
                     >> 2U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r) 
                  >> 2U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_pick_ix_w = 2U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_slot_w 
            = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_slot_r) 
                     >> 4U));
    }
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_380 = ((4U 
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
    vlSelfRef.o_mac_ifg = (0x000000ffU & vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ifg);
    vlSelfRef.o_mc_hash = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mc_hi)) 
                            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mc_lo)));
    vlSelfRef.milan_datapath__DOT__cfg_crft_dmac = 
        (((QData)((IData)((0x0000ffffU & vlSelfRef.milan_datapath__DOT__csr__DOT__crft_dmhi))) 
          << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__crft_dmlo)));
    vlSelfRef.milan_datapath__DOT__cfg_crft_sid = (
                                                   ((QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__crft_sidhi)) 
                                                    << 0x00000020U) 
                                                   | (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__crft_sidlo)));
    vlSelfRef.milan_datapath__DOT____Vcellinp__avtp_rx_monitor__pres_ofs_i 
        = ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r))
            ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[0U]
            : 0x001e8480U);
    vlSelfRef.o_mac_tx_en = (1U & vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ctrl);
    vlSelfRef.o_mac_rx_en = (1U & (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ctrl 
                                   >> 1U));
    vlSelfRef.o_mac_promisc = (1U & (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ctrl 
                                     >> 2U));
    vlSelfRef.o_mac_allmulti = (1U & (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ctrl 
                                      >> 3U));
    vlSelfRef.milan_datapath__DOT__pcm_lpf_active = 
        (vlSelfRef.milan_datapath__DOT__csr__DOT__lpf_ctrl 
         & (2U == (IData)(vlSelfRef.milan_datapath__DOT__mon_wire_chans_w)));
    vlSelfRef.milan_datapath__DOT__pp_aecp_cur_config_w 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__cfg_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p1_en_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__wr_en_w));
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__s_tlast_q 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.s_axis_mac_rx_tlast));
    vlSelfRef.o_mac_addr = (((QData)((IData)((0x0000ffffU 
                                              & vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ahi))) 
                             << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_alo)));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout 
        = ((__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s 
            >> 1U) ^ ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__s))
                       ? 0xd800000000000000ULL : 0ULL));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_step_f__141__Vfuncout;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_next_w 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__advance_16__DOT__s;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__link_up_q_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__eff_link_w));
    vlSelfRef.milan_datapath__DOT__link_guard__DOT__both_alive_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__rx_alive_r) 
           & (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__tx_alive_r));
    vlSelfRef.s_axi_rvalid = vlSelfRef.milan_datapath__DOT__csr__DOT__r_valid;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__free_mask_w 
        = (0x0000000fU & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__writing_r) 
                             | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__occupied_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__free_mask_w 
        = (0x0000000fU & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__writing_r) 
                             | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__occupied_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__free_mask_w 
        = (0x0000000fU & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__writing_r) 
                             | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__occupied_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__free_mask_w 
        = (0x0000000fU & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__writing_r) 
                             | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__occupied_r))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_159 = (0x3fffffffU 
                                                  & ((IData)(
                                                             (0x00000fffffffffffULL 
                                                              & VL_SHIFTRS_QQI(44,44,32, vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r, 0x0000000eU))) 
                                                     + 
                                                     (1U 
                                                      & (- (IData)(
                                                                   (1U 
                                                                    & (IData)(
                                                                              (vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r 
                                                                               >> 0x0000000dU))))))));
    vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__sub_w 
        = ((3U == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r)) 
           | ((4U == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r)) 
              | ((8U == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r)) 
                 | (9U == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r)))));
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
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r) 
                  >> 1U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_sink_w = 1U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r) 
                  >> 2U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_sink_w = 2U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r) 
                  >> 3U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_sink_w = 3U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r) 
                  >> 4U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_sink_w = 4U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r) 
                  >> 5U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_sink_w = 5U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r) 
                  >> 6U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_sink_w = 6U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r) 
                  >> 7U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_sink_w = 7U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w)) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r) 
            >> 8U))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_sink_w = 8U;
    }
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbgf_meta_r 
        = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbg_frame_a_r;
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
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_evt_r) 
                  >> 1U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_sink_w = 1U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_evt_r) 
                  >> 2U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_sink_w = 2U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_evt_r) 
                  >> 3U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_sink_w = 3U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_evt_r) 
                  >> 4U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_sink_w = 4U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_evt_r) 
                  >> 5U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_sink_w = 5U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_evt_r) 
                  >> 6U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_sink_w = 6U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_evt_r) 
                  >> 7U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_sink_w = 7U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w)) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_evt_r) 
            >> 8U))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_sink_w = 8U;
    }
    __Vtemp_41[0U] = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_vlan_r) 
                      << 0x00000010U);
    __Vtemp_41[1U] = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_seq_r) 
                       << 0x00000010U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_flags_r));
    __Vtemp_41[2U] = (IData)(((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_da_r 
                               << 0x00000010U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_cc_r))));
    __Vtemp_41[3U] = (IData)((((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_da_r 
                                << 0x00000010U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_cc_r))) 
                              >> 0x00000020U));
    __Vtemp_41[4U] = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_tkuid_r) 
                       << 0x00000010U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_lsuid_r));
    __Vtemp_41[5U] = (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_lseid_r);
    __Vtemp_41[6U] = (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_lseid_r 
                              >> 0x00000020U));
    __Vtemp_41[7U] = (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_tkeid_r);
    __Vtemp_41[8U] = (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_tkeid_r 
                              >> 0x00000020U));
    __Vtemp_41[9U] = (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_ctlr_r);
    __Vtemp_41[10U] = (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_ctlr_r 
                               >> 0x00000020U));
    __Vtemp_41[11U] = (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_sid_r);
    __Vtemp_41[12U] = (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_sid_r 
                               >> 0x00000020U));
    __Vtemp_41[13U] = (0xfc00002cU | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_msg_r) 
                                       << 0x00000010U) 
                                      | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_status_r) 
                                         << 0x0000000bU)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_pdu_byte_w 
        = (0x000000ffU & ((((0U == (0x0000001fU & ((IData)(0x01b8U) 
                                                   - 
                                                   ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_bidx_r) 
                                                    << 3U))))
                             ? 0U : (__Vtemp_41[(((IData)(7U) 
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
                           | (__Vtemp_41[(0x0000000fU 
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
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__p1_w 
        = (7U & (((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pos_r)) 
                 & (- (IData)((2U != (7U & ((IData)(1U) 
                                            + (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pos_r))))))));
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
        if (vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bpop_w) {
            vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__curr_r 
                = (0x00ffffffU & (IData)((vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r
                                          [vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__brd_r] 
                                          >> 0x00000018U)));
            vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__curl_r 
                = (0x00ffffffU & (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r
                                         [vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__brd_r]));
            vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__brd_r 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__brd_r)));
        }
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
                vlSelfRef.milan_datapath__DOT__avtprx_idx 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__match_idx;
            }
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
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_valid_w = 0U;
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_valid_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_cancel_w 
                = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[1U] 
                         >> 0x0000000fU));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w 
                = (0x0000007fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[1U] 
                                  >> 8U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_owner_w 
                = (0x000000ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[1U]);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_deadline_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[0U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[0U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[2U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[1U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[1U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[3U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[2U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[2U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[4U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[3U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[3U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[5U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[4U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[4U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[4U]) 
                   | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[5U] 
                      >> 0x00000010U));
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
                = (IData)((0x0000ffffffffffffULL & 
                           (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                             << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U])))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[1U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[1U]) 
                   | (IData)(((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U])))) 
                              >> 0x00000020U)));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
             & (1U == (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[1U] 
                = ((0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[1U]) 
                   | ((IData)((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U]))))) 
                      << 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[2U] 
                = (((IData)((0x0000ffffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                 << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U]))))) 
                    >> 0x00000010U) | ((IData)(((0x0000ffffffffffffULL 
                                                 & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                                     << 0x00000020U) 
                                                    | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U])))) 
                                                >> 0x00000020U)) 
                                       << 0x00000010U));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
             & (2U == (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[3U] 
                = (IData)((0x0000ffffffffffffULL & 
                           (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                             << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U])))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[4U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[4U]) 
                   | (IData)(((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U])))) 
                              >> 0x00000020U)));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
             & (3U == (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[4U] 
                = ((0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[4U]) 
                   | ((IData)((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U]))))) 
                      << 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[5U] 
                = (((IData)((0x0000ffffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                 << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U]))))) 
                    >> 0x00000010U) | ((IData)(((0x0000ffffffffffffULL 
                                                 & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                                     << 0x00000020U) 
                                                    | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U])))) 
                                                >> 0x00000020U)) 
                                       << 0x00000010U));
        }
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_cancel_w 
                = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[7U] 
                         >> 0x0000000fU));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w 
                = (0x0000007fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[7U] 
                                  >> 8U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_owner_w 
                = (0x000000ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[7U]);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_deadline_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[6U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[6U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[8U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[7U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[7U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[9U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[8U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[8U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[10U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[9U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[9U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[11U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[10U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[10U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[10U]) 
                   | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[11U] 
                      >> 0x00000010U));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 1U) & (0U == (0x00000018U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[6U] 
                = (IData)((0x0000ffffffffffffULL & 
                           (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                             << 0x00000010U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                                >> 0x00000010U))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[7U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[7U]) 
                   | (IData)(((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                   << 0x00000010U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                     >> 0x00000010U))) 
                              >> 0x00000020U)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 1U) & (8U == (0x00000018U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[7U] 
                = ((0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[7U]) 
                   | ((IData)((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                   << 0x00000010U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                     >> 0x00000010U)))) 
                      << 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[8U] 
                = (((IData)((0x0000ffffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                 << 0x00000010U) | 
                                ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                 >> 0x00000010U)))) 
                    >> 0x00000010U) | ((IData)(((0x0000ffffffffffffULL 
                                                 & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                                     << 0x00000010U) 
                                                    | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                                       >> 0x00000010U))) 
                                                >> 0x00000020U)) 
                                       << 0x00000010U));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 1U) & (0x00000010U == (0x00000018U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[9U] 
                = (IData)((0x0000ffffffffffffULL & 
                           (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                             << 0x00000010U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                                >> 0x00000010U))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[10U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[10U]) 
                   | (IData)(((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                   << 0x00000010U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                     >> 0x00000010U))) 
                              >> 0x00000020U)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 1U) & (0x00000018U == (0x00000018U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[10U] 
                = ((0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[10U]) 
                   | ((IData)((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                   << 0x00000010U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                     >> 0x00000010U)))) 
                      << 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[11U] 
                = (((IData)((0x0000ffffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                 << 0x00000010U) | 
                                ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                 >> 0x00000010U)))) 
                    >> 0x00000010U) | ((IData)(((0x0000ffffffffffffULL 
                                                 & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U])) 
                                                     << 0x00000010U) 
                                                    | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U])) 
                                                       >> 0x00000010U))) 
                                                >> 0x00000020U)) 
                                       << 0x00000010U));
        }
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_cancel_w 
                = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[13U] 
                         >> 0x0000000fU));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w 
                = (0x0000007fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[13U] 
                                  >> 8U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_owner_w 
                = (0x000000ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[13U]);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_deadline_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[12U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[12U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[14U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[13U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[13U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[15U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[14U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[14U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[16U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[15U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[15U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[17U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[16U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[16U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[16U]) 
                   | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[17U] 
                      >> 0x00000010U));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 2U) & (0U == (0x000000c0U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[12U] 
                = (IData)((0x0000ffffffffffffULL & 
                           (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                             << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U])))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[13U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[13U]) 
                   | (IData)(((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U])))) 
                              >> 0x00000020U)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 2U) & (0x00000040U == (0x000000c0U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[13U] 
                = ((0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[13U]) 
                   | ((IData)((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U]))))) 
                      << 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[14U] 
                = (((IData)((0x0000ffffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                 << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U]))))) 
                    >> 0x00000010U) | ((IData)(((0x0000ffffffffffffULL 
                                                 & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                                     << 0x00000020U) 
                                                    | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U])))) 
                                                >> 0x00000020U)) 
                                       << 0x00000010U));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 2U) & (0x00000080U == (0x000000c0U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[15U] 
                = (IData)((0x0000ffffffffffffULL & 
                           (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                             << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U])))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[16U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[16U]) 
                   | (IData)(((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U])))) 
                              >> 0x00000020U)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 2U) & (0x000000c0U == (0x000000c0U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[16U] 
                = ((0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[16U]) 
                   | ((IData)((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U]))))) 
                      << 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[17U] 
                = (((IData)((0x0000ffffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                 << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U]))))) 
                    >> 0x00000010U) | ((IData)(((0x0000ffffffffffffULL 
                                                 & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                                     << 0x00000020U) 
                                                    | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U])))) 
                                                >> 0x00000020U)) 
                                       << 0x00000010U));
        }
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_cancel_w 
                = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[19U] 
                         >> 0x0000000fU));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w 
                = (0x0000007fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[19U] 
                                  >> 8U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_owner_w 
                = (0x000000ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[19U]);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_deadline_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[18U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[18U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[20U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[19U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[19U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[21U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[20U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[20U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[22U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[21U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[21U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[23U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[22U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[22U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[22U]) 
                   | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[23U] 
                      >> 0x00000010U));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 3U) & (0U == (0x00000600U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[18U] 
                = (IData)((0x0000ffffffffffffULL & 
                           (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                             << 0x00000010U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                                >> 0x00000010U))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[19U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[19U]) 
                   | (IData)(((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                   << 0x00000010U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                     >> 0x00000010U))) 
                              >> 0x00000020U)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 3U) & (0x00000200U == (0x00000600U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[19U] 
                = ((0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[19U]) 
                   | ((IData)((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                   << 0x00000010U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                     >> 0x00000010U)))) 
                      << 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[20U] 
                = (((IData)((0x0000ffffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                 << 0x00000010U) | 
                                ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                 >> 0x00000010U)))) 
                    >> 0x00000010U) | ((IData)(((0x0000ffffffffffffULL 
                                                 & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                                     << 0x00000010U) 
                                                    | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                                       >> 0x00000010U))) 
                                                >> 0x00000020U)) 
                                       << 0x00000010U));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 3U) & (0x00000400U == (0x00000600U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[21U] 
                = (IData)((0x0000ffffffffffffULL & 
                           (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                             << 0x00000010U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                                >> 0x00000010U))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[22U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[22U]) 
                   | (IData)(((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                   << 0x00000010U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                     >> 0x00000010U))) 
                              >> 0x00000020U)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 3U) & (0x00000600U == (0x00000600U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[22U] 
                = ((0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[22U]) 
                   | ((IData)((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                   << 0x00000010U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                     >> 0x00000010U)))) 
                      << 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[23U] 
                = (((IData)((0x0000ffffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                 << 0x00000010U) | 
                                ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                 >> 0x00000010U)))) 
                    >> 0x00000010U) | ((IData)(((0x0000ffffffffffffULL 
                                                 & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U])) 
                                                     << 0x00000010U) 
                                                    | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U])) 
                                                       >> 0x00000010U))) 
                                                >> 0x00000020U)) 
                                       << 0x00000010U));
        }
        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_cancel_w 
                = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[25U] 
                         >> 0x0000000fU));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w 
                = (0x0000007fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[25U] 
                                  >> 8U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_owner_w 
                = (0x000000ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[25U]);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_deadline_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[24U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[24U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[26U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[25U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[25U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[27U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[26U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[26U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[28U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[27U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[27U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[29U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[28U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[28U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[28U]) 
                   | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[29U] 
                      >> 0x00000010U));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 4U) & (0U == (0x00003000U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[24U] 
                = (IData)((0x0000ffffffffffffULL & 
                           (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                             << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U])))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[25U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[25U]) 
                   | (IData)(((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U])))) 
                              >> 0x00000020U)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 4U) & (0x00001000U == (0x00003000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[25U] 
                = ((0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[25U]) 
                   | ((IData)((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U]))))) 
                      << 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[26U] 
                = (((IData)((0x0000ffffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                 << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U]))))) 
                    >> 0x00000010U) | ((IData)(((0x0000ffffffffffffULL 
                                                 & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                                     << 0x00000020U) 
                                                    | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U])))) 
                                                >> 0x00000020U)) 
                                       << 0x00000010U));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 4U) & (0x00002000U == (0x00003000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[27U] 
                = (IData)((0x0000ffffffffffffULL & 
                           (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                             << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U])))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[28U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[28U]) 
                   | (IData)(((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U])))) 
                              >> 0x00000020U)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 4U) & (0x00003000U == (0x00003000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[28U] 
                = ((0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[28U]) 
                   | ((IData)((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U]))))) 
                      << 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[29U] 
                = (((IData)((0x0000ffffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                 << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U]))))) 
                    >> 0x00000010U) | ((IData)(((0x0000ffffffffffffULL 
                                                 & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                                     << 0x00000020U) 
                                                    | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U])))) 
                                                >> 0x00000020U)) 
                                       << 0x00000010U));
        }
        if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_cancel_w 
                = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[31U] 
                         >> 0x0000000fU));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w 
                = (0x0000007fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[31U] 
                                  >> 8U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_owner_w 
                = (0x000000ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[31U]);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_deadline_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[30U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[30U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[32U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[31U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[31U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[33U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[32U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[32U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[34U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[33U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[33U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[35U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[34U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[34U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[34U]) 
                   | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[35U] 
                      >> 0x00000010U));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 5U) & (0U == (0x00018000U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[30U] 
                = (IData)((0x0000ffffffffffffULL & 
                           (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                             << 0x00000010U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                                >> 0x00000010U))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[31U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[31U]) 
                   | (IData)(((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                   << 0x00000010U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                     >> 0x00000010U))) 
                              >> 0x00000020U)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 5U) & (0x00008000U == (0x00018000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[31U] 
                = ((0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[31U]) 
                   | ((IData)((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                   << 0x00000010U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                     >> 0x00000010U)))) 
                      << 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[32U] 
                = (((IData)((0x0000ffffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                 << 0x00000010U) | 
                                ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                 >> 0x00000010U)))) 
                    >> 0x00000010U) | ((IData)(((0x0000ffffffffffffULL 
                                                 & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                                     << 0x00000010U) 
                                                    | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                                       >> 0x00000010U))) 
                                                >> 0x00000020U)) 
                                       << 0x00000010U));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 5U) & (0x00010000U == (0x00018000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[33U] 
                = (IData)((0x0000ffffffffffffULL & 
                           (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                             << 0x00000010U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                                >> 0x00000010U))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[34U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[34U]) 
                   | (IData)(((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                   << 0x00000010U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                     >> 0x00000010U))) 
                              >> 0x00000020U)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 5U) & (0x00018000U == (0x00018000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[34U] 
                = ((0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[34U]) 
                   | ((IData)((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                   << 0x00000010U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                     >> 0x00000010U)))) 
                      << 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[35U] 
                = (((IData)((0x0000ffffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                 << 0x00000010U) | 
                                ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                 >> 0x00000010U)))) 
                    >> 0x00000010U) | ((IData)(((0x0000ffffffffffffULL 
                                                 & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U])) 
                                                     << 0x00000010U) 
                                                    | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U])) 
                                                       >> 0x00000010U))) 
                                                >> 0x00000020U)) 
                                       << 0x00000010U));
        }
        if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_cancel_w 
                = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[37U] 
                         >> 0x0000000fU));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w 
                = (0x0000007fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[37U] 
                                  >> 8U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_owner_w 
                = (0x000000ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[37U]);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_deadline_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[36U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[36U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[38U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[37U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[37U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[39U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[38U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[38U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[40U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[39U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[39U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[41U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[40U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[40U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[40U]) 
                   | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[41U] 
                      >> 0x00000010U));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 6U) & (0U == (0x000c0000U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[36U] 
                = (IData)((0x0000ffffffffffffULL & 
                           (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                             << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U])))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[37U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[37U]) 
                   | (IData)(((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U])))) 
                              >> 0x00000020U)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 6U) & (0x00040000U == (0x000c0000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[37U] 
                = ((0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[37U]) 
                   | ((IData)((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U]))))) 
                      << 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[38U] 
                = (((IData)((0x0000ffffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                 << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U]))))) 
                    >> 0x00000010U) | ((IData)(((0x0000ffffffffffffULL 
                                                 & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                                     << 0x00000020U) 
                                                    | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U])))) 
                                                >> 0x00000020U)) 
                                       << 0x00000010U));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 6U) & (0x00080000U == (0x000c0000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[39U] 
                = (IData)((0x0000ffffffffffffULL & 
                           (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                             << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U])))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[40U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[40U]) 
                   | (IData)(((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U])))) 
                              >> 0x00000020U)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 6U) & (0x000c0000U == (0x000c0000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[40U] 
                = ((0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[40U]) 
                   | ((IData)((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U]))))) 
                      << 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[41U] 
                = (((IData)((0x0000ffffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                 << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U]))))) 
                    >> 0x00000010U) | ((IData)(((0x0000ffffffffffffULL 
                                                 & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                                     << 0x00000020U) 
                                                    | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U])))) 
                                                >> 0x00000020U)) 
                                       << 0x00000010U));
        }
        if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_valid_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_cancel_w 
                = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[43U] 
                         >> 0x0000000fU));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w 
                = (0x0000007fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[43U] 
                                  >> 8U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_owner_w 
                = (0x000000ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[43U]);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_deadline_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[42U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[42U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[44U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[43U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[43U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[45U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[44U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[44U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[46U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[45U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[45U] 
                = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[47U] 
                    << 0x00000010U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[46U] 
                                       >> 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[46U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[46U]) 
                   | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[47U] 
                      >> 0x00000010U));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 7U) & (0U == (0x00600000U 
                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[42U] 
                = (IData)((0x0000ffffffffffffULL & 
                           (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                             << 0x00000010U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                                >> 0x00000010U))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[43U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[43U]) 
                   | (IData)(((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                                   << 0x00000010U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                     >> 0x00000010U))) 
                              >> 0x00000020U)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 7U) & (0x00200000U == (0x00600000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[43U] 
                = ((0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[43U]) 
                   | ((IData)((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                                   << 0x00000010U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                     >> 0x00000010U)))) 
                      << 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[44U] 
                = (((IData)((0x0000ffffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                                 << 0x00000010U) | 
                                ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                 >> 0x00000010U)))) 
                    >> 0x00000010U) | ((IData)(((0x0000ffffffffffffULL 
                                                 & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                                                     << 0x00000010U) 
                                                    | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                                       >> 0x00000010U))) 
                                                >> 0x00000020U)) 
                                       << 0x00000010U));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 7U) & (0x00400000U == (0x00600000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[45U] 
                = (IData)((0x0000ffffffffffffULL & 
                           (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                             << 0x00000010U) | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                                >> 0x00000010U))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[46U] 
                = ((0xffff0000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[46U]) 
                   | (IData)(((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                                   << 0x00000010U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                     >> 0x00000010U))) 
                              >> 0x00000020U)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w) 
                      >> 7U) & (0x00600000U == (0x00600000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[46U] 
                = ((0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[46U]) 
                   | ((IData)((0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                                   << 0x00000010U) 
                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                     >> 0x00000010U)))) 
                      << 0x00000010U));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[47U] 
                = (((IData)((0x0000ffffffffffffULL 
                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                                 << 0x00000010U) | 
                                ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                 >> 0x00000010U)))) 
                    >> 0x00000010U) | ((IData)(((0x0000ffffffffffffULL 
                                                 & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U])) 
                                                     << 0x00000010U) 
                                                    | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U])) 
                                                       >> 0x00000010U))) 
                                                >> 0x00000020U)) 
                                       << 0x00000010U));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__noadp_exp_w) {
            if ((8U >= (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                       - (IData)(1U))))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r 
                    = ((~ ((IData)(1U) << (0x0000000fU 
                                           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                              - (IData)(1U))))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r));
            }
        }
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r 
                = (0x01feU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r));
        }
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r 
                = (0x01fdU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r));
        }
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r 
                = (0x01fbU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r));
        }
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r 
                = (0x01f7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r));
        }
        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r 
                = (0x01efU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r));
        }
        if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r 
                = (0x01dfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r));
        }
        if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r 
                = (0x01bfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r));
        }
        if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r 
                = (0x017fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r));
        }
        if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r 
                = (0x00ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__st_set_w) {
            if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r) 
                       | (0x01ffU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r))));
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__st_clr_w) {
            if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r));
            }
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
            if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sink_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__dirty_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sink_r))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__dirty_r));
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_wr_w) {
            if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__dirty_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__dirty_r) 
                       | (0x01ffU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r))));
            }
        }
        vlSelfRef.milan_datapath__DOT__src_recentre_q_r 
            = vlSelfRef.milan_datapath__DOT__media_clk_src_r;
        if (vlSelfRef.milan_datapath__DOT__crf_clk_selected_r) {
            if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__engaged_r)) 
                       | (0x208cU <= (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__quiet_r))))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__media_grid_align__DOT__quiet_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__aafcap_pv_w)
                        ? 0U : (0x00003fffU & ((0x208cU 
                                                <= (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__quiet_r))
                                                ? (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__quiet_r)
                                                : ((IData)(1U) 
                                                   + (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__quiet_r)))));
                if (vlSelfRef.milan_datapath__DOT__aafcap_pv_w) {
                    vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__ref_r 
                        = vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__tst_next_w;
                }
                vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__tst_r 
                    = vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__tst_next_w;
                vlSelfRef.__Vdly__milan_datapath__DOT__media_grid_align__DOT__slip_r = 0U;
                vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__engaged_r 
                    = vlSelfRef.milan_datapath__DOT__aafcap_pv_w;
                vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__err_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__media_grid_align__DOT__acc_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__mnco_servo_trim_w = 0U;
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__media_grid_align__DOT__quiet_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__aafcap_pv_w)
                        ? 0U : (0x00003fffU & ((IData)(1U) 
                                               + (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__quiet_r))));
                if (vlSelfRef.milan_datapath__DOT__aafcap_pv_w) {
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
                        __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_acc__267__v 
                            = (vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__acc_r 
                               + vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__err_w);
                        __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_acc__267__Vfuncout 
                            = (VL_LTS_III(32, 0x00c80000U, __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_acc__267__v)
                                ? 0x00c80000U : (VL_GTS_III(32, 0xff380000U, __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_acc__267__v)
                                                  ? 0xff380000U
                                                  : __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_acc__267__v));
                        vlSelfRef.__Vdly__milan_datapath__DOT__media_grid_align__DOT__acc_r 
                            = __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_acc__267__Vfuncout;
                    }
                    __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_u__268__v 
                        = (VL_MULS_III(32, (IData)(0xffffffffU), 
                                       (vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__err_w 
                                        << 2U)) - VL_SHIFTRS_III(32,32,32, vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__acc_r, 0x0000000cU));
                    vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__err_r 
                        = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__err_w);
                    __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_u__268__Vfuncout 
                        = (VL_LTS_III(32, 0x00000c80U, __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_u__268__v)
                            ? 0x00000c80U : (VL_GTS_III(32, 0xfffff380U, __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_u__268__v)
                                              ? 0x0000f380U
                                              : (0x0000ffffU 
                                                 & __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_u__268__v)));
                    vlSelfRef.__Vdly__milan_datapath__DOT__mnco_servo_trim_w 
                        = __Vfunc_milan_datapath__DOT__media_grid_align__DOT__clamp_u__268__Vfuncout;
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
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_txp_q_r 
            = ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__ltap_txmac_w) 
                 << 3U) | (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__aaf_tx_acc_w) 
                            & (IData)(vlSelfRef.milan_datapath__DOT__aaf_tx_tlast)) 
                           << 2U)) | ((((~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__aaf_tx_inframe_r)) 
                                        & (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__aaf_tx_acc_w)) 
                                       << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__aafcap_pv_w)));
        vlSelfRef.milan_datapath__DOT__csr__DOT__ltap_clr_p = 0U;
        if (vlSelfRef.s_axi_awready) {
            if ((0x0920U != (IData)(vlSelfRef.s_axi_awaddr))) {
                if ((0x0934U == (IData)(vlSelfRef.s_axi_awaddr))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_sel_r 
                        = (0x0000003fU & vlSelfRef.s_axi_wdata);
                }
            }
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
                                            }
                                        }
                                    }
                                }
                            }
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
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_rxp_q_r 
            = (((((IData)(vlSelfRef.milan_datapath__DOT__rend_pcm_tvalid_w) 
                  & (IData)(vlSelfRef.milan_datapath__DOT__dpkt_pcm_tlast_w)) 
                 << 3U) | (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w) 
                            & (IData)(vlSelfRef.milan_datapath__DOT__dpkt_pcm_tlast_w)) 
                           << 2U)) | (((IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_p) 
                                       << 1U) | ((~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__mac_rx_inframe_r)) 
                                                 & (IData)(vlSelfRef.s_axis_mac_rx_tvalid))));
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
        if (vlSelfRef.milan_datapath__DOT__rsp_render_tick_p_w) {
            vlSelfRef.milan_datapath__DOT__chmap_phys_w[0U] 
                = ((0xff000000U & vlSelfRef.milan_datapath__DOT__chmap_phys_w[0U]) 
                   | ((1U & ((vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[0U] 
                              >> 7U) & (~ (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[0U] 
                                           >> 6U))))
                       ? vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[0U]
                       : 0U));
            vlSelfRef.milan_datapath__DOT__chmap_phys_w[0U] 
                = ((0x00ffffffU & vlSelfRef.milan_datapath__DOT__chmap_phys_w[0U]) 
                   | (((1U & ((vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[1U] 
                               >> 7U) & (~ (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[1U] 
                                            >> 6U))))
                        ? vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[1U]
                        : 0U) << 0x00000018U));
            vlSelfRef.milan_datapath__DOT__chmap_phys_w[1U] 
                = ((0xffff0000U & vlSelfRef.milan_datapath__DOT__chmap_phys_w[1U]) 
                   | (((1U & ((vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[1U] 
                               >> 7U) & (~ (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[1U] 
                                            >> 6U))))
                        ? vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[1U]
                        : 0U) >> 8U));
            vlSelfRef.milan_datapath__DOT__chmap_phys_w[1U] 
                = ((0x0000ffffU & vlSelfRef.milan_datapath__DOT__chmap_phys_w[1U]) 
                   | (((1U & ((vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[2U] 
                               >> 7U) & (~ (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[2U] 
                                            >> 6U))))
                        ? vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[2U]
                        : 0U) << 0x00000010U));
            vlSelfRef.milan_datapath__DOT__chmap_phys_w[2U] 
                = ((0xffffff00U & vlSelfRef.milan_datapath__DOT__chmap_phys_w[2U]) 
                   | (((1U & ((vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[2U] 
                               >> 7U) & (~ (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[2U] 
                                            >> 6U))))
                        ? vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[2U]
                        : 0U) >> 0x00000010U));
            vlSelfRef.milan_datapath__DOT__chmap_phys_w[2U] 
                = ((0x000000ffU & vlSelfRef.milan_datapath__DOT__chmap_phys_w[2U]) 
                   | (((1U & ((vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[3U] 
                               >> 7U) & (~ (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[3U] 
                                            >> 6U))))
                        ? vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[3U]
                        : 0U) << 8U));
            vlSelfRef.milan_datapath__DOT__chmap_phys_w[3U] 
                = ((0xff000000U & vlSelfRef.milan_datapath__DOT__chmap_phys_w[3U]) 
                   | ((1U & ((vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[4U] 
                              >> 7U) & (~ (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[4U] 
                                           >> 6U))))
                       ? vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[4U]
                       : 0U));
            vlSelfRef.milan_datapath__DOT__chmap_phys_w[3U] 
                = ((0x00ffffffU & vlSelfRef.milan_datapath__DOT__chmap_phys_w[3U]) 
                   | (((1U & ((vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[5U] 
                               >> 7U) & (~ (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[5U] 
                                            >> 6U))))
                        ? vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[5U]
                        : 0U) << 0x00000018U));
            vlSelfRef.milan_datapath__DOT__chmap_phys_w[4U] 
                = ((0xffff0000U & vlSelfRef.milan_datapath__DOT__chmap_phys_w[4U]) 
                   | (((1U & ((vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[5U] 
                               >> 7U) & (~ (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[5U] 
                                            >> 6U))))
                        ? vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[5U]
                        : 0U) >> 8U));
            vlSelfRef.milan_datapath__DOT__chmap_phys_w[4U] 
                = ((0x0000ffffU & vlSelfRef.milan_datapath__DOT__chmap_phys_w[4U]) 
                   | (((1U & ((vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[6U] 
                               >> 7U) & (~ (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[6U] 
                                            >> 6U))))
                        ? vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[6U]
                        : 0U) << 0x00000010U));
            vlSelfRef.milan_datapath__DOT__chmap_phys_w[5U] 
                = ((0xffffff00U & vlSelfRef.milan_datapath__DOT__chmap_phys_w[5U]) 
                   | (((1U & ((vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[6U] 
                               >> 7U) & (~ (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[6U] 
                                            >> 6U))))
                        ? vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[6U]
                        : 0U) >> 0x00000010U));
            vlSelfRef.milan_datapath__DOT__chmap_phys_w[5U] 
                = ((0x000000ffU & vlSelfRef.milan_datapath__DOT__chmap_phys_w[5U]) 
                   | (((1U & ((vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[7U] 
                               >> 7U) & (~ (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[7U] 
                                            >> 6U))))
                        ? vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[7U]
                        : 0U) << 8U));
            vlSelfRef.milan_datapath__DOT__chmap_phys_w[6U] 
                = ((0xff000000U & vlSelfRef.milan_datapath__DOT__chmap_phys_w[6U]) 
                   | ((1U & ((vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[8U] 
                              >> 7U) & (~ (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[8U] 
                                           >> 6U))))
                       ? vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[8U]
                       : 0U));
            vlSelfRef.milan_datapath__DOT__chmap_phys_w[6U] 
                = ((0x00ffffffU & vlSelfRef.milan_datapath__DOT__chmap_phys_w[6U]) 
                   | (((1U & ((vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[9U] 
                               >> 7U) & (~ (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[9U] 
                                            >> 6U))))
                        ? vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[9U]
                        : 0U) << 0x00000018U));
            vlSelfRef.milan_datapath__DOT__chmap_phys_w[7U] 
                = (0x0000ffffU & (((1U & ((vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[9U] 
                                           >> 7U) & 
                                          (~ (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[9U] 
                                              >> 6U))))
                                    ? vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[9U]
                                    : 0U) >> 8U));
        }
        vlSelfRef.milan_datapath__DOT__cmap_rd_valid_w = 0U;
        if (vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_capture__map_rd_en_i) {
            vlSelfRef.milan_datapath__DOT__cmap_rd_valid_w = 1U;
            vlSelfRef.milan_datapath__DOT__cmap_rd_data_w 
                = (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_fed_r) 
                    << 0x0000000eU) | (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w) 
                                        << 0x0000000dU) 
                                       | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                       [vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r]));
        }
        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r 
            = (0x0000ffffU & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_next_w));
        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_done_p = 0U;
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__beat_w) {
            vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r 
                = ((7U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r))
                    ? 7U : (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r))));
            if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r))) {
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__191__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__194__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_1__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__191__w 
                                              >> 0x20U)));
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_4__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__194__w 
                                              >> 0x38U)));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__192__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_msg_r 
                    = (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_4__lane));
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_2__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__192__w 
                                              >> 0x28U)));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__193__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_3__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__193__w 
                                              >> 0x30U)));
                vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__is_maap_r 
                    = (((0x22U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_1__lane)) 
                        & (0xf0U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_2__lane))) 
                       & (0xfeU == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_3__lane)));
            }
            if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r))) {
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__195__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_5__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__195__w 
                                              >> 0x10U)));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__196__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_6__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__196__w 
                                              >> 0x18U)));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__197__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_7__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__197__w 
                                              >> 0x20U)));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__198__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_8__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__198__w 
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
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__199__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_9__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__199__w 
                                              >> 0x30U)));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__200__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_10__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__200__w 
                                              >> 0x38U)));
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_start_r 
                    = ((0x0000ffffffff0000ULL & vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_start_r) 
                       | (IData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_9__lane) 
                                           << 8U) | (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_10__lane)))));
            }
            if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r))) {
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__201__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__203__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_11__lane 
                    = (0x000000ffU & (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__201__w));
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_13__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__203__w 
                                              >> 0x10U)));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__202__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__204__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_12__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__202__w 
                                              >> 8U)));
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_14__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__204__w 
                                              >> 0x18U)));
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_cnt_r 
                    = (((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_11__lane) 
                        << 8U) | (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_12__lane));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__205__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_15__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__205__w 
                                              >> 0x20U)));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__206__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_16__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__206__w 
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
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__207__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_17__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__207__w 
                                              >> 0x30U)));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__208__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_18__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__208__w 
                                              >> 0x38U)));
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_conf_start_r 
                    = ((0x0000ffffffff0000ULL & vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_conf_start_r) 
                       | (IData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_17__lane) 
                                           << 8U) | (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_18__lane)))));
            }
            if ((5U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r))) {
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__209__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_19__lane 
                    = (0x000000ffU & (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__209__w));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__210__w 
                    = vlSelfRef.s_axis_mac_rx_tdata;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_20__lane 
                    = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lane__210__w 
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
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_la_mvrp_r = 0U;
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r) {
                if ((0x6bU >= (0x0000007fU & ((IData)(0x0000000cU) 
                                              * (0x0000000fU 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) {
                    VL_ASSIGNSEL_WI(108, 12, (0x0000007fU 
                                              & ((IData)(0x0000000cU) 
                                                 * 
                                                 (0x0000000fU 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))), vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_vid_r);
                }
            }
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_q2_r 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_q1_r;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__iv_bytes_r 
            = (0x00000001ffffffffULL & ((QData)((IData)(
                                                        ((0x8fU 
                                                          >= 
                                                          (0x000000ffU 
                                                           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_q1_r) 
                                                              << 4U)))
                                                          ? 
                                                         (0x0000ffffU 
                                                          & (((0U 
                                                               == 
                                                               (0x0000001fU 
                                                                & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_q1_r) 
                                                                   << 4U)))
                                                               ? 0U
                                                               : 
                                                              (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_mif_r
                                                               [
                                                               (((IData)(0x0000000fU) 
                                                                 + 
                                                                 (0x000000ffU 
                                                                  & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_q1_r) 
                                                                     << 4U))) 
                                                                >> 5U)] 
                                                               << 
                                                               ((IData)(0x00000020U) 
                                                                - 
                                                                (0x0000001fU 
                                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_q1_r) 
                                                                    << 4U))))) 
                                                             | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_mif_r
                                                                [
                                                                (7U 
                                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_q1_r) 
                                                                    >> 1U))] 
                                                                >> 
                                                                (0x0000001fU 
                                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_q1_r) 
                                                                    << 4U)))))
                                                          : 0U))) 
                                        * (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__frame_bytes_r))));
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
            if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_waddr_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__declaring_r 
                    = (((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_waddr_w))) 
                        & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__declaring_r)) 
                       | (0x01ffU & ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[2U] 
                                                   >> 0x00000012U))) 
                                     << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_waddr_w))));
            }
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
                    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r))) {
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
                                               * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246)))))) {
                        vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__pend_r__v0 
                            = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
                        vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__pend_r__v0 = 1U;
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
                                            * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246))))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__eiss_r 
                            = (0x0000001fU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eiss_r)));
                        if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eo_r) 
                             == ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246) 
                                 - (IData)(1U)))) {
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
                            vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v0 
                                = (0x00ffffffU & (IData)(
                                                         (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__stg_q_r 
                                                          >> 0x18U)));
                            vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v0 
                                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ecap_r;
                            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v0 = 1U;
                            vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r__v0 
                                = (0x00ffffffU & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__stg_q_r));
                            vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r__v0 
                                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ecap_r;
                            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r__v0 = 1U;
                        }
                        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__ecap_r 
                            = (0x0000001fU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ecap_r)));
                        if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ecap_r) 
                             == (0x0000001fU & (((IData)(6U) 
                                                 * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246)) 
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
            if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_v_w) {
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r 
                    = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w;
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__etu_r 
                    = vlSelfRef.milan_datapath__DOT__clkv_tu_w;
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__emr_r 
                    = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__mcr_mr_v_w) 
                             >> (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w)));
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ebank_r 
                    = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__wbank_r
                                       [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w])));
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__rr_r 
                    = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w;
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__est_r 
                    = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w))
                        ? 2U : 1U);
            }
        }
        if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__stg_we_w) {
            if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__own_last_w) {
                if ((5U == vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r
                     [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v0 
                        = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__wbank_r
                                           [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w])));
                    vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v0 
                        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w;
                    vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v0 = 1U;
                    vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v0 
                        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w;
                    vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__pend_r__v1 
                        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w;
                } else {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v1 
                        = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r
                                                       [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w])));
                    vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v1 
                        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w;
                    vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v1 = 1U;
                }
            }
            if (((0U == vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r
                  [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w]) 
                 & (0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__tsw_pend_r = 1U;
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tsw_t_r 
                    = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w;
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tsw_val_r 
                    = (((vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[1U] 
                         << 8U) | (vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[0U] 
                                   >> 0x00000018U)) 
                       + vlSelfRef.milan_datapath__DOT____Vcellinp__aaf_packetizer__transit_ns_i
                       [(7U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w))]);
            }
        }
        if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_stream_en_w)))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v2 = 1U;
        }
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__aaf_stream_en_w) 
                      >> 1U)))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v3 = 1U;
        }
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__aaf_stream_en_w) 
                      >> 2U)))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v4 = 1U;
        }
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__aaf_stream_en_w) 
                      >> 3U)))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v5 = 1U;
        }
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__aaf_stream_en_w) 
                      >> 4U)))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v6 = 1U;
        }
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__aaf_stream_en_w) 
                      >> 5U)))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v7 = 1U;
        }
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__aaf_stream_en_w) 
                      >> 6U)))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v8 = 1U;
        }
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__aaf_stream_en_w) 
                      >> 7U)))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v9 = 1U;
        }
        vlSelfRef.milan_datapath__DOT__avtprx_dirty_p_w = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_accept_p_w = 0U;
        vlSelfRef.milan_datapath__DOT__lctx_rd_valid_w = 0U;
        if ((1U == ((((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__penq_w) 
                      & (~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pdisp_new_w))) 
                     << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pdisp_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v0[0U] 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][0U];
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v0[1U] 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][1U];
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v0[2U] 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][2U];
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v0[3U] 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][3U];
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v0[4U] 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][4U];
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v0 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r 
                = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r) 
                         - (IData)(1U)));
        } else if ((2U == ((((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__penq_w) 
                             & (~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pdisp_new_w))) 
                            << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pdisp_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1[0U] 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[0U];
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1[1U] 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[1U];
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1[2U] 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[2U];
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1[3U] 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[3U];
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1[4U] 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[4U];
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1 
                = (1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r 
                = (3U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r)));
        } else if ((3U == ((((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__penq_w) 
                             & (~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pdisp_new_w))) 
                            << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pdisp_w)))) {
            if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v2[0U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[0U];
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v2[1U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[1U];
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v2[2U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[2U];
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v2[3U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[3U];
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v2[4U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[4U];
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v2 = 1U;
            } else {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v3[0U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][0U];
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v3[1U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][1U];
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v3[2U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][2U];
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v3[3U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][3U];
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v3[4U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][4U];
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v3 = 1U;
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v4[0U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[0U];
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v4[1U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[1U];
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v4[2U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[2U];
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v4[3U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[3U];
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v4[4U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[4U];
            }
        }
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_rise_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r 
                = (1U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r));
        }
        if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r 
                = (1U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdu_p_w) 
              & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdu_idx_w))) 
             & (~ (7U == vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[0U])))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v0 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[0U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v0 = 1U;
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__overflow_reg) 
              & (0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__tl_idx_r))) 
             & (~ (7U == vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[0U])))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v0 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[0U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v0 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ms_tick_r) 
             & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r))) {
            if ((0x63U <= vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[0U])) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r 
                    = (1U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r));
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v0 = 1U;
            } else {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v1 
                    = (0x0000007fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[0U])));
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v1 = 1U;
            }
        }
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_rise_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r 
                = (2U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r));
        }
        if ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r 
                = (2U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdu_p_w) 
              & (1U == (IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdu_idx_w))) 
             & (~ (7U == vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[1U])))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v1 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[1U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v1 = 1U;
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__overflow_reg) 
              & (1U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__tl_idx_r))) 
             & (~ (7U == vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[1U])))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v1 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[1U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v1 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ms_tick_r) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r) 
                >> 1U))) {
            if ((0x63U <= vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[1U])) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r 
                    = (2U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r));
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v2 = 1U;
            } else {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v3 
                    = (0x0000007fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[1U])));
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v3 = 1U;
            }
        }
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_rise_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r 
                = (4U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r));
        }
        if ((4U & ((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r 
                = (4U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdu_p_w) 
              & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdu_idx_w))) 
             & (~ (7U == vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[2U])))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v2 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[2U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v2 = 1U;
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__overflow_reg) 
              & (2U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__tl_idx_r))) 
             & (~ (7U == vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[2U])))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v2 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[2U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v2 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ms_tick_r) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r) 
                >> 2U))) {
            if ((0x63U <= vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[2U])) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r 
                    = (4U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r));
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v4 = 1U;
            } else {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v5 
                    = (0x0000007fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[2U])));
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v5 = 1U;
            }
        }
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_rise_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r 
                = (8U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r));
        }
        if ((8U & ((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r 
                = (8U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdu_p_w) 
              & (3U == (IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdu_idx_w))) 
             & (~ (7U == vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[3U])))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v3 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[3U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v3 = 1U;
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__overflow_reg) 
              & (3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__tl_idx_r))) 
             & (~ (7U == vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[3U])))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v3 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[3U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v3 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ms_tick_r) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r) 
                >> 3U))) {
            if ((0x63U <= vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[3U])) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r 
                    = (8U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r));
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v6 = 1U;
            } else {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v7 
                    = (0x0000007fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[3U])));
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v7 = 1U;
            }
        }
        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_rise_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r 
                = (0x00000010U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r));
        }
        if ((0x00000010U & ((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
                            & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r 
                = (0x00000010U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdu_p_w) 
              & (4U == (IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdu_idx_w))) 
             & (~ (7U == vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[4U])))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v4 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[4U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v4 = 1U;
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__overflow_reg) 
              & (4U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__tl_idx_r))) 
             & (~ (7U == vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[4U])))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v4 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[4U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v4 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ms_tick_r) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r) 
                >> 4U))) {
            if ((0x63U <= vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[4U])) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r 
                    = (0x00000010U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r));
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v8 = 1U;
            } else {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v9 
                    = (0x0000007fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[4U])));
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v9 = 1U;
            }
        }
        if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_rise_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r 
                = (0x00000020U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r));
        }
        if ((0x00000020U & ((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
                            & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r 
                = (0x00000020U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdu_p_w) 
              & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdu_idx_w))) 
             & (~ (7U == vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[5U])))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v5 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[5U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v5 = 1U;
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__overflow_reg) 
              & (5U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__tl_idx_r))) 
             & (~ (7U == vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[5U])))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v5 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[5U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v5 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ms_tick_r) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r) 
                >> 5U))) {
            if ((0x63U <= vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[5U])) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r 
                    = (0x00000020U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r));
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v10 = 1U;
            } else {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v11 
                    = (0x0000007fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[5U])));
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v11 = 1U;
            }
        }
        if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_rise_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r 
                = (0x00000040U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r));
        }
        if ((0x00000040U & ((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
                            & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r 
                = (0x00000040U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdu_p_w) 
              & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdu_idx_w))) 
             & (~ (7U == vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[6U])))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v6 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[6U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v6 = 1U;
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__overflow_reg) 
              & (6U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__tl_idx_r))) 
             & (~ (7U == vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[6U])))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v6 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[6U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v6 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ms_tick_r) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r) 
                >> 6U))) {
            if ((0x63U <= vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[6U])) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r 
                    = (0x00000040U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r));
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v12 = 1U;
            } else {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v13 
                    = (0x0000007fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[6U])));
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v13 = 1U;
            }
        }
        if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_rise_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r 
                = (0x00000080U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r));
        }
        if ((0x00000080U & ((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
                            & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r 
                = (0x00000080U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdu_p_w) 
              & (7U == (IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdu_idx_w))) 
             & (~ (7U == vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[7U])))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v7 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[7U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v7 = 1U;
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__overflow_reg) 
              & (7U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__tl_idx_r))) 
             & (~ (7U == vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[7U])))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v7 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[7U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v7 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ms_tick_r) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r) 
                >> 7U))) {
            if ((0x63U <= vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[7U])) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r 
                    = (0x00000080U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r));
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v14 = 1U;
            } else {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v15 
                    = (0x0000007fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[7U])));
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v15 = 1U;
            }
        }
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
            if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r) 
                          >> 2U)))) {
                if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r) 
                              >> 1U)))) {
                    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r)))) {
                        vlSelfRef.milan_datapath__DOT__lctx_rd_data_w 
                            = ((0x1aU == (0x0000001fU 
                                          & (IData)(vlSelfRef.milan_datapath__DOT__csr_lctx_rd_addr_w)))
                                ? vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__tv_cnt_r
                               [(7U & ((IData)(vlSelfRef.milan_datapath__DOT__csr_lctx_rd_addr_w) 
                                       >> 5U))] : (
                                                   (0x1bU 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__csr_lctx_rd_addr_w)))
                                                    ? vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__tnv_cnt_r
                                                   [
                                                   (7U 
                                                    & ((IData)(vlSelfRef.milan_datapath__DOT__csr_lctx_rd_addr_w) 
                                                       >> 5U))]
                                                    : vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r));
                        vlSelfRef.milan_datapath__DOT__lctx_rd_valid_w = 1U;
                    }
                }
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 0U;
        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
                    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r 
                            = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r))) 
                               & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r));
                        vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v16 
                            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                        vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v16 = 1U;
                        vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__tv_cnt_r__v0 
                            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                        vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__tnv_cnt_r__v0 
                            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r 
                            = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r))) 
                               & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r));
                        if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_s_r) 
                             == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_list_r = 0U;
                        }
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r 
                            = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r))
                                ? 1U : 5U);
                    } else if (((4U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r)) 
                                | (5U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r 
                            = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r))) 
                               & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r));
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_zero_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__zero_idx_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 5U;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r 
                            = (0x0000000fU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r)));
                    }
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 7U;
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
                if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__w11_mode_r) {
                    if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r) {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v8 
                            = (7U & (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r
                                              [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r]) 
                                      - (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_add_r)) 
                                     + (((IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdu_p_w) 
                                         & ((IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdu_idx_w) 
                                            == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r)))
                                         ? 1U : 0U)));
                        vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v8 
                            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                        vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v8 = 1U;
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v8 
                            = (7U & (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r
                                              [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r]) 
                                      - (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_add_r)) 
                                     + (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__overflow_reg) 
                                         & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__tl_idx_r) 
                                            == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r)))
                                         ? 1U : 0U)));
                        vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v8 
                            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r = 0U;
                        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__w11_mode_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 0U;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r = 1U;
                    }
                } else if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_mode_r) {
                    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r = 1U;
                    } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                        vlSelfRef.milan_datapath__DOT__avtprx_dirty_p_w 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__avtprx_dirty_p_w) 
                               | (0x00ffU & ((IData)(1U) 
                                             << (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r))));
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r = 2U;
                    } else if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r = 3U;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r 
                            = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r))) 
                               & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r));
                        vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v17 
                            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                        vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v17 = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r 
                            = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r))) 
                               & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r));
                        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_mode_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 0U;
                    }
                } else if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_zero_r) {
                    if ((9U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__zero_idx_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_zero_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__zero_idx_r = 0U;
                        vlSelfRef.milan_datapath__DOT__avtprx_dirty_p_w 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__avtprx_dirty_p_w) 
                               | (0x00ffU & ((IData)(1U) 
                                             << (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r))));
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 0U;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__zero_idx_r 
                            = (0x0000000fU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__zero_idx_r)));
                    }
                } else if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 0U;
                } else if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r) {
                    if ((0x0bU >= (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r 
                            = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w))) 
                               & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r));
                    }
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r = 0U;
                    if ((((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__penq_w) 
                          | (0U != (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r))) 
                         & (0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_list_r)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_list_r 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r) 
                               & (~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w))));
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_s_r 
                            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r = 0U;
                    }
                } else if ((((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__penq_w) 
                             | (0U != (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r))) 
                            & (0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_list_r)))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_list_r 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r;
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_s_r 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 0U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r = 1U;
                }
            } else if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 5U;
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r 
                    = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r)));
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
                if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__fmt_ok_w) {
                    if ((8U & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[4U])) {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__tv_cnt_r__v1 
                            = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__tv_cnt_r
                               [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r]);
                        vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__tv_cnt_r__v1 
                            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                        vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__tv_cnt_r__v1 = 1U;
                    } else {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__tnv_cnt_r__v1 
                            = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__tnv_cnt_r
                               [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r]);
                        vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__tnv_cnt_r__v1 
                            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                        vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__tnv_cnt_r__v1 = 1U;
                    }
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r 
                        = (((0x00001000U & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r)
                             ? 0U : 1U) | (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__seq_mm_w) 
                                            & (2U <= (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__lost_w)))
                                            ? 4U : 0U));
                    vlSelfRef.milan_datapath__DOT__avtprx_accept_p_w = 1U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtprx_accept_idx_w 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v0 
                        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[2U] 
                                          >> 0x0000000aU));
                    vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v0 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                    vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v0 = 1U;
                    vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v18 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                    if ((1U & (~ (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r 
                                  >> 0x0000000cU)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r 
                            = ((IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r) 
                               | (0x00ffU & ((IData)(1U) 
                                             << (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r))));
                    }
                    if ((1U & (((~ (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[4U] 
                                    >> 3U)) | (~ (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r 
                                                  >> 0x0000000cU))) 
                               | ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__seq_mm_w) 
                                  & (2U <= (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__lost_w)))))) {
                        vlSelfRef.milan_datapath__DOT__avtprx_dirty_p_w 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__avtprx_dirty_p_w) 
                               | (0x00ffU & ((IData)(1U) 
                                             << (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r))));
                    }
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_r 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w;
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 4U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 0U;
                }
            } else {
                if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r))) {
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__fmt_r 
                        = ((0x00000000ffffffffULL & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__fmt_r) 
                           | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r)) 
                              << 0x00000020U));
                }
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 3U;
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__fmt_r 
                = ((0xffffffff00000000ULL & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__fmt_r) 
                   | (IData)((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r)));
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 2U;
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_zero_r = 0U;
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__w11_mode_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__zero_idx_r = 0U;
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_mode_r = 0U;
            if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pdisp_new_w) 
                 | (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pdisp_w))) {
                if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pdisp_new_w) {
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[0U] 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[0U];
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[1U] 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[1U];
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[2U] 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[2U];
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[3U] 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[3U];
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[4U] 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[4U];
                } else {
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[0U] 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][0U];
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[1U] 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][1U];
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[2U] 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][2U];
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[3U] 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][3U];
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[4U] 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][4U];
                }
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__disp_s_w;
                if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__disp_s_w))) {
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__fmt_r 
                        = vlSelfRef.milan_datapath__DOT__aecp_in0_fmt;
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 2U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 1U;
                }
            } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r))) {
                if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 7U;
                }
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 6U;
                if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 6U;
                }
                if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 5U;
                }
                if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 4U;
                }
                if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 3U;
                }
                if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 2U;
                }
                if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 1U;
                }
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 0U;
                }
            } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r))) {
                if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 7U;
                }
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_mode_r = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 5U;
                if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 6U;
                }
                if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 5U;
                }
                if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 4U;
                }
                if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 3U;
                }
                if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 2U;
                }
                if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 1U;
                }
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 0U;
                }
            } else if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__depkt_any_w) {
                if (((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[7U]) 
                     | (0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[7U]))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 7U;
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_add_r 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[7U];
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_add_r 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[7U];
                }
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__w11_mode_r = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 5U;
                if (((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[6U]) 
                     | (0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[6U]))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 6U;
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_add_r 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[6U];
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_add_r 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[6U];
                }
                if (((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[5U]) 
                     | (0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[5U]))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 5U;
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_add_r 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[5U];
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_add_r 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[5U];
                }
                if (((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[4U]) 
                     | (0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[4U]))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 4U;
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_add_r 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[4U];
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_add_r 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[4U];
                }
                if (((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[3U]) 
                     | (0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[3U]))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 3U;
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_add_r 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[3U];
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_add_r 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[3U];
                }
                if (((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[2U]) 
                     | (0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[2U]))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 2U;
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_add_r 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[2U];
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_add_r 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[2U];
                }
                if (((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[1U]) 
                     | (0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[1U]))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 1U;
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_add_r 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[1U];
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_add_r 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[1U];
                }
                if (((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[0U]) 
                     | (0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[0U]))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 0U;
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_add_r 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[0U];
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_add_r 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[0U];
                }
            } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_list_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_list_r;
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_s_r;
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 5U;
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_list_r = 0U;
            } else if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_go_w) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r
                    [Vmilan_datapath__ConstPool__TABLE_h9276b836_0
                    [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r]];
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r 
                    = Vmilan_datapath__ConstPool__TABLE_h9276b836_0
                    [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r];
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_add_r 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r
                    [Vmilan_datapath__ConstPool__TABLE_h9276b836_0
                    [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r]];
                if ((0U != (0x0dffU & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r
                            [Vmilan_datapath__ConstPool__TABLE_h9276b836_0
                            [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r]]))) {
                    vlSelfRef.milan_datapath__DOT__avtprx_dirty_p_w 
                        = ((IData)(vlSelfRef.milan_datapath__DOT__avtprx_dirty_p_w) 
                           | (0x00ffU & ((IData)(1U) 
                                         << Vmilan_datapath__ConstPool__TABLE_h9276b836_0
                                         [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r])));
                }
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 5U;
            } else if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ext_rd_go_w) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 8U;
            }
        }
        if ((((7U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r)) 
              & (0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) 
             & (0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v0 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[0U];
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v0 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                = (0xfeU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v0 
                = (1U & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[0U] 
                         >> 9U));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v0 = 1U;
        } else {
            if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_go_w) 
                 & (0U == Vmilan_datapath__ConstPool__TABLE_h9276b836_0
                    [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r]))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v1 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[0U];
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v1 = 1U;
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v1 
                    = (1U & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[0U] 
                             >> 9U));
            } else {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v2 
                    = (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[0U] 
                       | vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[0U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v2 = 1U;
                if (((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[0U] 
                      >> 9U) & (0xffffU != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[0U]))) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v2 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[0U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v2 = 1U;
                }
            }
            if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_tick_r) 
                 & (0U != (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[0U] 
                           | vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[0U])))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                    = (1U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            } else if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_go_w) 
                        & (0U == Vmilan_datapath__ConstPool__TABLE_h9276b836_0
                           [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r]))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                    = (0xfeU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            }
        }
        if ((((7U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r)) 
              & (0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) 
             & (1U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v3 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[1U];
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v3 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                = (0xfdU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v3 
                = (1U & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[1U] 
                         >> 9U));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v3 = 1U;
        } else {
            if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_go_w) 
                 & (1U == Vmilan_datapath__ConstPool__TABLE_h9276b836_0
                    [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r]))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v4 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[1U];
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v4 = 1U;
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v4 
                    = (1U & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[1U] 
                             >> 9U));
            } else {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v5 
                    = (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[1U] 
                       | vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[1U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v5 = 1U;
                if (((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[1U] 
                      >> 9U) & (0xffffU != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[1U]))) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v5 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[1U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v5 = 1U;
                }
            }
            if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_tick_r) 
                 & (0U != (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[1U] 
                           | vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[1U])))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                    = (2U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            } else if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_go_w) 
                        & (1U == Vmilan_datapath__ConstPool__TABLE_h9276b836_0
                           [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r]))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                    = (0xfdU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            }
        }
        if ((((7U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r)) 
              & (0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) 
             & (2U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v6 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[2U];
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v6 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                = (0xfbU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v6 
                = (1U & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[2U] 
                         >> 9U));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v6 = 1U;
        } else {
            if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_go_w) 
                 & (2U == Vmilan_datapath__ConstPool__TABLE_h9276b836_0
                    [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r]))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v7 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[2U];
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v7 = 1U;
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v7 
                    = (1U & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[2U] 
                             >> 9U));
            } else {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v8 
                    = (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[2U] 
                       | vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[2U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v8 = 1U;
                if (((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[2U] 
                      >> 9U) & (0xffffU != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[2U]))) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v8 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[2U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v8 = 1U;
                }
            }
            if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_tick_r) 
                 & (0U != (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[2U] 
                           | vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[2U])))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                    = (4U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            } else if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_go_w) 
                        & (2U == Vmilan_datapath__ConstPool__TABLE_h9276b836_0
                           [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r]))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                    = (0xfbU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            }
        }
        if ((((7U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r)) 
              & (0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) 
             & (3U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v9 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[3U];
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v9 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                = (0xf7U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v9 
                = (1U & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[3U] 
                         >> 9U));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v9 = 1U;
        } else {
            if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_go_w) 
                 & (3U == Vmilan_datapath__ConstPool__TABLE_h9276b836_0
                    [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r]))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v10 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[3U];
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v10 = 1U;
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v10 
                    = (1U & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[3U] 
                             >> 9U));
            } else {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v11 
                    = (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[3U] 
                       | vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[3U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v11 = 1U;
                if (((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[3U] 
                      >> 9U) & (0xffffU != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[3U]))) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v11 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[3U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v11 = 1U;
                }
            }
            if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_tick_r) 
                 & (0U != (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[3U] 
                           | vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[3U])))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                    = (8U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            } else if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_go_w) 
                        & (3U == Vmilan_datapath__ConstPool__TABLE_h9276b836_0
                           [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r]))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                    = (0xf7U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            }
        }
        if ((((7U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r)) 
              & (0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) 
             & (4U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v12 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[4U];
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v12 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                = (0xefU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v12 
                = (1U & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[4U] 
                         >> 9U));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v12 = 1U;
        } else {
            if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_go_w) 
                 & (4U == Vmilan_datapath__ConstPool__TABLE_h9276b836_0
                    [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r]))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v13 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[4U];
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v13 = 1U;
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v13 
                    = (1U & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[4U] 
                             >> 9U));
            } else {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v14 
                    = (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[4U] 
                       | vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[4U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v14 = 1U;
                if (((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[4U] 
                      >> 9U) & (0xffffU != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[4U]))) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v14 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[4U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v14 = 1U;
                }
            }
            if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_tick_r) 
                 & (0U != (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[4U] 
                           | vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[4U])))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                    = (0x00000010U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            } else if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_go_w) 
                        & (4U == Vmilan_datapath__ConstPool__TABLE_h9276b836_0
                           [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r]))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                    = (0xefU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            }
        }
        if ((((7U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r)) 
              & (0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) 
             & (5U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v15 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[5U];
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v15 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                = (0xdfU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v15 
                = (1U & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[5U] 
                         >> 9U));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v15 = 1U;
        } else {
            if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_go_w) 
                 & (5U == Vmilan_datapath__ConstPool__TABLE_h9276b836_0
                    [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r]))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v16 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[5U];
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v16 = 1U;
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v16 
                    = (1U & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[5U] 
                             >> 9U));
            } else {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v17 
                    = (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[5U] 
                       | vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[5U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v17 = 1U;
                if (((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[5U] 
                      >> 9U) & (0xffffU != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[5U]))) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v17 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[5U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v17 = 1U;
                }
            }
            if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_tick_r) 
                 & (0U != (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[5U] 
                           | vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[5U])))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                    = (0x00000020U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            } else if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_go_w) 
                        & (5U == Vmilan_datapath__ConstPool__TABLE_h9276b836_0
                           [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r]))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                    = (0xdfU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            }
        }
        if ((((7U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r)) 
              & (0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) 
             & (6U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v18 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[6U];
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v18 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                = (0xbfU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v18 
                = (1U & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[6U] 
                         >> 9U));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v18 = 1U;
        } else {
            if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_go_w) 
                 & (6U == Vmilan_datapath__ConstPool__TABLE_h9276b836_0
                    [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r]))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v19 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[6U];
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v19 = 1U;
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v19 
                    = (1U & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[6U] 
                             >> 9U));
            } else {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v20 
                    = (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[6U] 
                       | vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[6U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v20 = 1U;
                if (((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[6U] 
                      >> 9U) & (0xffffU != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[6U]))) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v20 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[6U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v20 = 1U;
                }
            }
            if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_tick_r) 
                 & (0U != (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[6U] 
                           | vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[6U])))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                    = (0x00000040U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            } else if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_go_w) 
                        & (6U == Vmilan_datapath__ConstPool__TABLE_h9276b836_0
                           [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r]))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                    = (0xbfU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            }
        }
        if ((((7U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r)) 
              & (0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) 
             & (7U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v21 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[7U];
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v21 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                = (0x7fU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v21 
                = (1U & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[7U] 
                         >> 9U));
            vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v21 = 1U;
        } else {
            if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_go_w) 
                 & (7U == Vmilan_datapath__ConstPool__TABLE_h9276b836_0
                    [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r]))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v22 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[7U];
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v22 = 1U;
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v22 
                    = (1U & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[7U] 
                             >> 9U));
            } else {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v23 
                    = (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[7U] 
                       | vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[7U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v23 = 1U;
                if (((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[7U] 
                      >> 9U) & (0xffffU != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[7U]))) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v23 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[7U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v23 = 1U;
                }
            }
            if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_tick_r) 
                 & (0U != (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[7U] 
                           | vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[7U])))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                    = (0x00000080U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            } else if (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_go_w) 
                        & (7U == Vmilan_datapath__ConstPool__TABLE_h9276b836_0
                           [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r]))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
                    = (0x7fU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r));
            }
        }
        vlSelfRef.milan_datapath__DOT__avtprx_locked 
            = (1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r));
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
                       - (IData)(0x00000047U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_la_mvrp_r = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_la_r 
                    = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_la_r));
            } else if ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                              - (IData)(0x00000047U)))) {
                if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                           - (IData)(1U)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_la_r 
                        = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_la_r));
                }
            }
            if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                           - (IData)(0x00000047U)) 
                          >> 2U)))) {
                if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                               - (IData)(0x00000047U)) 
                              >> 1U)))) {
                    if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                               - (IData)(1U)))) {
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
        if ((8U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__aidx_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__gslope_r[0U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[0U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__gslope_r[1U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[1U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__gslope_r[2U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[2U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__gslope_r[3U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[3U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__gslope_r[4U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[4U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__gslope_r[5U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[5U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__gslope_r[6U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[6U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__gslope_r[7U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[7U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__gslope_r[8U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[8U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__sum_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__fit_w)
                    ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cand_w)
                    : vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__acc_r);
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__acc_r = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__over_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__over_acc_r) 
                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__refuse_w));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__over_acc_r = 0U;
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__acc_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__fit_w)
                    ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cand_w)
                    : vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__acc_r);
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__over_acc_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__over_acc_r) 
                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__refuse_w));
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
                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_221)))) {
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
                                    if (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_221) 
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
                                    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_allowed__61__command_type 
                                        = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_cmd_hi_r) 
                                            << 8U) 
                                           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o));
                                    __Vtemp_48 = VL_MATCHMASKED_I(16, (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_allowed__61__command_type), Vmilan_datapath__ConstPool__CONST_hca6ff4b2_0);
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____VlemCall_0__gdi_allowed 
                                        = Vmilan_datapath__ConstPool__TABLE_h90282f34_0
                                        [__Vtemp_48];
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
                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_178))) {
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
                    if (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_45) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__opd0_r 
                            = (((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r) 
                                                  << 0x00000010U) 
                                                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)))) 
                                << 0x00000010U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_cfg_r)));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__opd1_r 
                            = (((QData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_134)) 
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
                                     ? (QData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_134))
                                     : (((QData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_293)) 
                                         << 0x00000010U) 
                                        | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r))))));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__opd1_r 
                            = (QData)((IData)(((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_r)
                                                ? vlSelfRef.__VdfgRegularize_h6e95ff9d_0_293
                                                : ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__tix_w)
                                                    ? vlSelfRef.__VdfgRegularize_h6e95ff9d_0_134
                                                    : 
                                                   ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gasp_r)
                                                     ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)
                                                     : 
                                                    ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ty_r) 
                                                       & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_291)) 
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
                            ? 0x05e9U : (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_169) 
                                          | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_170) 
                                             | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_171) 
                                                | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_172) 
                                                   | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_173) 
                                                      | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_174) 
                                                         | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_175) 
                                                            | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_176) 
                                                               | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_177) 
                                                                  | (0U 
                                                                     != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r)))))))))))
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
    } else {
        vlSelfRef.milan_datapath__DOT__avtprx_mr_bit = 0U;
        vlSelfRef.milan_datapath__DOT__link_guard__DOT__tx_armed_r = 0U;
        vlSelfRef.milan_datapath__DOT__tkd_crfq_r = 0U;
        vlSelfRef.milan_datapath__DOT__link_guard__DOT__rx_armed_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__cur_slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__cur_slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__cur_slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__cur_slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__brd_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__curl_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__curr_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__ptp_sync__DOT__snap_ret_s = 0U;
        vlSelfRef.milan_datapath__DOT__ptp_sync__DOT__tod_rd_reg = 0ULL;
        vlSelfRef.milan_datapath__DOT__ptp_sync__DOT__tod_rd_valid_reg = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__cur_slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_sid_frame = 0ULL;
        vlSelfRef.milan_datapath__DOT__avtprx_match = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_parse_p = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_subtype = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_idx = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__tick_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__talker_diag__DOT__tick_p_r = 0U;
        vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_valid_w = 0U;
        VL_ASSIGN_W(1536, vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r, Vmilan_datapath__ConstPool__CONST_h22f5c49d_0);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_cancel_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_owner_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_deadline_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r = 0U;
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
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_txp_q_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__ltap_clr_p = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__ltap_en_r = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_rxp_q_r = 0U;
        vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__rollover_r = 0U;
        VL_ASSIGN_W(240, vlSelfRef.milan_datapath__DOT__chmap_phys_w, Vmilan_datapath__ConstPool__CONST_h7f3586b3_0);
        vlSelfRef.milan_datapath__DOT__cmap_rd_valid_w = 0U;
        vlSelfRef.milan_datapath__DOT__cmap_rd_data_w = 0U;
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
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_la_mvrp_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_q2_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__iv_bytes_r = 0ULL;
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
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__rr_r = 0U;
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
        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v5 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v6 = 1U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[4U] = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__fmt_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__zero_idx_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_zero_r = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__w11_mode_r = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_mode_r = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_add_r = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_add_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_add_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v24 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_list_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_s_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v1 = 1U;
        vlSelfRef.milan_datapath__DOT__avtprx_locked = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_dirty_p_w = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_accept_p_w = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__avtprx_accept_idx_w = 0U;
        vlSelfRef.milan_datapath__DOT__lctx_rd_data_w = 0U;
        vlSelfRef.milan_datapath__DOT__lctx_rd_valid_w = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__tv_cnt_r__v3 = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_la_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__rnd_act_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__td_tk_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__td_ls_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_join_r = 0U;
        VL_ASSIGN_W(288, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__gslope_r, Vmilan_datapath__ConstPool__CONST_h9a2fc1c8_0);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__alarm_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__acc_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__sum_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__over_acc_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__over_r = 0U;
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
    }
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w 
        = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r) 
                 - (IData)(1U)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_408 = (7U 
                                                  & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
                                                     - 
                                                     (1U 
                                                      & (- (IData)(
                                                                   (0U 
                                                                    != 
                                                                    (7U 
                                                                     & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_428 = ((0U 
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
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__diff_w 
        = (vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__cyc_r 
           - vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__prevc_r);
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__diff_w 
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
    vlSelfRef.o_irq_csr = (0U != (vlSelfRef.milan_datapath__DOT__csr__DOT__irq_status 
                                  & vlSelfRef.milan_datapath__DOT__csr__DOT__irq_mask));
    vlSelfRef.milan_datapath__DOT__evt_link_change 
        = ((IData)(vlSelfRef.axis_resetn) && ((IData)(vlSelfRef.milan_datapath__DOT__speed_q) 
                                              != (IData)(vlSelfRef.milan_datapath__DOT__speed_sync)));
    vlSelfRef.milan_datapath__DOT__chmap_phys_v_w = 
        ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__rsp_render_tick_p_w));
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
            = (0x00000fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r[0U]);
    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w 
            = (0x00000fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r[0U]);
    }
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w)))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w 
                = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r[0U] 
                                  >> 0x0000000cU));
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w 
                = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r[0U] 
                                  >> 0x0000000cU));
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w)))) {
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 2U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w 
                = (0x00000fffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r[1U] 
                                   << 8U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r[0U] 
                                             >> 0x00000018U)));
        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 2U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w 
                = (0x00000fffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r[1U] 
                                   << 8U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r[0U] 
                                             >> 0x00000018U)));
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w)))) {
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 3U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w 
                = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r[1U] 
                                  >> 4U));
        } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 3U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w 
                = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r[1U] 
                                  >> 4U));
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w)))) {
        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 4U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w 
                = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r[1U] 
                                  >> 0x00000010U));
        } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 4U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w 
                = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r[1U] 
                                  >> 0x00000010U));
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w)))) {
        if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w 
                = (0x00000fffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r[2U] 
                                   << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r[1U] 
                                             >> 0x0000001cU)));
        } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w 
                = (0x00000fffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r[2U] 
                                   << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r[1U] 
                                             >> 0x0000001cU)));
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w)))) {
        if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w 
                = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r[2U] 
                                  >> 8U));
        } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w 
                = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r[2U] 
                                  >> 8U));
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w)))) {
        if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 7U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w 
                = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r[2U] 
                   >> 0x00000014U);
        } else if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 7U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w 
                = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r[2U] 
                   >> 0x00000014U);
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w)))) {
        if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 8U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w 
                = (0x00000fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r[3U]);
        } else if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = 8U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w 
                = (0x00000fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r[3U]);
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
            = (0x00000fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r[0U]);
    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w 
            = (0x00000fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r[0U]);
    }
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w)))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w 
                = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r[0U] 
                                  >> 0x0000000cU));
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w 
                = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r[0U] 
                                  >> 0x0000000cU));
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w)))) {
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 2U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w 
                = (0x00000fffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r[1U] 
                                   << 8U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r[0U] 
                                             >> 0x00000018U)));
        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 2U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w 
                = (0x00000fffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r[1U] 
                                   << 8U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r[0U] 
                                             >> 0x00000018U)));
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w)))) {
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 3U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w 
                = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r[1U] 
                                  >> 4U));
        } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 3U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w 
                = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r[1U] 
                                  >> 4U));
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w)))) {
        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 4U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w 
                = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r[1U] 
                                  >> 0x00000010U));
        } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 4U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w 
                = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r[1U] 
                                  >> 0x00000010U));
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w)))) {
        if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w 
                = (0x00000fffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r[2U] 
                                   << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r[1U] 
                                             >> 0x0000001cU)));
        } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w 
                = (0x00000fffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r[2U] 
                                   << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r[1U] 
                                             >> 0x0000001cU)));
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w)))) {
        if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w 
                = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r[2U] 
                                  >> 8U));
        } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w 
                = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r[2U] 
                                  >> 8U));
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w)))) {
        if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 7U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w 
                = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r[2U] 
                   >> 0x00000014U);
        } else if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 7U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w 
                = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r[2U] 
                   >> 0x00000014U);
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w)))) {
        if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 8U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w 
                = (0x00000fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r[3U]);
        } else if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = 8U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w 
                = (0x00000fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r[3U]);
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_avail_w 
        = (1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__gp_valid_r) 
                    | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_busy_r) 
                       | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_stale_r))))));
    vlSelfRef.s_axi_rdata = vlSelfRef.milan_datapath__DOT__csr__DOT__r_data;
    vlSelfRef.milan_datapath__DOT__csr__DOT__rd_pend2 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_pend));
    vlSelfRef.milan_datapath__DOT__strtbl_sid_w[0U] 
        = (IData)((vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[0U]
                    ? vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[0U]
                    : (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[1U])) 
                        << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[0U])))));
    vlSelfRef.milan_datapath__DOT__strtbl_sid_w[1U] 
        = (IData)(((vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[0U]
                     ? vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[0U]
                     : (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[1U])) 
                         << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[0U])))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__strtbl_sid_w[2U] 
        = (IData)((vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[1U]
                    ? vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[1U]
                    : (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[3U])) 
                        << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[2U])))));
    vlSelfRef.milan_datapath__DOT__strtbl_sid_w[3U] 
        = (IData)(((vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[1U]
                     ? vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[1U]
                     : (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[3U])) 
                         << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[2U])))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__strtbl_sid_w[4U] 
        = (IData)((vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[2U]
                    ? vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[2U]
                    : (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[5U])) 
                        << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[4U])))));
    vlSelfRef.milan_datapath__DOT__strtbl_sid_w[5U] 
        = (IData)(((vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[2U]
                     ? vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[2U]
                     : (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[5U])) 
                         << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[4U])))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__strtbl_sid_w[6U] 
        = (IData)((vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[3U]
                    ? vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[3U]
                    : (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[7U])) 
                        << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[6U])))));
    vlSelfRef.milan_datapath__DOT__strtbl_sid_w[7U] 
        = (IData)(((vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[3U]
                     ? vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[3U]
                     : (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[7U])) 
                         << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[6U])))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__strtbl_sid_w[8U] 
        = (IData)((vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[4U]
                    ? vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[4U]
                    : (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[9U])) 
                        << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[8U])))));
    vlSelfRef.milan_datapath__DOT__strtbl_sid_w[9U] 
        = (IData)(((vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[4U]
                     ? vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[4U]
                     : (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[9U])) 
                         << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[8U])))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__strtbl_sid_w[10U] 
        = (IData)((vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[5U]
                    ? vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[5U]
                    : (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[11U])) 
                        << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[10U])))));
    vlSelfRef.milan_datapath__DOT__strtbl_sid_w[11U] 
        = (IData)(((vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[5U]
                     ? vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[5U]
                     : (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[11U])) 
                         << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[10U])))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__strtbl_sid_w[12U] 
        = (IData)((vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[6U]
                    ? vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[6U]
                    : (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[13U])) 
                        << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[12U])))));
    vlSelfRef.milan_datapath__DOT__strtbl_sid_w[13U] 
        = (IData)(((vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[6U]
                     ? vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[6U]
                     : (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[13U])) 
                         << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[12U])))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__strtbl_sid_w[14U] 
        = (IData)((vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[7U]
                    ? vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[7U]
                    : (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[15U])) 
                        << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[14U])))));
    vlSelfRef.milan_datapath__DOT__strtbl_sid_w[15U] 
        = (IData)(((vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[7U]
                     ? vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[7U]
                     : (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[15U])) 
                         << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[14U])))) 
                   >> 0x00000020U));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_243 = (1U 
                                                  & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_busy_r)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_244 = (1U 
                                                  & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_dir_r)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_245 = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_rden_r) 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_dir_r));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_271 = ((~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_dir_r)) 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_rden_r));
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
        __Vtemp_47[0U] = 0U;
        __Vtemp_47[1U] = 0U;
        __Vtemp_47[2U] = 0U;
        __Vtemp_47[3U] = 0U;
        __Vtemp_47[4U] = 0U;
        __Vtemp_47[5U] = 0U;
        __Vtemp_47[6U] = 0U;
        __Vtemp_47[7U] = 0U;
        __Vtemp_47[8U] = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mvrp_q_r);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__alen_w = 2U;
    } else {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_type_w 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[8U] 
                              >> 0x00000015U));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_ev_w 
            = (7U & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[8U] 
                      << 0x0000000eU) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[8U] 
                                         >> 0x00000012U)));
        __Vtemp_47[0U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[0U];
        __Vtemp_47[1U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[1U];
        __Vtemp_47[2U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[2U];
        __Vtemp_47[3U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[3U];
        __Vtemp_47[4U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[4U];
        __Vtemp_47[5U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[5U];
        __Vtemp_47[6U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[6U];
        __Vtemp_47[7U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[7U];
        __Vtemp_47[8U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[8U];
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
        = __Vtemp_47[0U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[1U] 
        = __Vtemp_47[1U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[2U] 
        = __Vtemp_47[2U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[3U] 
        = __Vtemp_47[3U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[4U] 
        = __Vtemp_47[4U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[5U] 
        = __Vtemp_47[5U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[6U] 
        = __Vtemp_47[6U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[7U] 
        = __Vtemp_47[7U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[8U] 
        = (0x0000ffffU & __Vtemp_47[8U]);
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
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__st_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__st_r;
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__slot_r;
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
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v7) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v8) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v9) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v10) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[8U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v11) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[9U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v12) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[10U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v13) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[11U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v14) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[12U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v15) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[13U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v16) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[14U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v17) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[15U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v18) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[16U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v19) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[17U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v20) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[18U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v21) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[19U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v22) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[20U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v23) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[21U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v24) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[22U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v25) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[23U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v26) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[24U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v27) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[25U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v28) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[26U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v29) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[27U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v30) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[28U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v31) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[29U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v32) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[30U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v33) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[31U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v34) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[8U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[9U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[10U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[11U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[12U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[13U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[14U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[15U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[16U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[17U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[18U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[19U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[20U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[21U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[22U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[23U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[24U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[25U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[26U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[27U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[28U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[29U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[30U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[31U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r;
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
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[11U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v11;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v12) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[12U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v12;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v13) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[13U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v13;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v14) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[14U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v14;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v15) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[15U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v15;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v16) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[16U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v16;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v17) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[17U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v17;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v18) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[18U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v18;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v19) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[19U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v19;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v20) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[20U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v20;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v21) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[21U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v21;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v22) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[22U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v22;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v23) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[23U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v23;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v24) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[24U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v24;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v25) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[25U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v25;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v26) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[26U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v26;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v27) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[27U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v27;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v28) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[28U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v28;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v29) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[29U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v29;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v30) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[30U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v30;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v31) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[31U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v31;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v32) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v32) {
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
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[11U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[12U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[13U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[14U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[15U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[16U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[17U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[18U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[19U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[20U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[21U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[22U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[23U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[24U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[25U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[26U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[27U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[28U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[29U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[30U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[31U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__to_cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__to_cnt_r;
    vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__flush_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__flush_r;
    vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__sel_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__sel_r;
    vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__locked_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__locked_r;
    vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__to_cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__to_cnt_r;
    vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__sel_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__sel_r;
    vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__locked_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__locked_r;
    vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__to_cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__crf_dp_mux__DOT__to_cnt_r;
}
