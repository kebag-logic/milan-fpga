// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

extern const VlWide<28>/*895:0*/ Vmilan_datapath__ConstPool__CONST_hca6ff4b2_0;
extern const VlUnpacked<CData/*0:0*/, 14> Vmilan_datapath__ConstPool__TABLE_h90282f34_0;
extern const VlWide<13>/*415:0*/ Vmilan_datapath__ConstPool__CONST_hb995d365_0;
extern const VlUnpacked<IData/*16:0*/, 16> Vmilan_datapath__ConstPool__TABLE_h441640be_0;
extern const VlWide<9>/*287:0*/ Vmilan_datapath__ConstPool__CONST_hc5471b50_0;
extern const VlUnpacked<CData/*2:0*/, 16> Vmilan_datapath__ConstPool__TABLE_h1b26f04f_0;
extern const VlWide<10>/*319:0*/ Vmilan_datapath__ConstPool__CONST_hab76c978_0;
extern const VlUnpacked<CData/*0:0*/, 256> Vmilan_datapath__ConstPool__TABLE_h6dea4ce6_0;

void Vmilan_datapath___024root___nba_sequent__TOP__3(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___nba_sequent__TOP__3\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*6:0*/ milan_datapath__DOT__csr_tctx_rd_addr_w;
    milan_datapath__DOT__csr_tctx_rd_addr_w = 0;
    VlWide<3>/*79:0*/ milan_datapath__DOT__rmap_flat_w;
    VL_ZERO_W(80, milan_datapath__DOT__rmap_flat_w);
    CData/*7:0*/ milan_datapath__DOT__tdm_lane_streams__DOT__rword;
    milan_datapath__DOT__tdm_lane_streams__DOT__rword = 0;
    CData/*0:0*/ milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run_v;
    milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run_v = 0;
    CData/*0:0*/ milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run0_v;
    milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__adv_scan__DOT__run0_v = 0;
    CData/*0:0*/ milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run_v;
    milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run_v = 0;
    CData/*0:0*/ milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run0_v;
    milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__adv_scan__DOT__run0_v = 0;
    CData/*0:0*/ milan_datapath__DOT__avtp_rx_monitor__DOT____VlemCall_6__ms_locked;
    IData/*31:0*/ milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t;
    milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_allowed__57__command_type;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_allowed__57__command_type = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__163__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__163__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__164__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__164__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__165__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__165__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__166__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__166__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__167__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__167__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__168__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__168__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__169__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__169__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__170__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__170__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__171__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__171__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__172__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__172__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__173__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__173__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__174__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__174__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__175__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__175__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__176__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__176__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__177__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__177__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__178__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__178__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__179__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__179__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__180__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__180__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__181__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__181__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__182__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__182__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__183__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__183__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__184__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__184__w = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__ms_locked__234__w;
    __Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__ms_locked__234__w = 0;
    CData/*5:0*/ __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__308__Vfuncout;
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__308__Vfuncout = 0;
    CData/*1:0*/ __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__308__t;
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__308__t = 0;
    CData/*2:0*/ __VdfgRegularize_h6e95ff9d_0_89;
    __VdfgRegularize_h6e95ff9d_0_89 = 0;
    CData/*2:0*/ __VdfgRegularize_h6e95ff9d_0_90;
    __VdfgRegularize_h6e95ff9d_0_90 = 0;
    CData/*3:0*/ __VdfgRegularize_h6e95ff9d_0_197;
    __VdfgRegularize_h6e95ff9d_0_197 = 0;
    CData/*3:0*/ __VdfgRegularize_h6e95ff9d_0_198;
    __VdfgRegularize_h6e95ff9d_0_198 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_203;
    __VdfgRegularize_h6e95ff9d_0_203 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_204;
    __VdfgRegularize_h6e95ff9d_0_204 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_330;
    __VdfgRegularize_h6e95ff9d_0_330 = 0;
    VlWide<3>/*73:0*/ __VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0;
    VL_ZERO_W(74, __VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0);
    CData/*7:0*/ __VdlyDim0__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0;
    __VdlyDim0__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0 = 0;
    IData/*31:0*/ __Vtemp_1;
    VlWide<3>/*95:0*/ __Vtemp_11;
    IData/*31:0*/ __Vilp1;
    // Body
    vlSelfRef.milan_datapath__DOT__csr__DOT__sweep_cnt 
        = vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__sweep_cnt;
    vlSelfRef.milan_datapath__DOT__zf_tick_cdc__DOT__sync 
        = vlSelfRef.__Vdly__milan_datapath__DOT__zf_tick_cdc__DOT__sync;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__v_mrp_valid_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__out_valid_r) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__out_emit_r));
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_q_r__v0) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_q_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__lb_q_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__lb_q_r__v0;
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
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[11U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v11;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v12) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[12U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v12;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v13) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[13U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v13;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v14) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[14U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v14;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v15) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[15U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v15;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v16) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[16U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v16;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v17) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[17U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v17;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v18) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[18U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v18;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v19) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[19U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v19;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v20) {
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
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[11U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[12U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[13U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[14U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[15U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[16U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[17U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[18U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[19U] = 0U;
    }
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
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__was_filled_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__was_filled_r;
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__prefill_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__prefill_r;
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__ms_div_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__ms_div_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fifo_r__v0) {
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fifo_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fifo_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fifo_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r__v0) {
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r__v1) {
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r__v1] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r__v1;
    }
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wen_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wen_r;
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wptr_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wptr_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__mem_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__mem_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__mem_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_idx_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_idx_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_st_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_st_r;
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__st_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__st_r;
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__slot_r;
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
    vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yfin_w 
        = (VL_LTS_III(30, 0x007fffffU, vlSelfRef.__VdfgRegularize_h6e95ff9d_0_114)
            ? 0x007fffffU : (VL_GTS_III(30, 0x3f800000U, vlSelfRef.__VdfgRegularize_h6e95ff9d_0_114)
                              ? 0x00800000U : (0x00ffffffU 
                                               & vlSelfRef.__VdfgRegularize_h6e95ff9d_0_114)));
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r__v0) {
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bpop_w 
        = (1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r) 
                    | (0U == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bcnt_r)))));
    vlSelfRef.milan_datapath__DOT__ptp_sync__DOT__snap_ret_s 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_sync__DOT__snap_ret_s;
    vlSelfRef.milan_datapath__DOT__talker_diag__DOT__tick_cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__tick_cnt_r;
    __Vilp1 = 0U;
    while ((__Vilp1 <= 0x0000002fU)) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r[__Vilp1] 
            = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r
            [__Vilp1];
        __Vilp1 = ((IData)(1U) + __Vilp1);
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r;
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
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w 
        = (0x0000ffffU & (vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__diff_w 
                          | (- (IData)((0U != (vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__diff_w 
                                               >> 0x00000010U))))));
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w 
        = (0x0000ffffU & (vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__diff_w 
                          | (- (IData)((0U != (vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__diff_w 
                                               >> 0x00000010U))))));
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_312 = (7U 
                                                  & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
                                                      >> 3U) 
                                                     - 
                                                     (1U 
                                                      & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_331))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_329 = (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_331) 
                                                   << 1U) 
                                                  | (0U 
                                                     != 
                                                     (7U 
                                                      & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r)));
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__map_r__v0) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_render__DOT__map_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__map_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__map_r__v1) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[8U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[9U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v0) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v1) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v2) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v2;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v3) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v4) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v5) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v5;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v6) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v6;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v7) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v7;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v8) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v8;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v9) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v9;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v10) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v10;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v11) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v11;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v12) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v12;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v13) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v13;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v14) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v14;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v15) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v15;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v16) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v16;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v17) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v17;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v18) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v18;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v19) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v19;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v20) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v20;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v21) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v21;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v22) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v22;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v23) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v23;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v24) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[8U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v24;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v25) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[8U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v25;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v26) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[8U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v26;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v27) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[9U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v27;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v28) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[9U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v28;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v29) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[9U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v29;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v30) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[8U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[9U] = 0U;
    }
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
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[8U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[9U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[10U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[11U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[12U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[13U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[14U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[15U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[16U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[17U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[18U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[19U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[20U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[21U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[22U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[23U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[24U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[25U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[26U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[27U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[28U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[29U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[30U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[31U] = 0U;
    }
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
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__wbank_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v1) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__wbank_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v0] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v1) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v1] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v2) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v3) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v4) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v5) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v1) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__wbank_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__pend_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__pend_r__v0] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__pend_r__v1] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v2) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v3) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v4) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v5) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v1) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v2) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__wbank_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__wbank_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r[3U] = 0U;
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
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r[3U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__est_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_s_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_s_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__zero_idx_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__zero_idx_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_list_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_list_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v0) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v0[0U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v0[1U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v0[2U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v0[3U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v0[4U];
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1[0U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1[1U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1[2U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1][3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1[3U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1][4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1[4U];
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v2) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v2[0U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v2[1U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v2[2U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v2[3U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v2[4U];
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v3) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v3[0U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v3[1U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v3[2U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v3[3U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v3[4U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v4[0U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v4[1U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v4[2U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v4[3U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v4[4U];
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v5) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][0U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][1U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][2U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][3U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v6) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][0U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][1U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][2U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][3U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][4U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_zero_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_zero_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v0) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v1) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v2) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v3) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v4) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v5) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v5;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v6) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v7) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v7;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v8) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v8] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v9) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v9] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v0) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v10] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v0) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v1) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v2) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v2;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v3) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v4) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v5) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v5;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v6) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v6;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v7) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v7;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v8) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v8;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v9) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v9;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v10) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v10;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v11) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v11;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v0) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v1) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v2) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v2;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v3) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v4) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v5) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v5;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v6) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v6;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v7) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v7;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v8) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v8;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v9) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v9;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v10) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v10;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v11) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v11;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v12) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v0) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v1) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v2) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v2;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v3) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v4) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v4] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v1) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v0) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v1) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v2) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v2;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v3) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v4) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v4] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v1) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__tv_cnt_r__v3) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[3U] = 0U;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_130 = (0U 
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_281 = ((1ULL 
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
    if (vlSelfRef.axis_resetn) {
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
                                    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_allowed__57__command_type 
                                        = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_cmd_hi_r) 
                                            << 8U) 
                                           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o));
                                    __Vtemp_1 = VL_MATCHMASKED_I(16, (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_allowed__57__command_type), Vmilan_datapath__ConstPool__CONST_hca6ff4b2_0);
                                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____VlemCall_0__gdi_allowed 
                                        = Vmilan_datapath__ConstPool__TABLE_h90282f34_0
                                        [__Vtemp_1];
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
                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_128))) {
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
                    if (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_35) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__opd0_r 
                            = (((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r) 
                                                  << 0x00000010U) 
                                                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)))) 
                                << 0x00000010U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_cfg_r)));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__opd1_r 
                            = (((QData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_93)) 
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
                                     ? (QData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_93))
                                     : (((QData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_227)) 
                                         << 0x00000010U) 
                                        | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r))))));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__opd1_r 
                            = (QData)((IData)(((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_r)
                                                ? vlSelfRef.__VdfgRegularize_h6e95ff9d_0_227
                                                : ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__tix_w)
                                                    ? vlSelfRef.__VdfgRegularize_h6e95ff9d_0_93
                                                    : 
                                                   ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gasp_r)
                                                     ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)
                                                     : 
                                                    ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ty_r) 
                                                       & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_225)) 
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
                            ? 0x05e9U : (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_123) 
                                          | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_124) 
                                             | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_125) 
                                                | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_126) 
                                                   | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_127) 
                                                      | (0U 
                                                         != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r)))))))
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_take_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pick_vld_w) 
           & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r)));
    vlSelfRef.milan_datapath__DOT__pp_cd_adp_avail_index_w 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r[0U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_done_avail_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_dep_r)) 
           & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r)));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fill_w 
        = (0x000003ffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wptr_r) 
                          - (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rptr_r)));
    vlSelfRef.milan_datapath__DOT__gm_recentre_p_r 
        = ((IData)(vlSelfRef.axis_resetn) && ((0ULL 
                                               != vlSelfRef.milan_datapath__DOT__gm_recentre_q_r) 
                                              & (0ULL 
                                                 != vlSelfRef.milan_datapath__DOT__gm_recentre_q_r)));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wfull_w 
        = ((IData)(vlSelfRef.axis_resetn) && ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wptr_gray_n) 
                                              == ((0x00000018U 
                                                   & ((~ 
                                                       ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rgray_w2_r) 
                                                        >> 3U)) 
                                                      << 3U)) 
                                                  | (7U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rgray_w2_r)))));
    vlSelfRef.milan_datapath__DOT__rsp_tlast_w = ((IData)(vlSelfRef.axis_resetn) 
                                                  && (3U 
                                                      == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__beat_r)));
    vlSelfRef.milan_datapath__DOT__rsp_tvalid_w = ((IData)(vlSelfRef.axis_resetn) 
                                                   && ((0U 
                                                        == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__beat_r))
                                                        ? (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_take_w)
                                                        : (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ev_ok_r)));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_rd_w 
        = (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r
           [vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r] 
           & (- (IData)((0U >= (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r)))));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_visit_w 
        = ((1U == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__st_r)) 
           & (1U > (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r)));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_cnt_w 
        = (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r
           [vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r] 
           & (- (IData)((0U >= (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r)))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_32 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w) 
                                                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w));
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
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_v_w)) 
         & (0U != (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r) 
                         >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_ix_w = 2U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_v_w)) 
         & (0U != (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r) 
                         >> 6U))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_ix_w = 3U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_v_w)) 
         & (0U != (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r) 
                         >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_ix_w = 4U;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_199 = ((
                                                   (0x00000010U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r))
                                                    ? 2U
                                                    : 1U) 
                                                  & (- (IData)(
                                                               (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r) 
                                                                 >> 4U) 
                                                                & (0U 
                                                                   != 
                                                                   (3U 
                                                                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r) 
                                                                       >> 8U)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_200 = ((
                                                   (8U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r))
                                                    ? 2U
                                                    : 1U) 
                                                  & (- (IData)(
                                                               (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r) 
                                                                 >> 3U) 
                                                                & (0U 
                                                                   != 
                                                                   (3U 
                                                                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r) 
                                                                       >> 6U)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_201 = ((
                                                   (4U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r))
                                                    ? 2U
                                                    : 1U) 
                                                  & (- (IData)(
                                                               (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r) 
                                                                 >> 2U) 
                                                                & (0U 
                                                                   != 
                                                                   (3U 
                                                                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r) 
                                                                       >> 4U)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_202 = ((
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_84 = (((1U 
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
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_v_w)) 
         & (0U != (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r) 
                         >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_ix_w = 2U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_v_w)) 
         & (0U != (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r) 
                         >> 6U))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_ix_w = 3U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_v_w)) 
         & (0U != (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r) 
                         >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_ix_w = 4U;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_44 = (3U 
                                                 & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r) 
                                                     >> 8U) 
                                                    & (- (IData)(
                                                                 (0U 
                                                                  != 
                                                                  (3U 
                                                                   & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r) 
                                                                      >> 8U)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_45 = (3U 
                                                 & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r) 
                                                     >> 6U) 
                                                    & (- (IData)(
                                                                 (0U 
                                                                  != 
                                                                  (3U 
                                                                   & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r) 
                                                                      >> 6U)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_46 = (3U 
                                                 & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r) 
                                                     >> 4U) 
                                                    & (- (IData)(
                                                                 (0U 
                                                                  != 
                                                                  (3U 
                                                                   & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r) 
                                                                      >> 4U)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_47 = (3U 
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_228 = (IData)(
                                                         ((0x00000014U 
                                                           == 
                                                           (0x0000001cU 
                                                            & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[11U])) 
                                                          & (2U 
                                                             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__cnt_r))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_229 = (IData)(
                                                         ((4U 
                                                           == 
                                                           (0x0000001cU 
                                                            & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[11U])) 
                                                          & (4U 
                                                             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__cnt_r))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_230 = (IData)(
                                                         ((0U 
                                                           == 
                                                           (0x0000001cU 
                                                            & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[11U])) 
                                                          & (4U 
                                                             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__cnt_r))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_231 = ((0U 
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
    vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__prod_w 
        = (0x000001ffffffffffULL & VL_MULS_QQQ(41, 
                                               (0x000001ffffffffffULL 
                                                & VL_EXTENDS_QI(41,17, Vmilan_datapath__ConstPool__TABLE_h441640be_0
                                                                [vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r])), 
                                               (0x000001ffffffffffULL 
                                                & VL_EXTENDS_QI(41,24, 
                                                                ((0U 
                                                                  == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r))
                                                                  ? vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__curl_r
                                                                  : 
                                                                 ((1U 
                                                                   == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r))
                                                                   ? vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r
                                                                   : 
                                                                  ((2U 
                                                                    == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r))
                                                                    ? vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl2_r
                                                                    : 
                                                                   ((3U 
                                                                     == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r))
                                                                     ? vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r
                                                                     : 
                                                                    ((4U 
                                                                      == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r))
                                                                      ? vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl2_r
                                                                      : 
                                                                     ((5U 
                                                                       == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r))
                                                                       ? vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__curr_r
                                                                       : 
                                                                      ((6U 
                                                                        == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r))
                                                                        ? vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r
                                                                        : 
                                                                       ((7U 
                                                                         == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r))
                                                                         ? vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr2_r
                                                                         : 
                                                                        ((8U 
                                                                          == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r))
                                                                          ? vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r
                                                                          : vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr2_r)))))))))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_maddr_w 
        = (0x00000fffU & (((IData)(0x0240U) * (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__cur_slot_r)) 
                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_ptr_r)));
    vlSelfRef.milan_datapath__DOT__mga_engaged_w = vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__engaged_r;
    vlSelfRef.milan_datapath__DOT__mga_err_w = vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__err_r;
    vlSelfRef.milan_datapath__DOT__crf_clk_selected_r 
        = ((IData)(vlSelfRef.axis_resetn) && (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_aecp_clk_src_index_w)));
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
    __VdfgRegularize_h6e95ff9d_0_330 = ((0U != (7U 
                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
                                                   >> 6U))) 
                                        & (0U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_329)));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushA_w = 0U;
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pairA_w = 0ULL;
    if (vlSelfRef.milan_datapath__DOT__chmap_phys_v_w) {
        if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pos_r))) {
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushA_w = 1U;
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pairA_w 
                = (((QData)((IData)((0x00ffffffU & vlSelfRef.milan_datapath__DOT__chmap_phys_w[0U]))) 
                    << 0x00000018U) | (QData)((IData)(
                                                      (0x00ffffffU 
                                                       & ((vlSelfRef.milan_datapath__DOT__chmap_phys_w[1U] 
                                                           << 8U) 
                                                          | (vlSelfRef.milan_datapath__DOT__chmap_phys_w[0U] 
                                                             >> 0x00000018U))))));
        } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pos_r))) {
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushA_w = 1U;
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pairA_w 
                = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__lhold_r)) 
                    << 0x00000018U) | (QData)((IData)(
                                                      (0x00ffffffU 
                                                       & vlSelfRef.milan_datapath__DOT__chmap_phys_w[0U]))));
        }
    }
    milan_datapath__DOT__rmap_flat_w[0U] = (((((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[3U]) 
                                               << 8U) 
                                              | vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[2U]) 
                                             << 0x00000010U) 
                                            | (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[1U]) 
                                                << 8U) 
                                               | vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[0U]));
    milan_datapath__DOT__rmap_flat_w[1U] = (((((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[7U]) 
                                               << 8U) 
                                              | vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[6U]) 
                                             << 0x00000010U) 
                                            | (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[5U]) 
                                                << 8U) 
                                               | vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[4U]));
    milan_datapath__DOT__rmap_flat_w[2U] = (0x0000ffffU 
                                            & (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[9U]) 
                                                << 8U) 
                                               | vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[8U]));
    vlSelfRef.milan_datapath__DOT__rsp_render_tick_p_w 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__tick_d_r));
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
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[8U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[8U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[9U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[9U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[10U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[10U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[11U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[11U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[12U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[12U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[13U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[13U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[14U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[14U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[15U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[15U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[16U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[16U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[17U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[17U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[18U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[18U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[19U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[19U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[20U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[20U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[21U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[21U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[22U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[22U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[23U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[23U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[24U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[24U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[25U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[25U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[26U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[26U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[27U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[27U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[28U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[28U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[29U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[29U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[30U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[30U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[31U] 
          >> 0x0cU) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[31U] 
                                    >> 8U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    __VdfgRegularize_h6e95ff9d_0_89 = (7U & ((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
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
    __VdfgRegularize_h6e95ff9d_0_90 = (7U & ((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
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
    __VdfgRegularize_h6e95ff9d_0_197 = (0x0000000fU 
                                        & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                        [((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                          << 1U)]);
    __VdfgRegularize_h6e95ff9d_0_198 = (0x0000000fU 
                                        & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                        [(1U | ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                << 1U))]);
    __VdfgRegularize_h6e95ff9d_0_203 = (1U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                              [(1U 
                                                | ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                   << 1U))] 
                                              + (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                                 [(1U 
                                                   | ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                      << 1U))] 
                                                 >> 4U)));
    __VdfgRegularize_h6e95ff9d_0_204 = (1U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                              [((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                << 1U)] 
                                              + (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                                 [((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                   << 1U)] 
                                                 >> 4U)));
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
           | ((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[8U])) 
                        << 0x0000001aU) | (QData)((IData)(
                                                          (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[7U]) 
                                                            << 0x0000000dU) 
                                                           | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[6U]))))) 
              << 0x0000000eU));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[3U] 
        = ((0xffe00000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[3U]) 
           | (((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[8U])) 
                         << 0x0000001aU) | (QData)((IData)(
                                                           (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[7U]) 
                                                             << 0x0000000dU) 
                                                            | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[6U]))))) 
               >> 0x00000012U) | ((IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[8U])) 
                                             << 0x0000001aU) 
                                            | (QData)((IData)(
                                                              (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[7U]) 
                                                                << 0x0000000dU) 
                                                               | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[6U])))) 
                                           >> 0x00000020U)) 
                                  << 0x0000000eU)));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[3U] 
        = ((0x001fffffU & vlSelfRef.milan_datapath__DOT__cmap_flat_w[3U]) 
           | ((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[11U])) 
                        << 0x0000001aU) | (QData)((IData)(
                                                          (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[10U]) 
                                                            << 0x0000000dU) 
                                                           | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[9U]))))) 
              << 0x00000015U));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[4U] 
        = ((0xf0000000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[4U]) 
           | (((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[11U])) 
                         << 0x0000001aU) | (QData)((IData)(
                                                           (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[10U]) 
                                                             << 0x0000000dU) 
                                                            | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[9U]))))) 
               >> 0x0000000bU) | ((IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[11U])) 
                                             << 0x0000001aU) 
                                            | (QData)((IData)(
                                                              (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[10U]) 
                                                                << 0x0000000dU) 
                                                               | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[9U])))) 
                                           >> 0x00000020U)) 
                                  << 0x00000015U)));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[4U] 
        = ((0x0fffffffU & vlSelfRef.milan_datapath__DOT__cmap_flat_w[4U]) 
           | ((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[14U])) 
                        << 0x0000001aU) | (QData)((IData)(
                                                          (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[13U]) 
                                                            << 0x0000000dU) 
                                                           | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[12U]))))) 
              << 0x0000001cU));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[5U] 
        = (((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[14U])) 
                      << 0x0000001aU) | (QData)((IData)(
                                                        (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[13U]) 
                                                          << 0x0000000dU) 
                                                         | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[12U]))))) 
            >> 4U) | ((IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[14U])) 
                                 << 0x0000001aU) | (QData)((IData)(
                                                                   (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[13U]) 
                                                                     << 0x0000000dU) 
                                                                    | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[12U])))) 
                               >> 0x00000020U)) << 0x0000001cU));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[6U] 
        = ((0xfffffff8U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[6U]) 
           | ((IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[14U])) 
                         << 0x0000001aU) | (QData)((IData)(
                                                           (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[13U]) 
                                                             << 0x0000000dU) 
                                                            | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[12U])))) 
                       >> 0x00000020U)) >> 4U));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[6U] 
        = ((7U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[6U]) 
           | ((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[17U])) 
                        << 0x0000001aU) | (QData)((IData)(
                                                          (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[16U]) 
                                                            << 0x0000000dU) 
                                                           | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[15U]))))) 
              << 3U));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[7U] 
        = ((0xfffffc00U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[7U]) 
           | (((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[17U])) 
                         << 0x0000001aU) | (QData)((IData)(
                                                           (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[16U]) 
                                                             << 0x0000000dU) 
                                                            | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[15U]))))) 
               >> 0x0000001dU) | ((IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[17U])) 
                                             << 0x0000001aU) 
                                            | (QData)((IData)(
                                                              (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[16U]) 
                                                                << 0x0000000dU) 
                                                               | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[15U])))) 
                                           >> 0x00000020U)) 
                                  << 3U)));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[7U] 
        = ((0x000003ffU & vlSelfRef.milan_datapath__DOT__cmap_flat_w[7U]) 
           | ((IData)((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[21U]) 
                                          << 0x0000000dU) 
                                         | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[20U]))) 
                        << 0x0000001aU) | (QData)((IData)(
                                                          (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[19U]) 
                                                            << 0x0000000dU) 
                                                           | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[18U]))))) 
              << 0x0000000aU));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[8U] 
        = ((0xc0000000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[8U]) 
           | (((IData)((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[21U]) 
                                           << 0x0000000dU) 
                                          | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[20U]))) 
                         << 0x0000001aU) | (QData)((IData)(
                                                           (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[19U]) 
                                                             << 0x0000000dU) 
                                                            | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[18U]))))) 
               >> 0x00000016U) | ((IData)(((((QData)((IData)(
                                                             (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[21U]) 
                                                               << 0x0000000dU) 
                                                              | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[20U]))) 
                                             << 0x0000001aU) 
                                            | (QData)((IData)(
                                                              (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[19U]) 
                                                                << 0x0000000dU) 
                                                               | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[18U])))) 
                                           >> 0x00000020U)) 
                                  << 0x0000000aU)));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[8U] 
        = ((0x3fffffffU & vlSelfRef.milan_datapath__DOT__cmap_flat_w[8U]) 
           | ((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[24U])) 
                        << 0x0000001aU) | (QData)((IData)(
                                                          (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[23U]) 
                                                            << 0x0000000dU) 
                                                           | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[22U]))))) 
              << 0x0000001eU));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[9U] 
        = (((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[24U])) 
                      << 0x0000001aU) | (QData)((IData)(
                                                        (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[23U]) 
                                                          << 0x0000000dU) 
                                                         | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[22U]))))) 
            >> 2U) | ((IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[24U])) 
                                 << 0x0000001aU) | (QData)((IData)(
                                                                   (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[23U]) 
                                                                     << 0x0000000dU) 
                                                                    | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[22U])))) 
                               >> 0x00000020U)) << 0x0000001eU));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[10U] 
        = ((0xffffffe0U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[10U]) 
           | ((IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[24U])) 
                         << 0x0000001aU) | (QData)((IData)(
                                                           (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[23U]) 
                                                             << 0x0000000dU) 
                                                            | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[22U])))) 
                       >> 0x00000020U)) >> 2U));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[10U] 
        = ((0x0000001fU & vlSelfRef.milan_datapath__DOT__cmap_flat_w[10U]) 
           | ((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[27U])) 
                        << 0x0000001aU) | (QData)((IData)(
                                                          (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[26U]) 
                                                            << 0x0000000dU) 
                                                           | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[25U]))))) 
              << 5U));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[11U] 
        = ((0xfffff000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[11U]) 
           | (((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[27U])) 
                         << 0x0000001aU) | (QData)((IData)(
                                                           (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[26U]) 
                                                             << 0x0000000dU) 
                                                            | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[25U]))))) 
               >> 0x0000001bU) | ((IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[27U])) 
                                             << 0x0000001aU) 
                                            | (QData)((IData)(
                                                              (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[26U]) 
                                                                << 0x0000000dU) 
                                                               | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[25U])))) 
                                           >> 0x00000020U)) 
                                  << 5U)));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[11U] 
        = ((0x00000fffU & vlSelfRef.milan_datapath__DOT__cmap_flat_w[11U]) 
           | ((IData)((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[31U]) 
                                          << 0x0000000dU) 
                                         | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[30U]))) 
                        << 0x0000001aU) | (QData)((IData)(
                                                          (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[29U]) 
                                                            << 0x0000000dU) 
                                                           | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[28U]))))) 
              << 0x0000000cU));
    vlSelfRef.milan_datapath__DOT__cmap_flat_w[12U] 
        = (((IData)((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[31U]) 
                                        << 0x0000000dU) 
                                       | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[30U]))) 
                      << 0x0000001aU) | (QData)((IData)(
                                                        (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[29U]) 
                                                          << 0x0000000dU) 
                                                         | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[28U]))))) 
            >> 0x00000014U) | ((IData)(((((QData)((IData)(
                                                          (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[31U]) 
                                                            << 0x0000000dU) 
                                                           | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[30U]))) 
                                          << 0x0000001aU) 
                                         | (QData)((IData)(
                                                           (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[29U]) 
                                                             << 0x0000000dU) 
                                                            | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[28U])))) 
                                        >> 0x00000020U)) 
                               << 0x0000000cU));
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
    if (vlSelfRef.axis_resetn) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p1_d_r 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w;
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
            if ((0x013fU >= (0x000001ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r) 
                                            << 6U)))) {
                VL_ASSIGNSEL_WQ(320, 64, (0x000001ffU 
                                          & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r) 
                                             << 6U)), vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_disc_eid_w);
            }
            if ((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r) 
                       | (0x1fU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r))));
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_disc_disarm_w) {
            if ((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_vld_r) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__accept_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_vld_r = 0U;
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
        if (vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__aaf_tx_acc_w) {
            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__aaf_tx_inframe_r 
                = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_tx_tlast)));
        }
        if (vlSelfRef.s_axis_mac_rx_tvalid) {
            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__mac_rx_inframe_r 
                = (1U & (~ (IData)(vlSelfRef.s_axis_mac_rx_tlast)));
        }
        vlSelfRef.milan_datapath__DOT__csr__DOT__stats_rst_p = 0U;
        vlSelfRef.milan_datapath__DOT__speed_q = vlSelfRef.milan_datapath__DOT__speed_sync;
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
            = ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_r))
                ? 0U : (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_r))));
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
        if ((0x0001869fU <= vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ms_div_r)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ms_div_r = 0U;
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ms_tick_r = 1U;
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ms_div_r 
                = (0x0001ffffU & ((IData)(1U) + vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ms_div_r));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ms_tick_r = 0U;
        }
        if ((0xffU <= (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_div_r))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_div_r = 0U;
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_tick_r = 1U;
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_div_r 
                = (0x000000ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_div_r)));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_tick_r = 0U;
        }
        vlSelfRef.milan_datapath__DOT__strtbl_bind_rise_w 
            = ((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w) 
               & (~ (IData)(vlSelfRef.milan_datapath__DOT__stream_table__DOT__en_q_r)));
        vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w 
            = ((~ (IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w)) 
               & (IData)(vlSelfRef.milan_datapath__DOT__stream_table__DOT__en_q_r));
        if (((IData)(vlSelfRef.s_axis_mac_rx_tvalid) 
             & (IData)(vlSelfRef.s_axis_mac_rx_tlast))) {
            vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__tl_idx_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_p)
                    ? (IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_idx_w)
                    : (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__wv_idx_r));
            vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__good_r = 0U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_p) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__in_frame_r) 
                       | (IData)(vlSelfRef.s_axis_mac_rx_tvalid)))) {
            vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__good_r = 1U;
        }
        vlSelfRef.milan_datapath__DOT__pcmrx_pdu_p_w = 0U;
        if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r))) {
            if (vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__pop_w) {
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r 
                    = ((7U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r))
                        ? 7U : (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r))));
                if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r))) {
                    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__163__w 
                        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_0__fbyte 
                        = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__163__w 
                                                  >> 0x20U)));
                    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__164__w 
                        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_1__fbyte 
                        = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__164__w 
                                                  >> 0x28U)));
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r 
                        = ((0x81U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_0__fbyte)) 
                           & (0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_1__fbyte)));
                }
                if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r))) {
                    if (vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r) {
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__165__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_2__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__165__w 
                                                      >> 0x30U)));
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__166__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_3__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__166__w 
                                                      >> 0x38U)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r 
                            = (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_2__fbyte) 
                                << 8U) | (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_3__fbyte));
                    } else {
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__167__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__169__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_4__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__167__w 
                                                      >> 0x10U)));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_6__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__169__w 
                                                      >> 0x38U)));
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__168__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__170__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r = 1U;
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_5__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__168__w 
                                                      >> 0x18U)));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_7__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__170__w 
                                                      >> 0x30U)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r 
                            = (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_4__fbyte) 
                                << 8U) | (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_5__fbyte));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_6__fbyte)) 
                                << 8U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_7__fbyte)));
                    }
                }
                if (((5U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r)) 
                     & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r))) {
                    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__171__w 
                        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_8__fbyte 
                        = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__171__w 
                                                  >> 0x38U)));
                    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__172__w 
                        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r = 1U;
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_9__fbyte 
                        = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__172__w 
                                                  >> 0x30U)));
                    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__173__w 
                        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_10__fbyte 
                        = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__173__w 
                                                  >> 0x28U)));
                    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__174__w 
                        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_11__fbyte 
                        = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__174__w 
                                                  >> 0x20U)));
                    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__175__w 
                        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_12__fbyte 
                        = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__175__w 
                                                  >> 0x18U)));
                    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__176__w 
                        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_13__fbyte 
                        = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__176__w 
                                                  >> 0x10U)));
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r 
                        = (((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_8__fbyte) 
                                              << 8U) 
                                             | (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_9__fbyte)))) 
                            << 0x00000020U) | (QData)((IData)(
                                                              ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_10__fbyte) 
                                                                 << 0x00000018U) 
                                                                | ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_11__fbyte) 
                                                                   << 0x00000010U)) 
                                                               | (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_12__fbyte) 
                                                                   << 8U) 
                                                                  | (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_13__fbyte))))));
                }
                if ((0x00000100U & vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][2U])) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r = 0U;
                }
            }
        } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r))) {
            if (vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w) {
                if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_only_w)))) {
                    if (vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r) {
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__177__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_14__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__177__w 
                                                      >> 0x38U)));
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__178__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_15__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__178__w 
                                                      >> 0x30U)));
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__179__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_16__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__179__w 
                                                      >> 0x28U)));
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__180__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_17__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__180__w 
                                                      >> 0x20U)));
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__181__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_18__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__181__w 
                                                      >> 0x18U)));
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__182__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_19__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__182__w 
                                                      >> 0x10U)));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCond_22 
                            = (((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_14__fbyte) 
                                                  << 8U) 
                                                 | (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_15__fbyte)))) 
                                << 0x00000020U) | (QData)((IData)(
                                                                  ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_16__fbyte) 
                                                                     << 0x00000018U) 
                                                                    | ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_17__fbyte) 
                                                                       << 0x00000010U)) 
                                                                   | (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_18__fbyte) 
                                                                       << 8U) 
                                                                      | (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_19__fbyte))))));
                    } else {
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__183__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_20__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__183__w 
                                                      >> 0x38U)));
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__184__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_21__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__184__w 
                                                      >> 0x30U)));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCond_22 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_20__fbyte)) 
                                << 8U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_21__fbyte)));
                    }
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r 
                        = vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCond_22;
                }
                if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r))) {
                    vlSelfRef.milan_datapath__DOT__pcmrx_pdus 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdus)));
                    vlSelfRef.milan_datapath__DOT__pcmrx_pdu_p_w = 1U;
                    vlSelfRef.milan_datapath__DOT__pcmrx_pdu_idx_w 
                        = vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                        [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r];
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r 
                        = ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_only_w) 
                                   | (~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__pop_w))) 
                                  | (~ (vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][2U] 
                                        >> 8U)))) ? 
                           ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_only_w) 
                                   | (~ (vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][2U] 
                                         >> 8U)))) ? 2U
                             : 0U) : 0U);
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r 
                        = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r) 
                                          - (IData)(8U)));
                }
            }
            if ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__pop_w) 
                  & (vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][2U] 
                     >> 8U)) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w) 
                                   & (8U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r)))))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r = 0U;
            }
        } else if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r))) {
            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__pop_w) 
                 & (vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][2U] 
                    >> 8U))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r = 0U;
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r = 0U;
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
                if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wmsg_w) 
                      >> 3U) & ((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)) 
                                && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                                          >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_code_r 
                        = (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wmsg_w));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_fp_r 
                        = ((9U >= (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r) 
                                                  << 1U)))
                            ? (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r) 
                                     >> (0x0000000fU 
                                         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r) 
                                            << 1U))))
                            : 0U);
                    if ((0x013fU >= (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275))) {
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
                                                           + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275)) 
                                                          >> 5U)])) 
                                         << ((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275)))
                                              ? 0x00000020U
                                              : ((IData)(0x00000040U) 
                                                 - 
                                                 (0x0000001fU 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275))))) 
                                        | (((0U == 
                                             (0x0000001fU 
                                              & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275)))
                                             ? 0ULL
                                             : ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r
                                                                [
                                                                (((IData)(0x0000001fU) 
                                                                  + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275)) 
                                                                 >> 5U)])) 
                                                << 
                                                ((IData)(0x00000020U) 
                                                 - 
                                                 (0x0000001fU 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275))))) 
                                           | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r
                                                              [
                                                              ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275) 
                                                               >> 5U)])) 
                                              >> (0x0000001fU 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275)))))) 
                               << 0x00000010U);
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r[7U] 
                            = (((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r
                                                          [
                                                          (((IData)(0x0000003fU) 
                                                            + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275)) 
                                                           >> 5U)])) 
                                          << ((0U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275)))
                                               ? 0x00000020U
                                               : ((IData)(0x00000040U) 
                                                  - 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275))))) 
                                         | (((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275)))
                                              ? 0ULL
                                              : ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r
                                                                 [
                                                                 (((IData)(0x0000001fU) 
                                                                   + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275)) 
                                                                  >> 5U)])) 
                                                 << 
                                                 ((IData)(0x00000020U) 
                                                  - 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275))))) 
                                            | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r
                                                               [
                                                               ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275) 
                                                                >> 5U)])) 
                                               >> (0x0000001fU 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275)))))) 
                                >> 0x00000010U) | ((IData)(
                                                           ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r
                                                                              [
                                                                              (((IData)(0x0000003fU) 
                                                                                + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275)) 
                                                                               >> 5U)])) 
                                                              << 
                                                              ((0U 
                                                                == 
                                                                (0x0000001fU 
                                                                 & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275)))
                                                                ? 0x00000020U
                                                                : 
                                                               ((IData)(0x00000040U) 
                                                                - 
                                                                (0x0000001fU 
                                                                 & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275))))) 
                                                             | (((0U 
                                                                  == 
                                                                  (0x0000001fU 
                                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275)))
                                                                  ? 0ULL
                                                                  : 
                                                                 ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r
                                                                                [
                                                                                (((IData)(0x0000001fU) 
                                                                                + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275)) 
                                                                                >> 5U)])) 
                                                                  << 
                                                                  ((IData)(0x00000020U) 
                                                                   - 
                                                                   (0x0000001fU 
                                                                    & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275))))) 
                                                                | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r
                                                                                [
                                                                                ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275) 
                                                                                >> 5U)])) 
                                                                   >> 
                                                                   (0x0000001fU 
                                                                    & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275))))) 
                                                            >> 0x00000020U)) 
                                                   << 0x00000010U));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r[8U] 
                            = ((IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r
                                                          [
                                                          (((IData)(0x0000003fU) 
                                                            + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275)) 
                                                           >> 5U)])) 
                                          << ((0U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275)))
                                               ? 0x00000020U
                                               : ((IData)(0x00000040U) 
                                                  - 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275))))) 
                                         | (((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275)))
                                              ? 0ULL
                                              : ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r
                                                                 [
                                                                 (((IData)(0x0000001fU) 
                                                                   + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275)) 
                                                                  >> 5U)])) 
                                                 << 
                                                 ((IData)(0x00000020U) 
                                                  - 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275))))) 
                                            | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r
                                                               [
                                                               ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275) 
                                                                >> 5U)])) 
                                               >> (0x0000001fU 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275))))) 
                                        >> 0x00000020U)) 
                               >> 0x00000010U);
                    } else {
                        VL_ASSIGN_W(272, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r, Vmilan_datapath__ConstPool__CONST_hc5471b50_0);
                    }
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r = 2U;
                } else if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r = 3U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r 
                        = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)));
                }
            }
        } else if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r))) {
            if (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_284) 
                 & ((2U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r)) 
                    & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r))))) {
                if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r = 3U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r 
                        = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)));
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
            if (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_28)
                  ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_15)
                  : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_51)
                      ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_15)
                      : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_50)
                          ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_15)
                          : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39)
                              ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_15)
                              : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_49)
                                  ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_15)
                                  : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_15) 
                                     | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_70)))))))) {
                if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wmsg_w) 
                      >> 3U) & ((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r)) 
                                && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                          >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r)))))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_code_r 
                        = (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wmsg_w));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_type_r 
                        = (((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r)) 
                            && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r) 
                                      >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r))))
                            ? 2U : 1U);
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r = 2U;
                    if (((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r)) 
                         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r) 
                            >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r)))) {
                        __Vtemp_11[0U] = (1U | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w) 
                                                << 8U));
                        __Vtemp_11[1U] = (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w) 
                                           >> 0x00000018U) 
                                          | ((IData)(
                                                     (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                      >> 0x00000020U)) 
                                             << 8U));
                        __Vtemp_11[2U] = ((IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                   >> 0x00000020U)) 
                                          >> 0x00000018U);
                    } else {
                        __Vtemp_11[0U] = 0U;
                        __Vtemp_11[1U] = 0U;
                        __Vtemp_11[2U] = 0U;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[0U] 
                        = __Vtemp_11[0U];
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[1U] 
                        = __Vtemp_11[1U];
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[2U] 
                        = ((0xffffff00U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[2U]) 
                           | __Vtemp_11[2U]);
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[2U] 
                        = ((0x000000ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[2U]) 
                           | (((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_245)))
                                  ? 0U : (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lat_r
                                          [(((IData)(0x0000001fU) 
                                             + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_245)) 
                                            >> 5U)] 
                                          << ((IData)(0x00000020U) 
                                              - (0x0000001fU 
                                                 & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_245))))) 
                                | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lat_r
                                   [((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_245) 
                                     >> 5U)] >> (0x0000001fU 
                                                 & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_245)))) 
                               & (- (IData)((0x9fU 
                                             >= (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_245))))) 
                              << 8U));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[3U] 
                        = ((0xffffff00U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[3U]) 
                           | (((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_245)))
                                  ? 0U : (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lat_r
                                          [(((IData)(0x0000001fU) 
                                             + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_245)) 
                                            >> 5U)] 
                                          << ((IData)(0x00000020U) 
                                              - (0x0000001fU 
                                                 & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_245))))) 
                                | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lat_r
                                   [((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_245) 
                                     >> 5U)] >> (0x0000001fU 
                                                 & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_245)))) 
                               & (- (IData)((0x9fU 
                                             >= (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_245))))) 
                              >> 0x00000018U));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[3U] 
                        = ((0x000000ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[3U]) 
                           | ((((((0U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95)))
                                   ? 0U : (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__mif_r
                                           [(((IData)(0x0000000fU) 
                                              + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95)) 
                                             >> 5U)] 
                                           << ((IData)(0x00000020U) 
                                               - (0x0000001fU 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95))))) 
                                 | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__mif_r
                                    [((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95) 
                                      >> 5U)] >> (0x0000001fU 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95)))) 
                                & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246)) 
                               << 0x00000010U) | ((
                                                   (0x000000e0U 
                                                    & ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__prio_r) 
                                                         >> (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_146)) 
                                                        & (- (IData)(
                                                                     (0x0eU 
                                                                      >= (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_146))))) 
                                                       << 5U)) 
                                                   | (((4U 
                                                        >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r)) 
                                                       & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rank_r) 
                                                          >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r))) 
                                                      << 4U)) 
                                                  << 8U)));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[4U] 
                        = ((0x0fff0000U & (((IData)(
                                                    (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vid_r 
                                                     >> (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_145))) 
                                            & (- (IData)(
                                                         (0x3bU 
                                                          >= (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_145))))) 
                                           << 0x00000010U)) 
                           | ((((0U == (0x0000001fU 
                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95)))
                                 ? 0U : (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__mfs_r
                                         [(((IData)(0x0000000fU) 
                                            + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95)) 
                                           >> 5U)] 
                                         << ((IData)(0x00000020U) 
                                             - (0x0000001fU 
                                                & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95))))) 
                               | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__mfs_r
                                  [((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95) 
                                    >> 5U)] >> (0x0000001fU 
                                                & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95)))) 
                              & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246)));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[5U] 
                        = (IData)((0x0000ffffffffffffULL 
                                   & ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r
                                                        [
                                                        (((IData)(0x0000002fU) 
                                                          + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144)) 
                                                         >> 5U)])) 
                                        << ((0U == 
                                             (0x0000001fU 
                                              & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144)))
                                             ? 0x00000020U
                                             : ((IData)(0x00000040U) 
                                                - (0x0000001fU 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144))))) 
                                       | (((0U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144)))
                                            ? 0ULL : 
                                           ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r
                                                            [
                                                            (((IData)(0x0000001fU) 
                                                              + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144)) 
                                                             >> 5U)])) 
                                            << ((IData)(0x00000020U) 
                                                - (0x0000001fU 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144))))) 
                                          | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r
                                                             [
                                                             ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144) 
                                                              >> 5U)])) 
                                             >> (0x0000001fU 
                                                 & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144))))) 
                                      & (- (QData)((IData)(
                                                           (0xefU 
                                                            >= (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144))))))));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[6U] 
                        = ((0xffff0000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[6U]) 
                           | (IData)(((0x0000ffffffffffffULL 
                                       & ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r
                                                            [
                                                            (((IData)(0x0000002fU) 
                                                              + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144)) 
                                                             >> 5U)])) 
                                            << ((0U 
                                                 == 
                                                 (0x0000001fU 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144)))
                                                 ? 0x00000020U
                                                 : 
                                                ((IData)(0x00000040U) 
                                                 - 
                                                 (0x0000001fU 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144))))) 
                                           | (((0U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144)))
                                                ? 0ULL
                                                : ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r
                                                                   [
                                                                   (((IData)(0x0000001fU) 
                                                                     + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144)) 
                                                                    >> 5U)])) 
                                                   << 
                                                   ((IData)(0x00000020U) 
                                                    - 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144))))) 
                                              | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r
                                                                 [
                                                                 ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144) 
                                                                  >> 5U)])) 
                                                 >> 
                                                 (0x0000001fU 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144))))) 
                                          & (- (QData)((IData)(
                                                               (0xefU 
                                                                >= (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144))))))) 
                                      >> 0x00000020U)));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[6U] 
                        = ((0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[6U]) 
                           | ((IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__sid_r
                                                         [
                                                         (((IData)(0x0000003fU) 
                                                           + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247)) 
                                                          >> 5U)])) 
                                         << ((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247)))
                                              ? 0x00000020U
                                              : ((IData)(0x00000040U) 
                                                 - 
                                                 (0x0000001fU 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247))))) 
                                        | (((0U == 
                                             (0x0000001fU 
                                              & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247)))
                                             ? 0ULL
                                             : ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__sid_r
                                                                [
                                                                (((IData)(0x0000001fU) 
                                                                  + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247)) 
                                                                 >> 5U)])) 
                                                << 
                                                ((IData)(0x00000020U) 
                                                 - 
                                                 (0x0000001fU 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247))))) 
                                           | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__sid_r
                                                              [
                                                              ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247) 
                                                               >> 5U)])) 
                                              >> (0x0000001fU 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247))))) 
                                       & (- (QData)((IData)(
                                                            (0x013fU 
                                                             >= (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247))))))) 
                              << 0x00000010U));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[7U] 
                        = (((IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__sid_r
                                                       [
                                                       (((IData)(0x0000003fU) 
                                                         + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247)) 
                                                        >> 5U)])) 
                                       << ((0U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247)))
                                            ? 0x00000020U
                                            : ((IData)(0x00000040U) 
                                               - (0x0000001fU 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247))))) 
                                      | (((0U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247)))
                                           ? 0ULL : 
                                          ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__sid_r
                                                           [
                                                           (((IData)(0x0000001fU) 
                                                             + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247)) 
                                                            >> 5U)])) 
                                           << ((IData)(0x00000020U) 
                                               - (0x0000001fU 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247))))) 
                                         | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__sid_r
                                                            [
                                                            ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247) 
                                                             >> 5U)])) 
                                            >> (0x0000001fU 
                                                & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247))))) 
                                     & (- (QData)((IData)(
                                                          (0x013fU 
                                                           >= (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247))))))) 
                            >> 0x00000010U) | ((IData)(
                                                       (((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__sid_r
                                                                           [
                                                                           (((IData)(0x0000003fU) 
                                                                             + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247)) 
                                                                            >> 5U)])) 
                                                           << 
                                                           ((0U 
                                                             == 
                                                             (0x0000001fU 
                                                              & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247)))
                                                             ? 0x00000020U
                                                             : 
                                                            ((IData)(0x00000040U) 
                                                             - 
                                                             (0x0000001fU 
                                                              & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247))))) 
                                                          | (((0U 
                                                               == 
                                                               (0x0000001fU 
                                                                & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247)))
                                                               ? 0ULL
                                                               : 
                                                              ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__sid_r
                                                                               [
                                                                               (((IData)(0x0000001fU) 
                                                                                + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247)) 
                                                                                >> 5U)])) 
                                                               << 
                                                               ((IData)(0x00000020U) 
                                                                - 
                                                                (0x0000001fU 
                                                                 & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247))))) 
                                                             | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__sid_r
                                                                                [
                                                                                ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247) 
                                                                                >> 5U)])) 
                                                                >> 
                                                                (0x0000001fU 
                                                                 & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247))))) 
                                                         & (- (QData)((IData)(
                                                                              (0x013fU 
                                                                               >= (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247)))))) 
                                                        >> 0x00000020U)) 
                                               << 0x00000010U));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[8U] 
                        = ((IData)((((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__sid_r
                                                       [
                                                       (((IData)(0x0000003fU) 
                                                         + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247)) 
                                                        >> 5U)])) 
                                       << ((0U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247)))
                                            ? 0x00000020U
                                            : ((IData)(0x00000040U) 
                                               - (0x0000001fU 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247))))) 
                                      | (((0U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247)))
                                           ? 0ULL : 
                                          ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__sid_r
                                                           [
                                                           (((IData)(0x0000001fU) 
                                                             + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247)) 
                                                            >> 5U)])) 
                                           << ((IData)(0x00000020U) 
                                               - (0x0000001fU 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247))))) 
                                         | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__sid_r
                                                            [
                                                            ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247) 
                                                             >> 5U)])) 
                                            >> (0x0000001fU 
                                                & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247))))) 
                                     & (- (QData)((IData)(
                                                          (0x013fU 
                                                           >= (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247)))))) 
                                    >> 0x00000020U)) 
                           >> 0x00000010U);
                } else if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r = 3U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r 
                        = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r)));
                }
            }
        } else if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r))) {
            if (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_284) 
                 & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r)))) {
                if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r = 3U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r 
                        = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r)));
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
                         & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_158))) {
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
                                                        (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_161 
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
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rgray_w2_r 
            = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rgray_w1_r;
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__eth_guard 
                                                                                = 
                                                                                (0x554e4c4bU 
                                                                                != vlSelfRef.s_axi_wdata);
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
                                                                                ((4U 
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
                                                                            ((4U 
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
                                                                        (4U 
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
                                                                            (4U 
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
                                                                        (4U 
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
                                                                        (4U 
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
                                                                    (4U 
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
        }
        vlSelfRef.milan_datapath__DOT__speed_sync = vlSelfRef.milan_datapath__DOT__speed_meta;
        vlSelfRef.milan_datapath__DOT__rsp_tuser_w 
            = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r;
        vlSelfRef.milan_datapath__DOT__rsp_pop_p_w = 0U;
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_take_w) 
             & (0U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))) {
            vlSelfRef.milan_datapath__DOT__rsp_pop_p_w 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__rsp_pop_p_w));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_take_w) 
             & (1U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))) {
            vlSelfRef.milan_datapath__DOT__rsp_pop_p_w 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__rsp_pop_p_w));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_take_w) 
             & (2U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))) {
            vlSelfRef.milan_datapath__DOT__rsp_pop_p_w 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__rsp_pop_p_w));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_take_w) 
             & (3U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))) {
            vlSelfRef.milan_datapath__DOT__rsp_pop_p_w 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__rsp_pop_p_w));
        }
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__tick_d_r 
            = (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__sched_r) 
                & (3U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__beat_r))) 
               & (3U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)));
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
                if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r))) {
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
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__alloc_req_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__abort_pend_r = 0U;
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__alloc_req_r) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__v_alloc_gnt_w) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__slot_held_r = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__slot_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ff_slot_w;
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r = 2U;
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__ser_busy_r) {
            if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r))) {
                if ((5U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_own_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_own_a_w;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mcast_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mcast_a_w;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_maap_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_maap_a_w;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_msrp_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_msrp_a_w;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mvrp_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mvrp_a_w;
                    if (((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r)) 
                         & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_1722_a_w) 
                               | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mrp_a_w))))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r = 2U;
                    }
                }
                if (((6U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r)) 
                     & (0x000bU >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r)))) {
                    if ((0x2fU >= (0x0000003fU & (((IData)(0x0000000bU) 
                                                   - (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r)) 
                                                  << 3U)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__src_mac_r 
                            = (((~ (0x00000000000000ffULL 
                                    << (0x0000003fU 
                                        & (((IData)(0x0000000bU) 
                                            - (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r)) 
                                           << 3U)))) 
                                & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__src_mac_r) 
                               | (0x0000ffffffffffffULL 
                                  & ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w)) 
                                     << (0x0000003fU 
                                         & (((IData)(0x0000000bU) 
                                             - (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r)) 
                                            << 3U)))));
                    }
                }
                if ((0x000cU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__et_hi_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w;
                }
                if ((0x000dU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r))) {
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_1722_a_w) {
                        if (((0x22f0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__et_w)) 
                             & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__end_w)))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r = 1U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__alloc_req_r = 1U;
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r = 2U;
                        }
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r = 2U;
                    }
                }
            } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pdu_byte_w) 
                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__in_budget_w))) {
                    if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__msg_type_r 
                            = (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w));
                    }
                    if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__status_r 
                            = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
                                              >> 3U));
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cdl_r 
                            = ((0x00ffU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cdl_r)) 
                               | (0x00000700U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
                                                 << 8U)));
                    }
                    if (((4U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w)) 
                         & (0x000bU >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__target_eid_r 
                            = (((~ (0x00000000000000ffULL 
                                    << (0x0000003fU 
                                        & (((IData)(0x0000000bU) 
                                            - (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w)) 
                                           << 3U)))) 
                                & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__target_eid_r) 
                               | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w)) 
                                  << (0x0000003fU & 
                                      (((IData)(0x0000000bU) 
                                        - (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w)) 
                                       << 3U))));
                    }
                    if ((((0xfaU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__subtype_r)) 
                          & (0x000cU <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) 
                         & (0x0013U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__ctlr_eid_r 
                            = (((~ (0x00000000000000ffULL 
                                    << (0x0000003fU 
                                        & (((IData)(0x00000013U) 
                                            - (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w)) 
                                           << 3U)))) 
                                & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__ctlr_eid_r) 
                               | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w)) 
                                  << (0x0000003fU & 
                                      (((IData)(0x00000013U) 
                                        - (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w)) 
                                       << 3U))));
                    }
                    if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cdl_r 
                            = ((0x0700U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cdl_r)) 
                               | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cdl_known_r = 1U;
                    }
                    if ((0xfbU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__subtype_r))) {
                        if ((0x0014U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__seq_r 
                                = ((0x00ffU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__seq_r)) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
                                      << 8U));
                        }
                        if ((0x0016U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__u_r 
                                = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
                                         >> 7U));
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cr_r 
                                = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
                                         >> 6U));
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__opcode_r 
                                = ((0x00ffU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__opcode_r)) 
                                   | (0x00003f00U & 
                                      ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
                                       << 8U)));
                        }
                        if ((0x0018U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_type_r 
                                = ((0x00ffU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_type_r)) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
                                      << 8U));
                        }
                        if ((0x001aU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_index_r 
                                = ((0x00ffU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_index_r)) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
                                      << 8U));
                        }
                        if ((0x0015U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__seq_r 
                                = ((0xff00U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__seq_r)) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w));
                        }
                        if ((0x0017U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__opcode_r 
                                = ((0xff00U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__opcode_r)) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w));
                        }
                        if ((0x0019U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_type_r 
                                = ((0xff00U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_type_r)) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w));
                        }
                        if ((0x001bU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_index_r 
                                = ((0xff00U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_index_r)) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w));
                        }
                    }
                    if ((0xfcU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__subtype_r))) {
                        if ((0x0024U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__tuid_r 
                                = ((0x00ffU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__tuid_r)) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
                                      << 8U));
                        }
                        if ((0x0026U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__luid_r 
                                = ((0x00ffU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__luid_r)) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
                                      << 8U));
                        }
                        if ((0x0030U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__seq_r 
                                = ((0x00ffU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__seq_r)) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
                                      << 8U));
                        }
                        if ((0x0025U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__tuid_r 
                                = ((0xff00U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__tuid_r)) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w));
                        }
                        if ((0x0027U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__luid_r 
                                = ((0xff00U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__luid_r)) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w));
                        }
                        if ((0x0031U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__seq_r 
                                = ((0xff00U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__seq_r)) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w));
                        }
                    }
                    if ((0xfeU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__subtype_r))) {
                        if ((0x0014U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_type_r 
                                = ((0x00ffU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_type_r)) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
                                      << 8U));
                        }
                        if ((0x0016U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_index_r 
                                = ((0x00ffU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_index_r)) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
                                      << 8U));
                        }
                        if ((0x0018U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__tuid_r 
                                = ((0x00ffU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__tuid_r)) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
                                      << 8U));
                        }
                        if ((0x001aU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__luid_r 
                                = ((0x00ffU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__luid_r)) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
                                      << 8U));
                        }
                        if ((0x0015U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_type_r 
                                = ((0xff00U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_type_r)) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w));
                        }
                        if ((0x0017U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_index_r 
                                = ((0xff00U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_index_r)) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w));
                        }
                        if ((0x0019U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__tuid_r 
                                = ((0xff00U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__tuid_r)) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w));
                        }
                        if ((0x001bU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__luid_r 
                                = ((0xff00U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__luid_r)) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w));
                        }
                    }
                    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__subtype_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w;
                    }
                }
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fail_now_w) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r = 2U;
                }
            }
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__end_w) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r = 0U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_own_r = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mcast_r = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_maap_r = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_msrp_r = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mvrp_r = 1U;
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r 
                    = (0x000007ffU & ((0x07ffU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r))
                                       ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r)
                                       : ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r))));
            }
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fail_now_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__slot_now_w)) 
             | (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__end_w) 
                   & (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r))) 
                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__slot_now_w)) 
                 & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fail_now_w))) 
                & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__v1_pass_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__abort_pend_r = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__abort_pend_r) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__slot_held_r = 0U;
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
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__slot_held_r = 0U;
        }
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cp_r 
            = ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cp_r) 
                      << 1U)) | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__end_pend_r) 
                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__end_pass_r)));
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__end_pend_r) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__subtype_r = 0U;
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__end_pass_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_msg_type_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__msg_type_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_status_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__status_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_cdl_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cdl_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_src_mac_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__src_mac_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_target_eid_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__target_eid_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_seq_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__seq_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_u_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__u_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_cr_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cr_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_rx_slot_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__slot_r;
                if ((0xfaU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__subtype_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r = 0ULL;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_protocol_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_opcode_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__msg_type_r;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_operands_r = 0ULL;
                } else {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__ctlr_eid_r;
                    if ((0xfeU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__subtype_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_protocol_r = 5U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_opcode_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__msg_type_r;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_operands_r 
                            = (((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_type_r) 
                                                  << 0x00000010U) 
                                                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_index_r)))) 
                                << 0x00000020U) | (QData)((IData)(
                                                                  (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__tuid_r) 
                                                                    << 0x00000010U) 
                                                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__luid_r)))));
                    } else if ((0xfcU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__subtype_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_protocol_r = 1U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_opcode_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__msg_type_r;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_operands_r 
                            = (QData)((IData)((((((0U 
                                                   == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__msg_type_r)) 
                                                  | (2U 
                                                     == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__msg_type_r))) 
                                                 | (4U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__msg_type_r))) 
                                                | (0x0cU 
                                                   == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__msg_type_r)))
                                                ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__tuid_r)
                                                : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__luid_r))));
                    } else {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_protocol_r 
                            = (((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__msg_type_r)) 
                                | (7U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__msg_type_r)))
                                ? 3U : (((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__msg_type_r)) 
                                         | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__msg_type_r)))
                                         ? 4U : 2U));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_opcode_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__opcode_r;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_operands_r 
                            = ((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_type_r) 
                                                 << 0x00000010U) 
                                                | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_index_r)))) 
                               << 0x00000020U);
                    }
                }
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cdl_known_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__msg_type_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__status_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cdl_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__src_mac_r = 0ULL;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__target_eid_r = 0ULL;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__ctlr_eid_r = 0ULL;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__seq_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__opcode_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_type_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_index_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__tuid_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__luid_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__u_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cr_r = 0U;
        }
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__en_q_r 
            = vlSelfRef.milan_datapath__DOT__strtbl_en_w;
        if (((IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_p) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__in_frame_r) 
                | (IData)(vlSelfRef.s_axis_mac_rx_tvalid)))) {
            vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__wv_idx_r 
                = vlSelfRef.milan_datapath__DOT__avtprx_accept_idx_w;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w) 
             & (1U == (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r 
                = ((0x03fcU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r)) 
                   | (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_fp_r)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w) 
                      >> 1U) & (4U == (0x000cU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r 
                = ((0x03f3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r)) 
                   | (0x0000000cU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_fp_r)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w) 
                      >> 2U) & (0x0010U == (0x0030U 
                                            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r 
                = ((0x03cfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r)) 
                   | (0x00000030U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_fp_r)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w) 
                      >> 3U) & (0x0040U == (0x00c0U 
                                            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r 
                = ((0x033fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r)) 
                   | (0x000000c0U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_fp_r)));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w) 
                      >> 4U) & (0x0100U == (0x0300U 
                                            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r 
                = ((0x00ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r)) 
                   | (0x00000300U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_fp_r)));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r) {
                if ((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r 
                        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                           | (0x1fU & ((IData)(1U) 
                                       << (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))));
                }
                if ((0x013fU >= (0x000001c0U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r) 
                                                << 6U)))) {
                    VL_ASSIGNSEL_WQ(320, 64, (0x000001c0U 
                                              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r) 
                                                 << 6U)), vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_sid_r);
                }
                if ((9U >= (0x0000000eU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r) 
                                           << 1U)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r 
                        = ((~ ((IData)(3U) << (0x0000000eU 
                                               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r) 
                                                  << 1U)))) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r));
                }
            }
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_join_fsm_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_la_msrp_r = 0U;
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_hit_w) {
            if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                           - (IData)(0x0000003bU)) 
                          >> 2U)))) {
                if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                               - (IData)(0x0000003bU)) 
                              >> 1U)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                  - (IData)(1U))))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_join_fsm_r = 1U;
                    }
                }
                if ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                           - (IData)(0x0000003bU)))) {
                    if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                               - (IData)(1U)))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_la_msrp_r = 1U;
                    }
                }
            }
        }
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__adm_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r 
                = ((0x1eU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r)) 
                   | (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__sr_adm_fsm_w))));
        }
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__adm_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r 
                = ((0x1dU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r)) 
                   | (2U & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__sr_adm_fsm_w) 
                                >> 1U)) << 1U)));
        }
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__adm_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r 
                = ((0x1bU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r)) 
                   | (4U & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__sr_adm_fsm_w) 
                                >> 2U)) << 2U)));
        }
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__adm_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r 
                = ((0x17U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r)) 
                   | (8U & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__sr_adm_fsm_w) 
                                >> 3U)) << 3U)));
        }
        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__adm_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r 
                = ((0x0fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r)) 
                   | (0x00000010U & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__sr_adm_fsm_w) 
                                         >> 4U)) << 4U)));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r) {
                if ((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rank_r 
                        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rank_r) 
                           | (0x1fU & ((IData)(1U) 
                                       << (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))));
                }
                if ((0x4fU >= (0x00000070U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r) 
                                              << 4U)))) {
                    VL_ASSIGNSEL_WI(80, 16, (0x00000070U 
                                             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r) 
                                                << 4U)), vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__mfs_r, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_mfs_r);
                    VL_ASSIGNSEL_WI(80, 16, (0x00000070U 
                                             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r) 
                                                << 4U)), vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__mif_r, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_mif_r);
                }
                if ((0x0eU >= (0x0000000fU & ((IData)(3U) 
                                              * (7U 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__prio_r 
                        = (((~ ((IData)(7U) << (0x0000000fU 
                                                & ((IData)(3U) 
                                                   * 
                                                   (7U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) 
                            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__prio_r)) 
                           | (0x7fffU & ((7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__decl_prio_r)) 
                                         << (0x0000000fU 
                                             & ((IData)(3U) 
                                                * (7U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))));
                }
                if ((0x9fU >= (0x000000e0U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r) 
                                              << 5U)))) {
                    VL_ASSIGNSEL_WI(160, 32, (0x000000e0U 
                                              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r) 
                                                 << 5U)), vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lat_r, vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_lat);
                }
            }
            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)))) {
                if ((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r 
                        = ((~ ((IData)(1U) << (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r));
                }
            }
        }
    } else {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p1_d_r = 0U;
        vlSelfRef.milan_datapath__DOT__wing_sid_hi_r = 0U;
        vlSelfRef.milan_datapath__DOT__wing_sid_lo_r = 0U;
        VL_ASSIGN_W(320, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r, Vmilan_datapath__ConstPool__CONST_hab76c978_0);
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
        vlSelfRef.milan_datapath__DOT__csr__DOT__phy_rst = 1U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__link_ctrl = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_taint_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__aaf_tx_inframe_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__mac_rx_inframe_r = 0U;
        vlSelfRef.milan_datapath__DOT__speed_q = 2U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_side_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__frame_bytes_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_q1_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_base_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_len_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ms_div_r = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ms_tick_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_div_r = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_tick_r = 0U;
        vlSelfRef.milan_datapath__DOT__strtbl_bind_rise_w = 0U;
        vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__tl_idx_r = 0U;
        vlSelfRef.milan_datapath__DOT__pcmrx_pdus = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pcmrx_pdu_p_w = 0U;
        vlSelfRef.milan_datapath__DOT__pcmrx_pdu_idx_w = 0U;
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
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rgray_w2_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl = 0x00020000U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_dmlo = 0xf000fe01U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_dmhi = 0x000091e0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_p_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_data_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_p_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_data_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__eth_guard = 1U;
        vlSelfRef.milan_datapath__DOT__speed_sync = 2U;
        vlSelfRef.__Vdly__milan_datapath__DOT__render_setpoint__DOT__sched_r = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__tick_q_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__render_setpoint__DOT__slot_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__render_setpoint__DOT__beat_r = 0U;
        vlSelfRef.milan_datapath__DOT__rsp_tuser_w = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__tick_d_r = 0U;
        vlSelfRef.milan_datapath__DOT__rsp_pop_p_w = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ev_ok_r = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ev_row_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__alloc_req_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__subtype_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__msg_type_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__status_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cdl_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__src_mac_r = 0ULL;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__target_eid_r = 0ULL;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__ctlr_eid_r = 0ULL;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__seq_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__opcode_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_type_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_index_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__tuid_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__luid_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__u_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cr_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__abort_pend_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_own_r = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mcast_r = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_maap_r = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_msrp_r = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mvrp_r = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__et_hi_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__slot_held_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cdl_known_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cp_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_protocol_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_msg_type_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_status_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_cdl_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_src_mac_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_target_eid_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_seq_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_opcode_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_u_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_cr_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_operands_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_rx_slot_r = 7U;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__en_q_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__good_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__wv_idx_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r = 0U;
        VL_ASSIGN_W(320, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r, Vmilan_datapath__ConstPool__CONST_hab76c978_0);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rank_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__mfs_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__mfs_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__mfs_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__mif_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__mif_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__mif_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__prio_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_join_fsm_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_la_msrp_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lat_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lat_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lat_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lat_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lat_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r = 0U;
    }
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
    vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_next_w 
        = ((0x0000fffeU & ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r) 
                           << 1U)) | (1U & VL_REDXOR_16(
                                                        (0xd008U 
                                                         & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r)))));
    vlSelfRef.milan_datapath__DOT__csr__DOT__shadow_q 
        = vlSelfRef.milan_datapath__DOT__csr__DOT__shadow_ram
        [(0x000001ffU & ((IData)(vlSelfRef.s_axi_araddr) 
                         >> 2U))];
    milan_datapath__DOT__csr_tctx_rd_addr_w = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_183)
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
    vlSelfRef.milan_datapath__DOT__csr_lctx_rd_addr_w 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_205)
            ? ((0x000000e0U & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_idx_r) 
                               << 5U)) | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_word_r))
            : (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_idx_r) 
                << 5U) | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_word_r)));
    vlSelfRef.milan_datapath__DOT__csr__DOT__rd_pend 
        = ((IData)(vlSelfRef.axis_resetn) && ((IData)(vlSelfRef.s_axi_arready) 
                                              & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_is_slow_w))));
    vlSelfRef.__VdfgBinToOneHot_Tab_hbfebb86c_0_0[vlSelfRef.__VdfgBinToOneHot_Pre_hbfebb86c_0_0] = 0U;
    vlSelfRef.__VdfgBinToOneHot_Tab_hbfebb86c_0_0[vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__op_region_r] = 1U;
    vlSelfRef.__VdfgBinToOneHot_Pre_hbfebb86c_0_0 = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__op_region_r;
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
                & (0x25U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((IData)(0x0000007aU) 
                              + ((IData)(0x0000001cU) 
                                 * (0x0003ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r) 
                                                   - (IData)(0x00000020U))))));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w = 0x001cU;
    } else if (((0x30U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0x35U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((IData)(0x00000106U) 
                              + (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r) 
                                  - (IData)(0x00000030U)) 
                                 << 4U)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w = 0x0010U;
    } else if (((0x40U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0x45U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((IData)(0x00000156U) 
                              + (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r) 
                                  - (IData)(0x00000040U)) 
                                 << 4U)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w = 0x0010U;
    } else if (((0x50U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0x55U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((IData)(0x000001a6U) 
                              + ((IData)(0x0000000cU) 
                                 * (0x0003ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r) 
                                                   - (IData)(0x00000050U))))));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w = 0x000cU;
    } else if (((0x60U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0x64U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((IData)(0x000001e2U) 
                              + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_pref_r
                              [(3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r))]));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w 
            = (0x00000fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_len_r
               [(3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r))]);
    } else if (((0x70U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0x74U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__b_mapo_w 
                              + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r
                              [(3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r))]));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w 
            = (0x00000fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r
               [(3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r))]);
    } else if (((0x80U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0xb3U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__b_mapo_w 
                               + (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r[3U] 
                                  + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r[3U])) 
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
    vlSelfRef.milan_datapath__DOT__pp_cd_acmp_declaring_w 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__declaring_r;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_q_r 
        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tctx_r
        [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w];
    vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i 
        = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_p_w)
            ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_idx_w)
            : 4U);
    vlSelfRef.milan_datapath__DOT__tkd_crf_p_w = ((~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_p_w)) 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__tkd_crf_pend_r));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_v_w = 0U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w = 0U;
    milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (3U & ((IData)(4U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__rr_r)));
    if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r
        [(3U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w 
            = (3U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (3U & ((IData)(3U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__rr_r)));
    if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r
        [(3U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w 
            = (3U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (3U & ((IData)(2U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__rr_r)));
    if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r
        [(3U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w 
            = (3U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (3U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__rr_r)));
    if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r
        [(3U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w 
            = (3U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_184 = (7U 
                                                  & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r
                                                     [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r] 
                                                     >> 1U));
    vlSelfRef.milan_datapath__DOT__csr__DOT__rds_valid_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_dir_r)
            ? (IData)(vlSelfRef.milan_datapath__DOT__tctx_rd_valid_w)
            : (IData)(vlSelfRef.milan_datapath__DOT__lctx_rd_valid_w));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__fmt_ok_w 
        = (((0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__fmt_r 
                                    >> 0x00000038U))) 
            == (0x000000ffU & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[4U] 
                               >> 0x0000000dU))) & 
           (((0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__fmt_r 
                                     >> 0x00000028U))) 
             == (0x000000ffU & ((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[3U] 
                                 << 6U) | (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[2U] 
                                           >> 0x0000001aU)))) 
            & (((0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__fmt_r 
                                        >> 0x00000030U))) 
                == (0x0000000fU & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[2U] 
                                   >> 0x00000016U))) 
               & ((~ ((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[1U] 
                       >> 0x0000000eU) | (0U == (0x000000ffU 
                                                 & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[2U] 
                                                    >> 0x0000000aU))))) 
                  & ((0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__fmt_r 
                                             >> 0x00000020U))) 
                     == (0x000000ffU & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[2U] 
                                        >> 2U)))))));
    vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_stat 
        = ((((0x0000ff00U & ((vlSelfRef.milan_datapath__DOT__avtprx_intr_c 
                              | (- (IData)((0x000000ffU 
                                            < vlSelfRef.milan_datapath__DOT__avtprx_intr_c)))) 
                             << 8U)) | (0x000000ffU 
                                        & (vlSelfRef.milan_datapath__DOT__avtprx_unlocked_c 
                                           | (- (IData)(
                                                        (0x000000ffU 
                                                         < vlSelfRef.milan_datapath__DOT__avtprx_unlocked_c)))))) 
            << 0x00000010U) | ((0x0000ff00U & ((vlSelfRef.milan_datapath__DOT__avtprx_locked_c 
                                                | (- (IData)(
                                                             (0x000000ffU 
                                                              < vlSelfRef.milan_datapath__DOT__avtprx_locked_c)))) 
                                               << 8U)) 
                               | (IData)(vlSelfRef.milan_datapath__DOT__avtprx_locked)));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r 
        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__lctx_r
        [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_raddr_w];
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 0x0fU;
    if ((0x00000800U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 0x0bU;
    }
    if ((0x00000400U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 0x0aU;
    }
    if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 9U;
    }
    if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 8U;
    }
    if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 7U;
    }
    if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 6U;
    }
    if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 5U;
    }
    if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 4U;
    }
    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 3U;
    }
    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 2U;
    }
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 1U;
    }
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 0U;
    }
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pdisp_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r)) 
           & (0U != (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r)));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w = 0U;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__depkt_any_w = 0U;
    if (((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[0U]) 
         | (0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[0U]))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__depkt_any_w = 1U;
    }
    if (((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[1U]) 
         | (0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[1U]))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__depkt_any_w = 1U;
    }
    if (((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[2U]) 
         | (0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[2U]))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__depkt_any_w = 1U;
    }
    if (((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[3U]) 
         | (0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[3U]))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__depkt_any_w = 1U;
    }
    vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
        = ((((0x000000f0U & ((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[3U] 
                              | (- (IData)((0x0fU < vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[3U])))) 
                             << 4U)) | (0x0000000fU 
                                        & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[2U] 
                                           | (- (IData)(
                                                        (0x0fU 
                                                         < vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[2U])))))) 
            << 8U) | ((0x000000f0U & ((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[1U] 
                                       | (- (IData)(
                                                    (0x0fU 
                                                     < vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[1U])))) 
                                      << 4U)) | (0x0000000fU 
                                                 & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[0U] 
                                                    | (- (IData)(
                                                                 (0x0fU 
                                                                  < vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[0U])))))));
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__overflow_reg = 0U;
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__good_frame_reg = 0U;
    if (vlSelfRef.s_axis_mac_rx_tvalid) {
        if (((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg) 
               == (0x0100U ^ (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__rd_ptr_reg))) 
              | ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg) 
                 == (0x0100U ^ (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_commit_reg)))) 
             | (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__drop_frame_reg))) {
            vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__drop_frame_reg = 1U;
            if (vlSelfRef.s_axis_mac_rx_tlast) {
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg 
                    = vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_commit_reg;
                vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__drop_frame_reg = 0U;
                vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__overflow_reg = 1U;
            }
        } else {
            __VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0[0U] 
                = vlSelfRef.__VdfgRegularize_h6e95ff9d_0_196[0U];
            __VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0[1U] 
                = vlSelfRef.__VdfgRegularize_h6e95ff9d_0_196[1U];
            __VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0[2U] 
                = ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__fw_user) 
                     | (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mark_frame_reg)) 
                    << 9U) | ((((IData)(vlSelfRef.s_axis_mac_rx_tlast) 
                                | (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mark_frame_reg)) 
                               << 8U) | vlSelfRef.__VdfgRegularize_h6e95ff9d_0_196[2U]));
            __VdlyDim0__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0 
                = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg));
            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg 
                = (0x000001ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg)));
            if (vlSelfRef.s_axis_mac_rx_tlast) {
                if (((IData)(vlSelfRef.s_axis_mac_rx_tlast) 
                     & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__fw_user))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg 
                        = vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_commit_reg;
                } else {
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_commit_reg 
                        = (0x000001ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg)));
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__good_frame_reg 
                        = vlSelfRef.s_axis_mac_rx_tlast;
                }
            }
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.axis_resetn)))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_fed_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_commit_reg = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__drop_frame_reg = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__overflow_reg = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__good_frame_reg = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mark_frame_reg = 0U;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_283 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_join_r) 
                                                  | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__join_pend_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__hw_full_q_r 
        = ((IData)(vlSelfRef.axis_resetn) && (0x0cU 
                                              == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_msrp_r)));
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_159 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__img_valid_r) 
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
                    if ((0x0033U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_names_r))) {
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
    } else if ((0x0033U < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_names_r))) {
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
        = ((0x0197U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_raddr_w))
            ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r
           [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_raddr_w]
            : 0ULL);
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_160 = ((0x0bU 
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_76 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__regun_r) 
                                                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__lockc_r));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_225 = (0x0000ffffU 
                                                  & (- (IData)(
                                                               (1U 
                                                                & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__scfg_r))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_223 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssfmt_r) 
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
                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_221))) 
               | (((0x0dU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r)) 
                   & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pending_r)) 
                      & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r) 
                         < (0x000007ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_len_r))))) 
                  | ((0x0aU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r)) 
                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_221))))))) {
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
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_drain_w 
        = (1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fill_w) 
                     >> 9U) | (0U == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_cnt_r)))));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__dup_sum_w 
        = (0x0001ffffU & (Vmilan_datapath__ConstPool__TABLE_h6dea4ce6_0
                          [(((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_cnt_w) 
                             << 4U) | ((((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r) 
                                         << 3U) | ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_primed_r) 
                                                   << 2U)) 
                                       | (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r) 
                                           << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_visit_w))))] 
                          + (IData)(vlSelfRef.milan_datapath__DOT__lb_dup_cnt_w)));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_act_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_visit_w) 
           & ((0U >= (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r)) 
              & (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_primed_r) 
                  >> (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r)) 
                 & (0U != (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_cnt_w)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_tk_reg_state_w 
        = ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_199) 
             << 8U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_200) 
                       << 6U)) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_201) 
                                   << 4U) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_202) 
                                              << 2U) 
                                             | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_84))));
    vlSelfRef.milan_datapath__DOT__lwsrp_ta_fail_code 
        = (0x000000ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r) 
                          & (- (IData)((2U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_84))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w 
        = ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_44) 
             << 8U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_45) 
                       << 6U)) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_46) 
                                   << 4U) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_47) 
                                              << 2U) 
                                             | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_decl))));
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
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_228));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__push_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_valid_r) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_229));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__push_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_valid_r) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_230));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_306 = (1U 
                                                  & (~ 
                                                     ((4U 
                                                       == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__cnt_r)) 
                                                      | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_231))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_vld_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_vld_r;
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_313 = (7U 
                                                  & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
                                                      >> 6U) 
                                                     - 
                                                     (1U 
                                                      & (- (IData)((IData)(__VdfgRegularize_h6e95ff9d_0_330))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_327 = (((IData)(__VdfgRegularize_h6e95ff9d_0_330) 
                                                   << 2U) 
                                                  | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_329));
    vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w = 0U;
    milan_datapath__DOT__tdm_lane_streams__DOT__rword 
        = (0x000000ffU & (milan_datapath__DOT__rmap_flat_w[0U] 
                          >> 0x00000010U));
    if ((IData)((0x80U == (0xc0U & (IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword))))) {
        if ((0U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((1U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((2U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((3U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
    }
    milan_datapath__DOT__tdm_lane_streams__DOT__rword 
        = (milan_datapath__DOT__rmap_flat_w[0U] >> 0x00000018U);
    if ((IData)((0x80U == (0xc0U & (IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword))))) {
        if ((0U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((1U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((2U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((3U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
    }
    milan_datapath__DOT__tdm_lane_streams__DOT__rword 
        = (0x000000ffU & milan_datapath__DOT__rmap_flat_w[1U]);
    if ((IData)((0x80U == (0xc0U & (IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword))))) {
        if ((0U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((1U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((2U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((3U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
    }
    milan_datapath__DOT__tdm_lane_streams__DOT__rword 
        = (0x000000ffU & (milan_datapath__DOT__rmap_flat_w[1U] 
                          >> 8U));
    if ((IData)((0x80U == (0xc0U & (IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword))))) {
        if ((0U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((1U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((2U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((3U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
    }
    milan_datapath__DOT__tdm_lane_streams__DOT__rword 
        = (0x000000ffU & (milan_datapath__DOT__rmap_flat_w[1U] 
                          >> 0x00000010U));
    if ((IData)((0x80U == (0xc0U & (IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword))))) {
        if ((0U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((1U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((2U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((3U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
    }
    milan_datapath__DOT__tdm_lane_streams__DOT__rword 
        = (milan_datapath__DOT__rmap_flat_w[1U] >> 0x00000018U);
    if ((IData)((0x80U == (0xc0U & (IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword))))) {
        if ((0U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((1U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((2U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((3U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
    }
    milan_datapath__DOT__tdm_lane_streams__DOT__rword 
        = (0x000000ffU & milan_datapath__DOT__rmap_flat_w[2U]);
    if ((IData)((0x80U == (0xc0U & (IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword))))) {
        if ((0U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((1U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((2U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((3U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
    }
    milan_datapath__DOT__tdm_lane_streams__DOT__rword 
        = (0x000000ffU & (milan_datapath__DOT__rmap_flat_w[2U] 
                          >> 8U));
    if ((IData)((0x80U == (0xc0U & (IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword))))) {
        if ((0U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((1U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((2U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
        if ((3U == (7U & ((IData)(milan_datapath__DOT__tdm_lane_streams__DOT__rword) 
                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__tdmr_lane_streams_w));
        }
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_195 = (0x0000ffffffffffffULL 
                                                  & ((4U 
                                                      & (IData)(__VdfgRegularize_h6e95ff9d_0_89))
                                                      ? 
                                                     (((1U 
                                                        & (IData)(__VdfgRegularize_h6e95ff9d_0_89))
                                                        ? 
                                                       (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r
                                                        [__VdfgRegularize_h6e95ff9d_0_203] 
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
                                                                              & ((1U 
                                                                                > (IData)(__VdfgRegularize_h6e95ff9d_0_198)) 
                                                                                & (0U 
                                                                                >= (IData)(__VdfgRegularize_h6e95ff9d_0_203))))))))
                                                        : 
                                                       (((QData)((IData)(vlSelfRef.milan_datapath__DOT__tone_smp_media)) 
                                                         << 0x00000018U) 
                                                        | (QData)((IData)(vlSelfRef.milan_datapath__DOT__tone_smp_media)))) 
                                                      & (- (QData)((IData)(
                                                                           (1U 
                                                                            & (~ 
                                                                               ((IData)(__VdfgRegularize_h6e95ff9d_0_89) 
                                                                                >> 1U)))))))
                                                      : 
                                                     ((2U 
                                                       & (IData)(__VdfgRegularize_h6e95ff9d_0_89))
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
                                                                            ((~ (IData)(__VdfgRegularize_h6e95ff9d_0_89)) 
                                                                             & (4U 
                                                                                > (IData)(__VdfgRegularize_h6e95ff9d_0_198)))))))
                                                       : 
                                                      (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__i2s_hold_r 
                                                       & (- (QData)((IData)(
                                                                            (1U 
                                                                             & (IData)(__VdfgRegularize_h6e95ff9d_0_89)))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_194 = (0x0000ffffffffffffULL 
                                                  & ((4U 
                                                      & (IData)(__VdfgRegularize_h6e95ff9d_0_90))
                                                      ? 
                                                     (((1U 
                                                        & (IData)(__VdfgRegularize_h6e95ff9d_0_90))
                                                        ? 
                                                       (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r
                                                        [__VdfgRegularize_h6e95ff9d_0_204] 
                                                        & (- (QData)((IData)(
                                                                             ((1U 
                                                                               > 
                                                                               (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                                                                [
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                                                << 1U)] 
                                                                                >> 4U))) 
                                                                              & ((1U 
                                                                                > (IData)(__VdfgRegularize_h6e95ff9d_0_197)) 
                                                                                & (0U 
                                                                                >= (IData)(__VdfgRegularize_h6e95ff9d_0_204))))))))
                                                        : 
                                                       (((QData)((IData)(vlSelfRef.milan_datapath__DOT__tone_smp_media)) 
                                                         << 0x00000018U) 
                                                        | (QData)((IData)(vlSelfRef.milan_datapath__DOT__tone_smp_media)))) 
                                                      & (- (QData)((IData)(
                                                                           (1U 
                                                                            & (~ 
                                                                               ((IData)(__VdfgRegularize_h6e95ff9d_0_90) 
                                                                                >> 1U)))))))
                                                      : 
                                                     ((2U 
                                                       & (IData)(__VdfgRegularize_h6e95ff9d_0_90))
                                                       ? 
                                                      (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r
                                                       [
                                                       (3U 
                                                        & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                                        [
                                                        ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                         << 1U)])] 
                                                       & (- (QData)((IData)(
                                                                            ((~ (IData)(__VdfgRegularize_h6e95ff9d_0_90)) 
                                                                             & (4U 
                                                                                > (IData)(__VdfgRegularize_h6e95ff9d_0_197)))))))
                                                       : 
                                                      (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__i2s_hold_r 
                                                       & (- (QData)((IData)(
                                                                            (1U 
                                                                             & (IData)(__VdfgRegularize_h6e95ff9d_0_90)))))))));
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
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__tctx_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tctx_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__tctx_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__tctx_r__v0;
    }
    vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_p_i 
        = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_p_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__tkd_crf_p_w));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w 
        = (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_183) 
            | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_busy_r) 
               & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_dir_r))) 
           & ((3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)) 
              | ((~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_v_w)) 
                 & (0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_192 = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                  == 
                                                  (0x0000001fU 
                                                   & ((IData)(5U) 
                                                      + 
                                                      ((IData)(6U) 
                                                       * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_184)))));
    vlSelfRef.milan_datapath__DOT__csr__DOT__rds_done_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_busy_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_valid_w) 
              & (0U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_cyc_r))));
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__lctx_r__v0) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__lctx_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__lctx_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__lctx_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w = 0U;
    if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w = 1U;
        if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__237__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__237__Vfuncout 
                = (8U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__237__s) 
                         << 5U));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__237__Vfuncout;
        } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__238__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__238__Vfuncout 
                = (9U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__238__s) 
                         << 5U));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__238__Vfuncout;
        } else {
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__239__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__239__Vfuncout 
                = (0x0aU | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__239__s) 
                            << 5U));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__239__Vfuncout;
        }
    } else if ((5U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
        if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__w11_mode_r) {
            if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r) {
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w = 1U;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__240__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__240__Vfuncout 
                    = (0x0bU | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__240__s) 
                                << 5U));
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__240__Vfuncout;
            }
        } else if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_mode_r) {
            if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w = 1U;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__241__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__241__Vfuncout 
                    = (0x11U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__241__s) 
                                << 5U));
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__241__Vfuncout;
            } else if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w = 1U;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__242__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__242__Vfuncout 
                    = (8U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__242__s) 
                             << 5U));
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__242__Vfuncout;
            }
        } else if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_zero_r) {
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w = 1U;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__243__w 
                = (0x10U | (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__zero_idx_r));
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__243__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__243__Vfuncout 
                = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__243__s) 
                    << 5U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__243__w));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__243__Vfuncout;
        } else if (((0U != (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r)) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r))) {
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w = 1U;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__244__w 
                = (0x10U | (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w));
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__244__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__244__Vfuncout 
                = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__244__s) 
                    << 5U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__244__w));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__244__Vfuncout;
        }
    } else if ((7U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r) 
                      >> 3U)))) {
            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r) 
                              >> 1U)))) {
                    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r)))) {
                        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w = 1U;
                        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__245__s 
                            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__245__Vfuncout 
                            = (3U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__245__s) 
                                     << 5U));
                        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                            = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__245__Vfuncout;
                    }
                }
            } else {
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w = 1U;
                if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__246__s 
                            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__246__Vfuncout 
                            = (2U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__246__s) 
                                     << 5U));
                        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                            = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__246__Vfuncout;
                    } else {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__247__s 
                            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__247__Vfuncout 
                            = (1U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__247__s) 
                                     << 5U));
                        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                            = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__247__Vfuncout;
                    }
                } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__248__s 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__248__Vfuncout 
                        = ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__248__s) 
                           << 5U);
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__248__Vfuncout;
                } else {
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__249__s 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__249__Vfuncout 
                        = (8U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__249__s) 
                                 << 5U));
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__249__Vfuncout;
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ms_div_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ms_div_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_div_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_div_r;
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__rd_ptr_reg 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__rd_ptr_reg;
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem[__VdlyDim0__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0][0U] 
            = __VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0[0U];
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem[__VdlyDim0__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0][1U] 
            = __VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0[1U];
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem[__VdlyDim0__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0][2U] 
            = __VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0[2U];
    }
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v0[0U];
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v0[1U];
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v0[2U];
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v1) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[0U][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v1[0U];
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[0U][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v1[1U];
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[0U][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v1[2U];
    }
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r;
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r;
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r;
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r__v0;
    }
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37 = ((5U 
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_224 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsfmt_r) 
                                                  | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_223));
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
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_space_w 
        = (7U & (((IData)(4U) - (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_cnt_r)) 
                 + (1U & (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_drain_w))))));
    vlSelfRef.milan_datapath__DOT__render_recentre_p_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__gm_recentre_p_r) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_adj_p) 
              | ((IData)(vlSelfRef.milan_datapath__DOT__src_recentre_p_r) 
                 | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_load_p))));
    vlSelfRef.milan_datapath__DOT__gm_recentre_q_r = 0ULL;
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wptr_bin_n 
        = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wptr_bin_r) 
                          + ((~ (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wfull_w)) 
                             & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wen_r))));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__push_same_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__push_ram_w) 
           & (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r) 
               == vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_addr_r
               [vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_rp_r]) 
              & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_act_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_snk_fail_code_w 
        = (((QData)((IData)((0x000000ffU & ((IData)(
                                                    (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r 
                                                     >> 0x00000020U)) 
                                            & (- (IData)(
                                                         (2U 
                                                          == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_199)))))))) 
            << 0x00000020U) | (QData)((IData)(((((0x0000ff00U 
                                                  & (((IData)(
                                                              (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r 
                                                               >> 0x00000018U)) 
                                                      & (- (IData)(
                                                                   (2U 
                                                                    == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_200))))) 
                                                     << 8U)) 
                                                 | (0x000000ffU 
                                                    & ((IData)(
                                                               (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r 
                                                                >> 0x00000010U)) 
                                                       & (- (IData)(
                                                                    (2U 
                                                                     == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_201))))))) 
                                                << 0x00000010U) 
                                               | ((0x0000ff00U 
                                                   & (((IData)(
                                                               (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r 
                                                                >> 8U)) 
                                                       & (- (IData)(
                                                                    (2U 
                                                                     == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_202))))) 
                                                      << 8U)) 
                                                  | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_ta_fail_code))))));
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
    if (((3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w) 
                >> 4U)) != (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_q_r) 
                                  >> 4U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_lsn_w 
            = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_lsn_w));
    }
    if (((3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w) 
                >> 6U)) != (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_q_r) 
                                  >> 6U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_lsn_w 
            = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_lsn_w));
    }
    if (((3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w) 
                >> 8U)) != (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_q_r) 
                                  >> 8U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_lsn_w 
            = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_lsn_w));
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
            if ((1U & (~ ((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r)) 
                          && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r) 
                                    >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r))))))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_dom_ok_w) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__st_set_w = 1U;
                }
            }
            if (((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r)) 
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
            if ((((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r)) 
                  && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r) 
                            >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r)))) 
                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_ifx_r) 
                    == (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_q_r 
                                               >> 0x00000020U)))))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__st_clr_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ev_dep_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_cancel_w = 1U;
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_q_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__push_w 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_306) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_valid_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nrm_txn_ready_w 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_230) 
           | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_229) 
              | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_306) 
                 | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_228))));
    vlSelfRef.o_phy_reset_n = (1U & vlSelfRef.milan_datapath__DOT__csr__DOT__phy_rst);
    vlSelfRef.o_mac_reinit = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__guard_rst_r) 
                                    | (vlSelfRef.milan_datapath__DOT__csr__DOT__link_ctrl 
                                       >> 1U)));
    vlSelfRef.milan_datapath__DOT__link_guard__DOT__rx_trans_w 
        = (1U & ((~ (vlSelfRef.milan_datapath__DOT__csr__DOT__link_ctrl 
                     >> 3U)) & VL_REDXOR_32((3U & ((IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__rx_sync_r) 
                                                   >> 1U)))));
    vlSelfRef.milan_datapath__DOT__link_guard__DOT__tx_trans_w 
        = (1U & ((~ (vlSelfRef.milan_datapath__DOT__csr__DOT__link_ctrl 
                     >> 3U)) & VL_REDXOR_32((3U & ((IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__tx_sync_r) 
                                                   >> 1U)))));
    vlSelfRef.milan_datapath__DOT__mnco_servo_en_w 
        = vlSelfRef.milan_datapath__DOT__crf_clk_selected_r;
    vlSelfRef.milan_datapath__DOT__media_nco__DOT__trim_sel_w 
        = ((- VL_SHIFTRS_III(32,32,32, VL_MULS_III(32, (IData)(0x00000064U), 
                                                   VL_EXTENDS_II(32,16, (IData)(vlSelfRef.milan_datapath__DOT__mnco_servo_trim_w))), 4U)) 
           & (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__crf_clk_selected_r))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_328 = ((0U 
                                                   != 
                                                   (7U 
                                                    & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
                                                       >> 9U))) 
                                                  & (0U 
                                                     == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_327)));
    vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_capture__map_rd_en_i 
        = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_side_r) 
           & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_busy_r));
    vlSelfRef.milan_datapath__DOT__rmap_rd_data_w = 0U;
    if ((0U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r)))) {
        vlSelfRef.milan_datapath__DOT__rmap_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[0U];
    }
    if ((1U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r)))) {
        vlSelfRef.milan_datapath__DOT__rmap_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[1U];
    }
    if ((2U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r)))) {
        vlSelfRef.milan_datapath__DOT__rmap_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[2U];
    }
    if ((3U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r)))) {
        vlSelfRef.milan_datapath__DOT__rmap_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[3U];
    }
    if ((4U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r)))) {
        vlSelfRef.milan_datapath__DOT__rmap_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[4U];
    }
    if ((5U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r)))) {
        vlSelfRef.milan_datapath__DOT__rmap_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[5U];
    }
    if ((6U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r)))) {
        vlSelfRef.milan_datapath__DOT__rmap_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[6U];
    }
    if ((7U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r)))) {
        vlSelfRef.milan_datapath__DOT__rmap_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[7U];
    }
    if ((8U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r)))) {
        vlSelfRef.milan_datapath__DOT__rmap_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[8U];
    }
    if ((9U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r)))) {
        vlSelfRef.milan_datapath__DOT__rmap_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[9U];
    }
    vlSelfRef.s_axi_arready = ((~ ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__r_valid) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_pend) 
                                      | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_pend2) 
                                         | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__sweep_busy) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_busy_r)))))) 
                               & (IData)(vlSelfRef.s_axi_arvalid));
    vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_rd_w 
        = ((0x0938U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
           | (0x093cU == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)));
    vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w = 0U;
    if (((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_p_i) 
         & (5U > (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i)))) {
        if ((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i)))) {
            vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w 
                = ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w) 
                   | (0x1fU & ((IData)(1U) << (7U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i)))));
        }
    }
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__308__t 
        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__308__Vfuncout 
        = (3U | ((IData)(__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__308__t) 
                 << 4U));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
        = __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__308__Vfuncout;
    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
            if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w) {
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                    = (0x0000003fU & (IData)(milan_datapath__DOT__csr_tctx_rd_addr_w));
            } else {
                vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__309__w 
                    = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w))
                        ? 3U : 0U);
                vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__309__t 
                    = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w;
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                    = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__309__t) 
                        << 4U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__309__w));
            }
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr;
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__310__t 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__310__Vfuncout 
                = (5U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__310__t) 
                         << 4U));
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__310__Vfuncout;
        } else {
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__311__t 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__311__Vfuncout 
                = (5U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__311__t) 
                         << 4U));
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__311__Vfuncout;
        }
    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
            if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w) {
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                    = (0x0000003fU & (IData)(milan_datapath__DOT__csr_tctx_rd_addr_w));
            } else {
                vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__312__w 
                    = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w))
                        ? 3U : 0U);
                vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__312__t 
                    = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w;
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                    = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__312__t) 
                        << 4U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__312__w));
            }
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr;
        } else {
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__313__w 
                = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))
                    ? 4U : 3U);
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__313__t 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__313__Vfuncout 
                = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__313__t) 
                    << 4U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__313__w));
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__313__Vfuncout;
        }
    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__314__w 
            = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))
                ? 1U : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))
                         ? 2U : 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__314__t 
            = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__314__Vfuncout 
            = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__314__t) 
                << 4U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__314__w));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__314__Vfuncout;
    } else {
        if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w) {
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                = (0x0000003fU & (IData)(milan_datapath__DOT__csr_tctx_rd_addr_w));
        } else {
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__315__w 
                = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w))
                    ? 3U : 0U);
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__315__t 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w;
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__315__t) 
                    << 4U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__315__w));
        }
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
            = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr;
    }
    vlSelfRef.milan_datapath__DOT__aaf_tx_tlast = (
                                                   (3U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)) 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_192));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__lost_w 
        = (0x000000ffU & (((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[4U] 
                            << 0x0000001bU) | (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[4U] 
                                               >> 5U)) 
                          - ((IData)(1U) + vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r)));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__seq_mm_w 
        = (IData)(((0x00001000U == (0x00001f00U & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r)) 
                   & ((0x000000ffU & ((IData)(1U) + vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r)) 
                      != (0x000000ffU & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[4U] 
                                         >> 5U)))));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w 
        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w 
        = (0x00800000U | ((0xff003fffU & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w) 
                          | (((0x00000100U & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[4U] 
                                              << 6U)) 
                              | (0x000000ffU & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[2U] 
                                                >> 0x0000000aU))) 
                             << 0x0000000eU)));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w 
        = ((0xffffff00U & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w) 
           | (0x000000ffU & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[4U] 
                             >> 5U)));
    __Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__ms_locked__234__w 
        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r;
    milan_datapath__DOT__avtp_rx_monitor__DOT____VlemCall_6__ms_locked 
        = (1U & (__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__ms_locked__234__w 
                 >> 0x0cU));
    if (milan_datapath__DOT__avtp_rx_monitor__DOT____VlemCall_6__ms_locked) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__ms_settle__235__w 
            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT____VlemCall_7__ms_settle 
            = (0x0000000fU & (vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__ms_settle__235__w 
                              >> 8U));
        if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT____VlemCall_7__ms_settle))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__ms_settle__236__w 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r;
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT____VlemCall_8__ms_settle 
                = (0x0000000fU & (vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__ms_settle__236__w 
                                  >> 8U));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w 
                = ((0xfffff0ffU & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w) 
                   | (0x00000f00U & (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT____VlemCall_8__ms_settle) 
                                      - (IData)(1U)) 
                                     << 8U)));
        }
    } else {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w 
            = (0x00001800U | (0xffffe0ffU & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w));
    }
    vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_capture__lb_flush_i 
        = (1U & (IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w));
    vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_pcmrx_cnt 
        = (((IData)(vlSelfRef.milan_datapath__DOT__pcmrx_drops) 
            << 0x00000010U) | (IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdus));
    if ((0U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                ? 6U : 2U))) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r));
    } else {
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__j 
            = (7U & (- ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                         ? 6U : 2U)));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__w 
            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__Vfuncout 
            = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__w 
                                      >> (0x0000003fU 
                                          & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__j) 
                                             << 3U)))));
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__Vfuncout;
    }
    vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w 
        = ((0xffffffffffffff00ULL & vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w) 
           | (IData)((IData)(((0U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r))
                               ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b)
                               : 0U))));
    if ((1U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                ? 6U : 2U))) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r 
                                      >> 8U)));
    } else {
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__j 
            = (7U & ((IData)(1U) - ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                                     ? 6U : 2U)));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__w 
            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__Vfuncout 
            = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__w 
                                      >> (0x0000003fU 
                                          & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__j) 
                                             << 3U)))));
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__Vfuncout;
    }
    vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w 
        = ((0xffffffffffff00ffULL & vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w) 
           | ((QData)((IData)(((1U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r))
                                ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b)
                                : 0U))) << 8U));
    if ((2U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                ? 6U : 2U))) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r 
                                      >> 0x10U)));
    } else {
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__j 
            = (7U & ((IData)(2U) - ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                                     ? 6U : 2U)));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__w 
            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__Vfuncout 
            = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__w 
                                      >> (0x0000003fU 
                                          & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__j) 
                                             << 3U)))));
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__Vfuncout;
    }
    vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w 
        = ((0xffffffffff00ffffULL & vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w) 
           | ((QData)((IData)(((2U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r))
                                ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b)
                                : 0U))) << 0x00000010U));
    if ((3U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                ? 6U : 2U))) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r 
                                      >> 0x18U)));
    } else {
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__j 
            = (7U & ((IData)(3U) - ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                                     ? 6U : 2U)));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__w 
            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__Vfuncout 
            = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__w 
                                      >> (0x0000003fU 
                                          & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__j) 
                                             << 3U)))));
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__Vfuncout;
    }
    vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w 
        = ((0xffffffff00ffffffULL & vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w) 
           | ((QData)((IData)(((3U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r))
                                ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b)
                                : 0U))) << 0x00000018U));
    if ((4U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                ? 6U : 2U))) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r 
                                      >> 0x20U)));
    } else {
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__j 
            = (7U & ((IData)(4U) - ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                                     ? 6U : 2U)));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__w 
            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__Vfuncout 
            = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__w 
                                      >> (0x0000003fU 
                                          & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__j) 
                                             << 3U)))));
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__Vfuncout;
    }
    vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w 
        = ((0xffffff00ffffffffULL & vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w) 
           | ((QData)((IData)(((4U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r))
                                ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b)
                                : 0U))) << 0x00000020U));
    if ((5U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                ? 6U : 2U))) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r 
                                      >> 0x28U)));
    } else {
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__j 
            = (7U & ((IData)(5U) - ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                                     ? 6U : 2U)));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__w 
            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__Vfuncout 
            = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__w 
                                      >> (0x0000003fU 
                                          & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__j) 
                                             << 3U)))));
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__Vfuncout;
    }
    vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w 
        = ((0xffff00ffffffffffULL & vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w) 
           | ((QData)((IData)(((5U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r))
                                ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b)
                                : 0U))) << 0x00000028U));
    if ((6U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                ? 6U : 2U))) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r 
                                      >> 0x30U)));
    } else {
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__j 
            = (7U & ((IData)(6U) - ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                                     ? 6U : 2U)));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__w 
            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__Vfuncout 
            = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__w 
                                      >> (0x0000003fU 
                                          & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__j) 
                                             << 3U)))));
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__Vfuncout;
    }
    vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w 
        = ((0xff00ffffffffffffULL & vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w) 
           | ((QData)((IData)(((6U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r))
                                ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b)
                                : 0U))) << 0x00000030U));
    vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__j 
        = (7U & ((IData)(7U) - ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                                 ? 6U : 2U)));
    vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__w 
        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
    vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__Vfuncout 
        = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__w 
                                  >> (0x0000003fU & 
                                      ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__j) 
                                       << 3U)))));
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
        = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__162__Vfuncout;
    vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w 
        = ((0x00ffffffffffffffULL & vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w) 
           | ((QData)((IData)(((7U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r))
                                ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b)
                                : 0U))) << 0x00000038U));
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_only_w 
        = ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r)) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r) 
              <= ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                   ? 6U : 2U)));
    vlSelfRef.milan_datapath__DOT__lb_tap_tuser_w = vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
        [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r];
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_337 = (vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                                                  [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r] 
                                                  << 5U);
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_in_w = 0U;
    if ((0U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
         [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r])) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_in_w 
            = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[0U];
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_338 = (vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                                                  [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r] 
                                                  << 4U);
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_in_w = 0U;
    if ((0U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
         [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r])) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_in_w 
            = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[0U];
    }
    if ((1U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
         [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r])) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_in_w 
            = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[1U];
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_in_w 
            = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[1U];
    }
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_in_raw_w = 0U;
    if ((0U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
         [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r])) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_in_raw_w 
            = (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w));
    }
    if ((1U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
         [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r])) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_in_raw_w 
            = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w) 
                              >> 4U));
    }
    if ((2U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
         [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r])) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_in_w 
            = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[2U];
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_in_w 
            = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[2U];
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_in_raw_w 
            = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w) 
                              >> 8U));
    }
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_in_w = 0U;
    if ((0U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
         [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r])) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_in_w 
            = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[0U];
    }
    if ((1U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
         [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r])) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_in_w 
            = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[1U];
    }
    if ((2U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
         [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r])) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_in_w 
            = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[2U];
    }
    if ((3U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
         [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r])) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_in_w 
            = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[3U];
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_in_w 
            = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[3U];
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_in_raw_w 
            = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w) 
                              >> 0x0cU));
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_in_w 
            = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[3U];
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__start0_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r)) 
           & ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_msrp_r)) 
              & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_283)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_275 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r) 
                                                  << 6U);
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_63 = (0x0000000fU 
                                                 & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                     >> 
                                                     ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r) 
                                                      << 2U)) 
                                                    & (- (IData)(
                                                                 (0x13U 
                                                                  >= 
                                                                  ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r) 
                                                                   << 2U))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r) 
                                                 << 4U);
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144 = (0x000000ffU 
                                                  & ((IData)(0x00000030U) 
                                                     * (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_145 = (0x0000003fU 
                                                  & ((IData)(0x0000000cU) 
                                                     * (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_146 = (0x0000000fU 
                                                  & ((IData)(3U) 
                                                     * (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_245 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r) 
                                                  << 5U);
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246 = (0x0000ffffU 
                                                  & (- (IData)(
                                                               (0x4fU 
                                                                >= 
                                                                ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r) 
                                                                 << 4U)))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_247 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r) 
                                                  << 6U);
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_48 = (0x0000000fU 
                                                 & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r 
                                                     >> 
                                                     ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r) 
                                                      << 2U)) 
                                                    & (- (IData)(
                                                                 (0x13U 
                                                                  >= 
                                                                  ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r) 
                                                                   << 2U))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_70 = ((1U 
                                                  == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r)) 
                                                 & (4U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_69 = ((1U 
                                                  == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r)) 
                                                 & (3U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68 = ((1U 
                                                  == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r)) 
                                                 & (2U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_67 = ((1U 
                                                  == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r)) 
                                                 & (1U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_66 = ((1U 
                                                  == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r)) 
                                                 & (0U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r)));
}
