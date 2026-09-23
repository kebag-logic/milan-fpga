// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

extern const VlWide<16>/*511:0*/ Vmilan_datapath__ConstPool__CONST_h88ed57bb_0;
extern const VlUnpacked<SData/*15:0*/, 8> Vmilan_datapath__ConstPool__TABLE_h42b7b3b2_0;
extern const VlWide<16>/*511:0*/ Vmilan_datapath__ConstPool__CONST_hfd3d218a_0;
extern const VlWide<12>/*383:0*/ Vmilan_datapath__ConstPool__CONST_h997e551f_0;
extern const VlUnpacked<CData/*0:0*/, 32> Vmilan_datapath__ConstPool__TABLE_h5f1389fb_0;
extern const VlUnpacked<CData/*2:0*/, 32> Vmilan_datapath__ConstPool__TABLE_h6dff1152_0;

void Vmilan_datapath___024root___nba_sequent__TOP__12(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___nba_sequent__TOP__12\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ milan_datapath__DOT__avtprx_stopped_w;
    milan_datapath__DOT__avtprx_stopped_w = 0;
    CData/*7:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_oversize_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_oversize_w = 0;
    SData/*8:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_rx_hit_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_rx_hit_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__drop_w;
    milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__drop_w = 0;
    CData/*0:0*/ milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_key;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_key = 0;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_key;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_key = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_20;
    __VdfgRegularize_h6e95ff9d_0_20 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_21;
    __VdfgRegularize_h6e95ff9d_0_21 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_22;
    __VdfgRegularize_h6e95ff9d_0_22 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_28;
    __VdfgRegularize_h6e95ff9d_0_28 = 0;
    CData/*7:0*/ __VdfgRegularize_h6e95ff9d_0_228;
    __VdfgRegularize_h6e95ff9d_0_228 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_276;
    __VdfgRegularize_h6e95ff9d_0_276 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_277;
    __VdfgRegularize_h6e95ff9d_0_277 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_366;
    __VdfgRegularize_h6e95ff9d_0_366 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_367;
    __VdfgRegularize_h6e95ff9d_0_367 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_368;
    __VdfgRegularize_h6e95ff9d_0_368 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_369;
    __VdfgRegularize_h6e95ff9d_0_369 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_370;
    __VdfgRegularize_h6e95ff9d_0_370 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_371;
    __VdfgRegularize_h6e95ff9d_0_371 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_372;
    __VdfgRegularize_h6e95ff9d_0_372 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_373;
    __VdfgRegularize_h6e95ff9d_0_373 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_374;
    __VdfgRegularize_h6e95ff9d_0_374 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_399;
    __VdfgRegularize_h6e95ff9d_0_399 = 0;
    IData/*31:0*/ __Vtemp_1;
    // Body
    if ((0x0aU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246))))) {
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
    if ((0x0bU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246))))) {
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
    if ((0x0cU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246))))) {
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
    if ((0x0dU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246))))) {
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
    if ((0x0eU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246))))) {
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
    if ((0x0fU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246))))) {
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
    if ((0x10U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246))))) {
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
    if ((0x11U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246))))) {
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
    if ((0x12U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246))))) {
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
    if ((0x13U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246))))) {
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
    if ((0x14U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246))))) {
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
    if ((0x15U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246))))) {
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
    if ((0x16U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246))))) {
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
    if ((0x17U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246))))) {
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
    vlSelfRef.milan_datapath__DOT__aaf_stream_en_raw_w 
        = ((((((((vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                  >> 1U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17) 
                            >> 7U)) & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_14)) 
               << 3U) | ((((vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                            >> 1U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17) 
                                      >> 6U)) & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_14)) 
                         << 2U)) | (((((vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                        >> 1U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17) 
                                                  >> 5U)) 
                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_14)) 
                                     << 1U) | (((vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                 >> 1U) 
                                                | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17) 
                                                   >> 4U)) 
                                               & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_14)))) 
            << 4U) | ((((((vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                           >> 1U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17) 
                                     >> 3U)) & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_14)) 
                        << 3U) | ((((vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                     >> 1U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17) 
                                               >> 2U)) 
                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_14)) 
                                  << 2U)) | ((0xfffffffeU 
                                              & ((vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                  | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17)) 
                                                 & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_14) 
                                                    << 1U))) 
                                             | (IData)(vlSelfRef.milan_datapath__DOT__aaf_gate))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ix26_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__tix_w) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__scfg_r) 
              | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_113)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__byte_ok_w 
        = (1U & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_133) 
                 | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r) 
                    | ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pay_w)) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_rd_valid_w)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_hold_w 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_213) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxf_fail_r)) 
              & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_288)));
    vlSelfRef.milan_datapath__DOT__pp_aecp_clk_src_index_w 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_r[0U];
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__iv_uf_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__iv_uf_r;
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__iv_sm_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__iv_sm_r;
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__iv_mr_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__iv_mr_r;
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__iv_tu_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__iv_tu_r;
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__iv_lt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__iv_lt_r;
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__iv_et_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__iv_et_r;
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__tout_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__tout_r;
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__settle_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__settle_r;
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__hfill_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__hfill_r;
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_bind_rise_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__en_q)) 
           & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__crf_rx__en_i));
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__have_seq_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__have_seq_r;
    vlSelfRef.milan_datapath__DOT__acmpl_stopped_v_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_aecp_strm_started_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r));
    vlSelfRef.milan_datapath__DOT__crf_locked_w = vlSelfRef.__Vdly__milan_datapath__DOT__crf_locked_w;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_adp_push_w 
        = ((8U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_adp_mid_w)) 
           & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_push_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txreq_valid_w) 
           & (8U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_mid_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_tx_eof_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_st_r))
            ? ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_valid_r) 
                         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_need_r)))) 
               && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_tx_eof_w))
            : ((1U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_st_r)) 
               && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_tx_eof_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reload_ok_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reload_w) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_pend_r) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_ok_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_tmo_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_maap_req_valid_w) 
           & (0x03ffU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__mreq_tmo_r)));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__out_vld_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__out_vld_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__rd_maddr_w 
        = (0x00000fffU & (((IData)(0x0240U) * (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rxslot_r))) 
                          + (0x000003ffU & ((8U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__f_idx_r))
                                             ? ((IData)(0x0014U) 
                                                + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__f_idx_r))
                                             : ((0x0aU 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__f_idx_r))
                                                 ? 
                                                ((IData)(0x0024U) 
                                                 + 
                                                 ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__f_idx_r) 
                                                  - (IData)(8U)))
                                                 : 
                                                ((0x0cU 
                                                  > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__f_idx_r))
                                                  ? 
                                                 ((IData)(0x0032U) 
                                                  + 
                                                  ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__f_idx_r) 
                                                   - (IData)(0x000aU)))
                                                  : 
                                                 ((0x14U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__f_idx_r))
                                                   ? 
                                                  ((IData)(4U) 
                                                   + 
                                                   ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__f_idx_r) 
                                                    - (IData)(0x000cU)))
                                                   : 
                                                  ((0x1aU 
                                                    > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__f_idx_r))
                                                    ? 
                                                   ((IData)(0x0028U) 
                                                    + 
                                                    ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__f_idx_r) 
                                                     - (IData)(0x0014U)))
                                                    : 
                                                   ((IData)(0x0034U) 
                                                    + 
                                                    ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__f_idx_r) 
                                                     - (IData)(0x001aU)))))))))));
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__mem_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__mem_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__mem_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxp_rd_en_w__BRA__1__KET__ 
        = ((7U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rxslot_r)) 
           & ((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__xs_r)) 
              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__f_idx_r) 
                 < ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__msg_x_r))
                     ? 0x1cU : 0x0cU))));
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0[0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0[1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0[2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0][3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0[3U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0][4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0[4U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0][5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0[5U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0][6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0[6U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0][7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0[7U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0][8U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0[8U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0][9U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0[9U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0][10U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0[10U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0][11U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0[11U];
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[0U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[0U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[1U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[1U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[2U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[2U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[3U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[3U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[4U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[4U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[5U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[5U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[6U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[6U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[7U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[7U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[8U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[8U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[9U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[9U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[10U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[10U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[11U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[11U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__wr_madr_w 
        = (0x00000fffU & (((IData)(0x00000240U) * (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_slot_w)) 
                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_addr_w)));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_oversize_w 
        = ((0x0240U < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__frame_len_r)) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_178));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__commit_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_commit_w) 
           & (1U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r
              [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_slot_w]));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__deadline_w 
        = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r 
           + ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_rgy_op_w) 
                >> 1U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_rgy_req_w))
               ? 0x0000ea60U : 0x000493e0U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_wdata_w 
        = (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__a_fmt_w);
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_223 = (0x00000001ffffffffULL 
                                                  & ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__a_fmt_w)) 
                                                     - (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__b_or_imm_w))));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_waddr_w 
        = (0x000003ffU & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_47)
                           ? (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_load_lane_r 
                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_ix_r))
                           : (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                              >> 3U)));
    __Vtemp_1 = VL_MATCHMASKED_I(13, (0x00001fffU & 
                                      (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                       >> 3U)), Vmilan_datapath__ConstPool__CONST_h88ed57bb_0);
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__in_range_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i) 
           < Vmilan_datapath__ConstPool__TABLE_h42b7b3b2_0
           [__Vtemp_1]);
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_da_w = 0ULL;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_close_w = 0U;
    if ((4U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
        if ((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_close_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_close_w;
        }
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_data_w = 0U;
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_117 = ((4U 
                                                   == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r)) 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__talker_cmd_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_valid_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_lsuid_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_lseid_w = 0ULL;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_status_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_flags_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_da_w = 0ULL;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_vlan_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_sid_w = 0ULL;
    if (((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r)) 
         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__talker_cmd_w))) {
        if ((0U == (0x0000000fU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[11U] 
                                    << 2U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[10U] 
                                              >> 0x0000001eU))))) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__uid_valid_w) {
                if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[12U] 
                                  >> 5U)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_valid_w = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_lsuid_w 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pdu_luid_r;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_lseid_w 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pdu_leid_r;
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__da_ok_w) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_status_w = 0U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_da_w 
                            = (0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[1U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[0U]))));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_vlan_w 
                            = (0x00000fffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__decl_vid_r));
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__106__s 
                            = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[1U] 
                               >> 0x0000001cU);
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__106__Vfuncout 
                            = ((0x023fU >= (0x000003ffU 
                                            & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__106__s) 
                                               << 6U)))
                                ? (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_src_sid_w
                                                    [
                                                    (((IData)(0x0000003fU) 
                                                      + 
                                                      (0x000003ffU 
                                                       & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__106__s) 
                                                          << 6U))) 
                                                     >> 5U)])) 
                                    << 0x00000020U) 
                                   | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_src_sid_w
                                                     [
                                                     (0x0000001eU 
                                                      & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__106__s) 
                                                         << 1U))])))
                                : 0ULL);
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_sid_w 
                            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__106__Vfuncout;
                    } else {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_status_w = 3U;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_flags_w 
                        = (0x000aU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pdu_flags_r));
                }
            } else {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_valid_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_lsuid_w 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pdu_luid_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_lseid_w 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pdu_leid_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_status_w = 2U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_flags_w 
                    = (0x000aU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pdu_flags_r));
            }
        } else {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_valid_w = 1U;
            if ((2U == (0x0000000fU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[11U] 
                                        << 2U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[10U] 
                                                  >> 0x0000001eU))))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_lsuid_w 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pdu_luid_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_lseid_w 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pdu_leid_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_status_w = 0U;
            } else {
                if ((4U != (0x0000000fU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[11U] 
                                            << 2U) 
                                           | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[10U] 
                                              >> 0x0000001eU))))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_lsuid_w 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pdu_luid_r;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_lseid_w 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pdu_leid_r;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_status_w 
                    = ((4U == (0x0000000fU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[11U] 
                                               << 2U) 
                                              | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[10U] 
                                                 >> 0x0000001eU))))
                        ? ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__uid_valid_w)
                            ? 0U : 2U) : 0x1fU);
            }
            if ((2U != (0x0000000fU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[11U] 
                                        << 2U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[10U] 
                                                  >> 0x0000001eU))))) {
                if ((4U == (0x0000000fU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[11U] 
                                            << 2U) 
                                           | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[10U] 
                                              >> 0x0000001eU))))) {
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__uid_valid_w) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_flags_w 
                            = (((0x11U >= (0x0000001eU 
                                           & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[1U] 
                                              >> 0x0000001bU))) 
                                & (1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w 
                                                >> 
                                                (0x0000001eU 
                                                 & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[1U] 
                                                    >> 0x0000001bU))))))
                                ? 0x0040U : 0U);
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_da_w 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__da_ok_w)
                                ? (0x0000ffffffffffffULL 
                                   & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[1U])) 
                                       << 0x00000020U) 
                                      | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[0U]))))
                                : 0ULL);
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_vlan_w 
                            = (0x00000fffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__decl_vid_r));
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__107__s 
                            = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[1U] 
                               >> 0x0000001cU);
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__107__Vfuncout 
                            = ((0x023fU >= (0x000003ffU 
                                            & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__107__s) 
                                               << 6U)))
                                ? (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_src_sid_w
                                                    [
                                                    (((IData)(0x0000003fU) 
                                                      + 
                                                      (0x000003ffU 
                                                       & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__107__s) 
                                                          << 6U))) 
                                                     >> 5U)])) 
                                    << 0x00000020U) 
                                   | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_src_sid_w
                                                     [
                                                     (0x0000001eU 
                                                      & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__107__s) 
                                                         << 1U))])))
                                : 0ULL);
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_sid_w 
                            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__107__Vfuncout;
                    }
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ping_w 
        = ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__talker_cmd_w) 
             & (0U == (0x0060U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[12U]))) 
            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__uid_valid_w)) 
           & (0U == (0x0000000fU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[11U] 
                                     << 2U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[10U] 
                                               >> 0x0000001eU)))));
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
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__dirty_r) 
                  >> 1U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_pick_w = 1U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__dirty_r) 
                  >> 2U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_pick_w = 2U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__dirty_r) 
                  >> 3U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_pick_w = 3U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__dirty_r) 
                  >> 4U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_pick_w = 4U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__dirty_r) 
                  >> 5U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_pick_w = 5U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__dirty_r) 
                  >> 6U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_pick_w = 6U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__dirty_r) 
                  >> 7U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_pick_w = 7U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w)) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__dirty_r) 
            >> 8U))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_pick_w = 8U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_retry_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_retry_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rp_k_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rp_k_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rcrc_rx_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rcrc_rx_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rplen_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rplen_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_valid_w = 0U;
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
                    = (0x01feU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r));
            }
            if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r) 
                          >> 1U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r 
                    = (0x01fdU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r));
            }
            if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r) 
                          >> 2U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r 
                    = (0x01fbU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r));
            }
            if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r) 
                          >> 3U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r 
                    = (0x01f7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r));
            }
            if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r) 
                          >> 4U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r 
                    = (0x01efU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r));
            }
            if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r) 
                          >> 5U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r 
                    = (0x01dfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r));
            }
            if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r) 
                          >> 6U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r 
                    = (0x01bfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r));
            }
            if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r) 
                          >> 7U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r 
                    = (0x017fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r));
            }
            if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r) 
                          >> 8U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r 
                    = (0x00ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r));
            }
        }
        if (((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_wr_gnt_w))) {
            if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r 
                    = (((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r))) 
                        & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r)) 
                       | (0x01ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rvld_q_r) 
                                     << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r))));
            }
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_complete_w) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rrec_ok_w))) 
             & (~ ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r)) 
                   && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r) 
                             >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r))))))) {
            if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_empty_w) 
             & (~ ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r)) 
                   && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r) 
                             >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r))))))) {
            if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r));
            }
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
            if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r 
                    = (((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r))) 
                        & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r)) 
                       | (0x01ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_vld_r) 
                                     << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r))));
            }
            if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__go_take_w) 
                 | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_402))) {
                if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r 
                        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r) 
                           | (0x01ffU & ((IData)(1U) 
                                         << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r))));
                }
            }
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__recwr_addr_w;
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
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__void_hard_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reload_ok_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rebase_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_rel_acmp_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_active_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_done_pending_r) 
              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_done_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
        = (0x01feU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (0U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U != (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
                    = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
        = (0x01fdU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 1U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (1U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 2U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
                    = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
        = (0x01fbU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 2U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (2U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 4U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
                    = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
        = (0x01f7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 3U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (3U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 6U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
                    = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
        = (0x01efU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 4U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (4U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 8U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
                    = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
        = (0x01dfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 5U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (5U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 0x0aU)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
                    = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
        = (0x01bfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 6U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (6U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 0x0cU)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
                    = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
        = (0x017fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 7U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (7U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 0x0eU)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
                    = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
        = (0x00ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
        = (0x01feU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (0U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r))) {
                if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
                        = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
        = (0x01fdU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 1U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (1U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 2U)))) {
                if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                            >> 1U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
                        = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
        = (0x01fbU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 2U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (2U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 4U)))) {
                if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                            >> 2U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
                        = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
        = (0x01f7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 3U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (3U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 6U)))) {
                if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                            >> 3U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
                        = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
        = (0x01efU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 4U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (4U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 8U)))) {
                if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                            >> 4U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
                        = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
        = (0x01dfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 5U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (5U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 0x0aU)))) {
                if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                            >> 5U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
                        = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
        = (0x01bfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 6U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (6U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 0x0cU)))) {
                if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                            >> 6U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
                        = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
        = (0x017fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 7U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (7U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 0x0eU)))) {
                if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                            >> 7U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
                        = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
        = (0x00ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w 
        = (0x01feU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w));
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (0U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r))) {
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
        = (0x01fdU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w));
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 1U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (1U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 2U)))) {
                if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                               >> 1U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w))))) {
                    if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                                >> 1U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w 
                            = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w));
                    }
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w 
        = (0x01fbU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w));
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 2U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (2U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 4U)))) {
                if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                               >> 2U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w))))) {
                    if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                                >> 2U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w 
                            = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w));
                    }
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w 
        = (0x01f7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w));
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 3U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (3U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 6U)))) {
                if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                               >> 3U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w))))) {
                    if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                                >> 3U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w 
                            = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w));
                    }
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w 
        = (0x01efU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w));
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 4U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (4U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 8U)))) {
                if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                               >> 4U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w))))) {
                    if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                                >> 4U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w 
                            = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w));
                    }
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w 
        = (0x01dfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w));
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 5U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (5U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 0x0aU)))) {
                if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                               >> 5U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w))))) {
                    if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                                >> 5U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w 
                            = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w));
                    }
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w 
        = (0x01bfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w));
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 6U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (6U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 0x0cU)))) {
                if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                               >> 6U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w))))) {
                    if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                                >> 6U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w 
                            = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w));
                    }
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w 
        = (0x017fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w));
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 7U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (7U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 0x0eU)))) {
                if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                               >> 7U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w))))) {
                    if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                                >> 7U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w 
                            = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w));
                    }
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w 
        = (0x00ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_grant_w = 0U;
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (0U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r))) {
                if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w))))) {
                    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                                  | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r))))) {
                        if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                             & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
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
                      & (1U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 2U)))) {
                if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                               >> 1U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w))))) {
                    if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                                   >> 1U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r))))) {
                        if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                             & (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_grant_w = 1U;
                        }
                    }
                }
            }
        }
    }
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 2U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (2U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 4U)))) {
                if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                               >> 2U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w))))) {
                    if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                                   >> 2U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r))))) {
                        if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                             & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_grant_w = 1U;
                        }
                    }
                }
            }
        }
    }
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 3U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (3U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 6U)))) {
                if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                               >> 3U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w))))) {
                    if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                                   >> 3U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r))))) {
                        if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                             & (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_grant_w = 1U;
                        }
                    }
                }
            }
        }
    }
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 4U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (4U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 8U)))) {
                if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                               >> 4U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w))))) {
                    if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                                   >> 4U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r))))) {
                        if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                             & (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_grant_w = 1U;
                        }
                    }
                }
            }
        }
    }
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 5U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (5U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 0x0aU)))) {
                if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                               >> 5U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w))))) {
                    if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                                   >> 5U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r))))) {
                        if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                             & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_grant_w = 1U;
                        }
                    }
                }
            }
        }
    }
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 6U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (6U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 0x0cU)))) {
                if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                               >> 6U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w))))) {
                    if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                                   >> 6U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r))))) {
                        if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                             & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_grant_w = 1U;
                        }
                    }
                }
            }
        }
    }
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 7U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (7U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 0x0eU)))) {
                if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                               >> 7U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w))))) {
                    if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                                   >> 7U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r))))) {
                        if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                             & (7U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_grant_w = 1U;
                        }
                    }
                }
            }
        }
    }
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 8U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (8U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 0x10U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
                    = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
            }
            if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                              >> 0x10U)))) {
                if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                              >> 8U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
                        = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
                }
                if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                               >> 8U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w))))) {
                    if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                                  >> 8U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w 
                            = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w));
                    }
                    if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                                   >> 8U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r))))) {
                        if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                             & (8U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_grant_w = 1U;
                        }
                    }
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
        = (0x01feU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                & (0U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = ((0x01feU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w)) 
               | (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r))));
    } else if ((0U != (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r))) {
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
                & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
        = (0x01fdU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                & (1U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = ((0x01fdU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w)) 
               | (2U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
                        << 1U)));
    } else if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                             >> 2U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                       >> 1U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                       >> 1U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                & (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
        = (0x01fbU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                & (2U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = ((0x01fbU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w)) 
               | (4U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
                        << 2U)));
    } else if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                             >> 4U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                       >> 2U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                       >> 2U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
        = (0x01f7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                & (3U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = ((0x01f7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w)) 
               | (8U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
                        << 3U)));
    } else if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                             >> 6U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                       >> 3U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                       >> 3U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                & (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
        = (0x01efU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                & (4U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = ((0x01efU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w)) 
               | (0x00000010U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
                                 << 4U)));
    } else if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                             >> 8U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                       >> 4U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                       >> 4U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                & (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
        = (0x01dfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                & (5U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = ((0x01dfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w)) 
               | (0x00000020U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
                                 << 5U)));
    } else if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                             >> 0x0aU)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                       >> 5U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                       >> 5U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
        = (0x01bfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                & (6U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = ((0x01bfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w)) 
               | (0x00000040U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
                                 << 6U)));
    } else if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                             >> 0x0cU)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                       >> 6U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                       >> 6U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
        = (0x017fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                & (7U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = ((0x017fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w)) 
               | (0x00000080U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
                                 << 7U)));
    } else if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                             >> 0x0eU)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                       >> 7U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                       >> 7U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                & (7U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
        = (0x00ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
        = (3ULL | (0x0000000ffffffff0ULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000ffffffff0ULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | (IData)((IData)((0x0000000fU & ((IData)(3U) 
                                                 + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))));
    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                & (0U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (2ULL | (0x0000000ffffffff0ULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if ((0U != (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000ffffffff0ULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | (IData)((IData)(((1U == (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r))
                                   ? 0U : 2U))));
    } else if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                      | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (9ULL | (0x0000000ffffffff0ULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                      | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x000000000000000aULL | (0x0000000ffffffff0ULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000ffffffff0ULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | (IData)((IData)(((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wtxla_r)
                                   ? 0x0cU : 0x0bU))));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
        = (0x0000000000000030ULL | (0x0000000fffffff0fULL 
                                    & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000fffffff0fULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)((0x0000000fU & ((IData)(3U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) 
                  << 4U));
    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                & (1U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x0000000000000020ULL | (0x0000000fffffff0fULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                             >> 2U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000fffffff0fULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)(((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                                                 >> 2U)))
                                    ? 0U : 2U))) << 4U));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                       >> 1U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x0000000000000090ULL | (0x0000000fffffff0fULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                       >> 1U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x00000000000000a0ULL | (0x0000000fffffff0fULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                & (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000fffffff0fULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)(((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wtxla_r)
                                    ? 0x0cU : 0x0bU))) 
                  << 4U));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
        = (0x0000000000000300ULL | (0x0000000ffffff0ffULL 
                                    & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000ffffff0ffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)((0x0000000fU & ((IData)(3U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) 
                  << 8U));
    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                & (2U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x0000000000000200ULL | (0x0000000ffffff0ffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                             >> 4U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000ffffff0ffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)(((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                                                 >> 4U)))
                                    ? 0U : 2U))) << 8U));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                       >> 2U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x0000000000000900ULL | (0x0000000ffffff0ffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                       >> 2U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x0000000000000a00ULL | (0x0000000ffffff0ffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000ffffff0ffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)(((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wtxla_r)
                                    ? 0x0cU : 0x0bU))) 
                  << 8U));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
        = (0x0000000000003000ULL | (0x0000000fffff0fffULL 
                                    & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000fffff0fffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)((0x0000000fU & ((IData)(3U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) 
                  << 0x0000000cU));
    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                & (3U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x0000000000002000ULL | (0x0000000fffff0fffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                             >> 6U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000fffff0fffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)(((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                                                 >> 6U)))
                                    ? 0U : 2U))) << 0x0000000cU));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                       >> 3U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x0000000000009000ULL | (0x0000000fffff0fffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                       >> 3U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x000000000000a000ULL | (0x0000000fffff0fffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                & (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000fffff0fffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)(((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wtxla_r)
                                    ? 0x0cU : 0x0bU))) 
                  << 0x0000000cU));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
        = (0x0000000000030000ULL | (0x0000000ffff0ffffULL 
                                    & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000ffff0ffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)((0x0000000fU & ((IData)(3U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) 
                  << 0x00000010U));
    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                & (4U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x0000000000020000ULL | (0x0000000ffff0ffffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                             >> 8U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000ffff0ffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)(((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                                                 >> 8U)))
                                    ? 0U : 2U))) << 0x00000010U));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                       >> 4U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x0000000000090000ULL | (0x0000000ffff0ffffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                       >> 4U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x00000000000a0000ULL | (0x0000000ffff0ffffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                & (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000ffff0ffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)(((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wtxla_r)
                                    ? 0x0cU : 0x0bU))) 
                  << 0x00000010U));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
        = (0x0000000000300000ULL | (0x0000000fff0fffffULL 
                                    & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000fff0fffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)((0x0000000fU & ((IData)(3U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) 
                  << 0x00000014U));
    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                & (5U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x0000000000200000ULL | (0x0000000fff0fffffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                             >> 0x0aU)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000fff0fffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)(((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                                                 >> 0x0aU)))
                                    ? 0U : 2U))) << 0x00000014U));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                       >> 5U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x0000000000900000ULL | (0x0000000fff0fffffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                       >> 5U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x0000000000a00000ULL | (0x0000000fff0fffffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000fff0fffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)(((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wtxla_r)
                                    ? 0x0cU : 0x0bU))) 
                  << 0x00000014U));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
        = (0x0000000003000000ULL | (0x0000000ff0ffffffULL 
                                    & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000ff0ffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)((0x0000000fU & ((IData)(3U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) 
                  << 0x00000018U));
    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                & (6U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x0000000002000000ULL | (0x0000000ff0ffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                             >> 0x0cU)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000ff0ffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)(((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                                                 >> 0x0cU)))
                                    ? 0U : 2U))) << 0x00000018U));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                       >> 6U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x0000000009000000ULL | (0x0000000ff0ffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                       >> 6U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x000000000a000000ULL | (0x0000000ff0ffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000ff0ffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)(((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wtxla_r)
                                    ? 0x0cU : 0x0bU))) 
                  << 0x00000018U));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
        = (0x0000000030000000ULL | (0x0000000f0fffffffULL 
                                    & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000f0fffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)((0x0000000fU & ((IData)(3U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) 
                  << 0x0000001cU));
    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                & (7U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x0000000020000000ULL | (0x0000000f0fffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                             >> 0x0eU)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000f0fffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)(((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                                                 >> 0x0eU)))
                                    ? 0U : 2U))) << 0x0000001cU));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                       >> 7U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x0000000090000000ULL | (0x0000000f0fffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                       >> 7U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x00000000a0000000ULL | (0x0000000f0fffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                & (7U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0000000f0fffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)(((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wtxla_r)
                                    ? 0x0cU : 0x0bU))) 
                  << 0x0000001cU));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
        = (0x0000000300000000ULL | (0x00000000ffffffffULL 
                                    & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x00000000ffffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)((0x0000000fU & ((IData)(3U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) 
                  << 0x00000020U));
    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                & (8U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = ((0x00ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w)) 
               | (0x00000100U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
                                 << 8U)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x0000000200000000ULL | (0x00000000ffffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if ((0U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                             >> 0x10U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x00000000ffffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)(((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r 
                                                 >> 0x10U)))
                                    ? 0U : 2U))) << 0x00000020U));
    } else if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                         >> 8U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x0000000900000000ULL | (0x00000000ffffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                         >> 8U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x0000000a00000000ULL | (0x00000000ffffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w));
    } else if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                & (8U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x00000000ffffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w) 
               | ((QData)((IData)(((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wtxla_r)
                                    ? 0x0cU : 0x0bU))) 
                  << 0x00000020U));
    }
    __VdfgRegularize_h6e95ff9d_0_366 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w) 
                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144));
    __VdfgRegularize_h6e95ff9d_0_367 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w) 
                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_145));
    __VdfgRegularize_h6e95ff9d_0_368 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w) 
                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_146));
    __VdfgRegularize_h6e95ff9d_0_369 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w) 
                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_147));
    __VdfgRegularize_h6e95ff9d_0_370 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w) 
                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_148));
    __VdfgRegularize_h6e95ff9d_0_371 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w) 
                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_149));
    __VdfgRegularize_h6e95ff9d_0_372 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w) 
                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_150));
    __VdfgRegularize_h6e95ff9d_0_373 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w) 
                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_151));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w 
        = ((((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144) 
               << 4U) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_145) 
                          << 3U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_146) 
                                    << 2U))) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_147) 
                                                 << 1U) 
                                                | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_148))) 
            << 4U) | ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_149) 
                        << 3U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_150) 
                                  << 2U)) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_151) 
                                              << 1U) 
                                             | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_152))));
    __VdfgRegularize_h6e95ff9d_0_374 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w) 
                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_152));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_36 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_350) 
                                                 & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_3) 
                                                    & ((5U 
                                                        >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                                       & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_205) 
                                                          & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_da_w 
                                                              == 
                                                              (0x0000ffffffffffffULL 
                                                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r[13U])) 
                                                                   << 0x00000020U) 
                                                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r[12U]))))) 
                                                             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_vid_w) 
                                                                == 
                                                                (0x00000fffU 
                                                                 & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vid_r[3U])))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_351) 
                                                 & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_3) 
                                                    & ((5U 
                                                        >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                                       & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_204) 
                                                          & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_da_w 
                                                              == 
                                                              (0x0000ffffffffffffULL 
                                                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r[11U])) 
                                                                   << 0x00000010U) 
                                                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r[10U])) 
                                                                     >> 0x00000010U)))) 
                                                             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_vid_w) 
                                                                == 
                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vid_r[2U] 
                                                                 >> 0x00000014U)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_352) 
                                                 & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_3) 
                                                    & ((5U 
                                                        >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                                       & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_203) 
                                                          & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_da_w 
                                                              == 
                                                              (0x0000ffffffffffffULL 
                                                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r[10U])) 
                                                                   << 0x00000020U) 
                                                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r[9U]))))) 
                                                             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_vid_w) 
                                                                == 
                                                                (0x00000fffU 
                                                                 & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vid_r[2U] 
                                                                    >> 8U))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_353) 
                                                 & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_3) 
                                                    & ((5U 
                                                        >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                                       & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_202) 
                                                          & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_da_w 
                                                              == 
                                                              (0x0000ffffffffffffULL 
                                                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r[8U])) 
                                                                   << 0x00000010U) 
                                                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r[7U])) 
                                                                     >> 0x00000010U)))) 
                                                             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_vid_w) 
                                                                == 
                                                                (0x00000fffU 
                                                                 & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vid_r[2U] 
                                                                     << 4U) 
                                                                    | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vid_r[1U] 
                                                                       >> 0x0000001cU)))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_40 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_354) 
                                                 & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_3) 
                                                    & ((5U 
                                                        >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                                       & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_201) 
                                                          & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_da_w 
                                                              == 
                                                              (0x0000ffffffffffffULL 
                                                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r[7U])) 
                                                                   << 0x00000020U) 
                                                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r[6U]))))) 
                                                             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_vid_w) 
                                                                == 
                                                                (0x00000fffU 
                                                                 & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vid_r[1U] 
                                                                    >> 0x00000010U))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_41 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_355) 
                                                 & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_3) 
                                                    & ((5U 
                                                        >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                                       & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_200) 
                                                          & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_da_w 
                                                              == 
                                                              (0x0000ffffffffffffULL 
                                                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r[5U])) 
                                                                   << 0x00000010U) 
                                                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r[4U])) 
                                                                     >> 0x00000010U)))) 
                                                             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_vid_w) 
                                                                == 
                                                                (0x00000fffU 
                                                                 & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vid_r[1U] 
                                                                    >> 4U))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_42 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_356) 
                                                 & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_3) 
                                                    & ((5U 
                                                        >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                                       & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_199) 
                                                          & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_da_w 
                                                              == 
                                                              (0x0000ffffffffffffULL 
                                                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r[4U])) 
                                                                   << 0x00000020U) 
                                                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r[3U]))))) 
                                                             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_vid_w) 
                                                                == 
                                                                (0x00000fffU 
                                                                 & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vid_r[1U] 
                                                                     << 8U) 
                                                                    | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vid_r[0U] 
                                                                       >> 0x00000018U)))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_43 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_357) 
                                                 & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_3) 
                                                    & ((5U 
                                                        >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                                       & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_198) 
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
                                                                 & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vid_r[0U] 
                                                                    >> 0x0000000cU))))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w 
        = (((((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_350) 
                & ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_205))) 
               << 4U) | ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_351) 
                           & ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                              & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_204))) 
                          << 3U) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_352) 
                                     & ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_203))) 
                                    << 2U))) | ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_353) 
                                                  & ((3U 
                                                      == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_202))) 
                                                 << 1U) 
                                                | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_354) 
                                                   & ((3U 
                                                       == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_201))))) 
            << 4U) | (((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_355) 
                         & ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                            & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_200))) 
                        << 3U) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_356) 
                                   & ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_199))) 
                                  << 2U)) | ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_357) 
                                               & ((3U 
                                                   == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_198))) 
                                              << 1U) 
                                             | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_358) 
                                                & ((3U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_197))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_92 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_358) 
                                                 & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_3) 
                                                    & ((5U 
                                                        >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                                       & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_197) 
                                                          & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_da_w 
                                                              == 
                                                              (0x0000ffffffffffffULL 
                                                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r[1U])) 
                                                                   << 0x00000020U) 
                                                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r[0U]))))) 
                                                             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_vid_w) 
                                                                == 
                                                                (0x00000fffU 
                                                                 & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vid_r[0U])))))));
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
        = ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_407)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__out_vld_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__fetch_r 
        = ((IData)(vlSelfRef.axis_resetn) && ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__avail_w) 
                                              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__space_w)));
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_229 = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[5U])) 
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_278 = (1U 
                                                  & ((~ 
                                                      (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[0U] 
                                                       >> 0x00000012U)) 
                                                     & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__trom_rdata_r 
                                                        >> 0x00000016U)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_230 = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__tk_eid_f_r 
                                                  == 
                                                  (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[2U])) 
                                                    << 0x00000020U) 
                                                   | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[1U]))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_231 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__tk_uid_f_r) 
                                                  == 
                                                  (0x0000ffffU 
                                                   & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[3U]));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__settled_w 
        = ((6U == (7U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[0U])) 
           | (7U == (7U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[0U])));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cmp_z_w 
        = ((3U == (7U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                 >> 0x0000001cU))))
            ? (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r 
               == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__b_or_imm_w)
            : (0U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_223)));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_we_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_waddr_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_initset_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[0U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[0U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[1U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[1U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[2U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_open_w = 0U;
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ping_w) {
        if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] 
                          >> 0x00000012U)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_initset_w = 1U;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[1U] 
            = ((0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[1U]) 
               | ((IData)((0x0000000100000000ULL | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r)))) 
                  << 0x00000010U));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[2U] 
            = ((0x000e0000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[2U]) 
               | (0x000fffffU & (((IData)((0x0000000100000000ULL 
                                           | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r)))) 
                                  >> 0x00000010U) | 
                                 ((IData)(((0x0000000100000000ULL 
                                            | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r))) 
                                           >> 0x00000020U)) 
                                  << 0x00000010U))));
        if ((IData)(((0x00040000U == (0x000c0000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U])) 
                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__da_ok_w)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[2U] 
                = (0x00080000U | (0x0003ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[2U]));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_open_w = 1U;
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_valid_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_cancel_w = 0U;
    if ((1U & (~ (((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r)) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ping_w)) 
                  & (3U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] 
                                  >> 0x00000012U))))))) {
        if ((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_arm_fresh_w)))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_cancel_w) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_cancel_w = 1U;
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_deadline_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_owner_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w = 0U;
    if ((((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r)) 
          & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ping_w)) 
         & (3U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] 
                         >> 0x00000012U))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_deadline_w 
            = ((IData)(0x00003a98U) + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_owner_w 
            = (0x000000ffU & ((IData)(0x50U) + (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[1U] 
                                                >> 0x0000001cU)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w 
            = (0x0000007fU & ((IData)(0x13U) + (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[1U] 
                                                >> 0x0000001cU)));
    } else if ((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_arm_fresh_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_valid_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_deadline_w 
                = ((IData)(0x00003a98U) + ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] 
                                            << 0x00000010U) 
                                           | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[1U] 
                                              >> 0x00000010U)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_owner_w 
                = (0x000000ffU & ((IData)(0x50U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w 
                = (0x0000007fU & ((IData)(0x13U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r)));
        } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_cancel_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_valid_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_owner_w 
                = (0x000000ffU & ((IData)(0x50U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w 
                = (0x0000007fU & ((IData)(0x13U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r)));
        }
    } else if ((9U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_deadline_w 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__arm_deadline_r;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_owner_w 
            = (0x000000ffU & ((IData)(0x50U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w 
            = (0x0000007fU & ((IData)(0x13U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r)));
    }
    __VdfgRegularize_h6e95ff9d_0_277 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_cancel_w) 
                                        | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_rsp_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_gnt_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__alloc_gnt_r) 
              & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_txs_gnt_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__alloc_gnt_r) 
              & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_381 = (0x000000ffU 
                                                  & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r
                                                  [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__sel_r]);
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_evt_tk_valid_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__valid_r) 
           & (0x13U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__sel_r)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_158 = (0x0000ffffffffffffULL 
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
    __VdfgRegularize_h6e95ff9d_0_228 = (0x000000ffU 
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
    if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_active_w) 
         | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_rd_req_w))) {
        if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rd_addr_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[0U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rd_addr_w][0U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[1U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rd_addr_w][1U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[2U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rd_addr_w][2U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[3U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rd_addr_w][3U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[4U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rd_addr_w][4U];
        } else {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[0U] = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[1U] = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[2U] = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[3U] = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[4U] = 0U;
        }
    }
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
    vlSelfRef.milan_datapath__DOT__avtprx_accept_p 
        = ((~ (IData)(milan_datapath__DOT__avtprx_stopped_w)) 
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
                    == ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r))
                         ? (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[17U])) 
                             << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[16U])))
                         : (((QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__crf_sidhi)) 
                             << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__crf_sidlo))))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__close_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_open_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__release_w) 
              | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_274) 
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
                       & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_274))))));
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
        = ((((((((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                               >> 0x00000010U))) | 
                 ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                  != (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r) 
                            >> 8U)))) & (IData)(__VdfgRegularize_h6e95ff9d_0_366)) 
               << 4U) | (((((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                                          >> 0x0000000eU))) 
                            | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                               != (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r) 
                                         >> 7U)))) 
                           & (IData)(__VdfgRegularize_h6e95ff9d_0_367)) 
                          << 3U) | ((((0U == (3U & 
                                              (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                                               >> 0x0000000cU))) 
                                      | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                                         != (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r) 
                                                   >> 6U)))) 
                                     & (IData)(__VdfgRegularize_h6e95ff9d_0_368)) 
                                    << 2U))) | ((((
                                                   (0U 
                                                    == 
                                                    (3U 
                                                     & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                                                        >> 0x0000000aU))) 
                                                   | ((2U 
                                                       == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                                                      != 
                                                      (1U 
                                                       & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r) 
                                                          >> 5U)))) 
                                                  & (IData)(__VdfgRegularize_h6e95ff9d_0_369)) 
                                                 << 1U) 
                                                | (((0U 
                                                     == 
                                                     (3U 
                                                      & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                                                         >> 8U))) 
                                                    | ((2U 
                                                        == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                                                       != 
                                                       (1U 
                                                        & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r) 
                                                           >> 4U)))) 
                                                   & (IData)(__VdfgRegularize_h6e95ff9d_0_370)))) 
            << 4U) | ((((((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                                        >> 6U))) | 
                          ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                           != (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r) 
                                     >> 3U)))) & (IData)(__VdfgRegularize_h6e95ff9d_0_371)) 
                        << 3U) | ((((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                                                  >> 4U))) 
                                    | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                                       != (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r) 
                                                 >> 2U)))) 
                                   & (IData)(__VdfgRegularize_h6e95ff9d_0_372)) 
                                  << 2U)) | (((((0U 
                                                 == 
                                                 (3U 
                                                  & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r 
                                                     >> 2U))) 
                                                | ((2U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                                                   != 
                                                   (1U 
                                                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r) 
                                                       >> 1U)))) 
                                               & (IData)(__VdfgRegularize_h6e95ff9d_0_373)) 
                                              << 1U) 
                                             | (((0U 
                                                  == 
                                                  (3U 
                                                   & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)) 
                                                 | ((2U 
                                                     == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                                                    != 
                                                    (1U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r)))) 
                                                & (IData)(__VdfgRegularize_h6e95ff9d_0_374)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ind_unreg_w 
        = (((((((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w) 
                  & (0x00020000U == (0x00030000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))) 
                 & ((8U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                            - (IData)(0x00000057U))) 
                    & (~ ((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                                        >> 0x00000010U))) 
                          | (IData)(__VdfgRegularize_h6e95ff9d_0_366))))) 
                | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144) 
                    & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                   & (0x00010000U == (0x00030000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)))) 
               << 4U) | ((((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w) 
                             & (0x00008000U == (0x0000c000U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))) 
                            & ((7U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                       - (IData)(0x00000057U))) 
                               & (~ ((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                                                   >> 0x0000000eU))) 
                                     | (IData)(__VdfgRegularize_h6e95ff9d_0_367))))) 
                           | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_145) 
                               & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                              & (0x00004000U == (0x0000c000U 
                                                 & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)))) 
                          << 3U) | (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w) 
                                       & (0x00002000U 
                                          == (0x00003000U 
                                              & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))) 
                                      & ((6U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                                 - (IData)(0x00000057U))) 
                                         & (~ ((1U 
                                                == 
                                                (3U 
                                                 & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                                                    >> 0x0000000cU))) 
                                               | (IData)(__VdfgRegularize_h6e95ff9d_0_368))))) 
                                     | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_146) 
                                         & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                                        & (0x00001000U 
                                           == (0x00003000U 
                                               & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)))) 
                                    << 2U))) | ((((
                                                   ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w) 
                                                    & (0x00000800U 
                                                       == 
                                                       (0x00000c00U 
                                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))) 
                                                   & ((5U 
                                                       == 
                                                       ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                                        - (IData)(0x00000057U))) 
                                                      & (~ 
                                                         ((1U 
                                                           == 
                                                           (3U 
                                                            & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                                                               >> 0x0000000aU))) 
                                                          | (IData)(__VdfgRegularize_h6e95ff9d_0_369))))) 
                                                  | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_147) 
                                                      & (5U 
                                                         == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                                                     & (0x00000400U 
                                                        == 
                                                        (0x00000c00U 
                                                         & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)))) 
                                                 << 1U) 
                                                | ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w) 
                                                     & (0x00000200U 
                                                        == 
                                                        (0x00000300U 
                                                         & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))) 
                                                    & ((4U 
                                                        == 
                                                        ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                                         - (IData)(0x00000057U))) 
                                                       & (~ 
                                                          ((1U 
                                                            == 
                                                            (3U 
                                                             & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                                                                >> 8U))) 
                                                           | (IData)(__VdfgRegularize_h6e95ff9d_0_370))))) 
                                                   | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_148) 
                                                       & (5U 
                                                          == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                                                      & (0x00000100U 
                                                         == 
                                                         (0x00000300U 
                                                          & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)))))) 
            << 4U) | (((((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w) 
                           & (0x00000080U == (0x000000c0U 
                                              & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))) 
                          & ((3U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                     - (IData)(0x00000057U))) 
                             & (~ ((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                                                 >> 6U))) 
                                   | (IData)(__VdfgRegularize_h6e95ff9d_0_371))))) 
                         | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_149) 
                             & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                            & (0x00000040U == (0x000000c0U 
                                               & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)))) 
                        << 3U) | (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w) 
                                     & (0x00000020U 
                                        == (0x00000030U 
                                            & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))) 
                                    & ((2U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                               - (IData)(0x00000057U))) 
                                       & (~ ((1U == 
                                              (3U & 
                                               (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                                                >> 4U))) 
                                             | (IData)(__VdfgRegularize_h6e95ff9d_0_372))))) 
                                   | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_150) 
                                       & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                                      & (0x00000010U 
                                         == (0x00000030U 
                                             & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)))) 
                                  << 2U)) | ((((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w) 
                                                 & (8U 
                                                    == 
                                                    (0x0000000cU 
                                                     & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))) 
                                                & ((1U 
                                                    == 
                                                    ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                                     - (IData)(0x00000057U))) 
                                                   & (~ 
                                                      ((1U 
                                                        == 
                                                        (3U 
                                                         & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r 
                                                            >> 2U))) 
                                                       | (IData)(__VdfgRegularize_h6e95ff9d_0_373))))) 
                                               | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_151) 
                                                   & (5U 
                                                      == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                                                  & (4U 
                                                     == 
                                                     (0x0000000cU 
                                                      & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)))) 
                                              << 1U) 
                                             | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w) 
                                                 & ((0U 
                                                     == 
                                                     ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                                      - (IData)(0x00000057U))) 
                                                    & ((~ 
                                                        ((1U 
                                                          == 
                                                          (3U 
                                                           & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r)) 
                                                         | (IData)(__VdfgRegularize_h6e95ff9d_0_374))) 
                                                       & (2U 
                                                          == 
                                                          (3U 
                                                           & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))))) 
                                                | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_152) 
                                                   & ((5U 
                                                       == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                                      & (1U 
                                                         == 
                                                         (3U 
                                                          & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))))))));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_rx_hit_w 
        = ((((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_36) 
               << 4U) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37) 
                          << 3U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38) 
                                    << 2U))) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39) 
                                                 << 1U) 
                                                | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_40))) 
            << 4U) | ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_41) 
                        << 3U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_42) 
                                  << 2U)) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_43) 
                                              << 1U) 
                                             | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_92))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__adm_grant_w 
        = (((((((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_36)) 
                & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_69)) 
                   & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68)) 
                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_49)))) 
               << 4U) | ((((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37)) 
                           & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_72)) 
                              & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_71)) 
                                 & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_50)))) 
                          << 3U) | (((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38)) 
                                     & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_75)) 
                                        & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_74)) 
                                           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_51)))) 
                                    << 2U))) | ((((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39)) 
                                                  & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_78)) 
                                                     & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_77)) 
                                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52)))) 
                                                 << 1U) 
                                                | ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_40)) 
                                                   & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_81)) 
                                                      & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_80)) 
                                                         & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_53)))))) 
            << 4U) | (((((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_41)) 
                         & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_84)) 
                            & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_83)) 
                               & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_54)))) 
                        << 3U) | (((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_42)) 
                                   & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_87)) 
                                      & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_86)) 
                                         & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_55)))) 
                                  << 2U)) | ((((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_43)) 
                                               & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_90)) 
                                                  & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_89)) 
                                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_56)))) 
                                              << 1U) 
                                             | ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_92)) 
                                                & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_142)) 
                                                   & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_141)) 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_120)))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w 
        = (((((((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_36)) 
                & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_69)) 
                   & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68)) 
                      & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_49)) 
                         & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_67))))) 
               << 4U) | ((((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37)) 
                           & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_72)) 
                              & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_71)) 
                                 & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_50)) 
                                    & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_70))))) 
                          << 3U) | (((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38)) 
                                     & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_75)) 
                                        & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_74)) 
                                           & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_51)) 
                                              & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_73))))) 
                                    << 2U))) | ((((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39)) 
                                                  & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_78)) 
                                                     & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_77)) 
                                                        & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52)) 
                                                           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_76))))) 
                                                 << 1U) 
                                                | ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_40)) 
                                                   & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_81)) 
                                                      & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_80)) 
                                                         & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_53)) 
                                                            & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_79))))))) 
            << 4U) | (((((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_41)) 
                         & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_84)) 
                            & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_83)) 
                               & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_54)) 
                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_82))))) 
                        << 3U) | (((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_42)) 
                                   & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_87)) 
                                      & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_86)) 
                                         & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_55)) 
                                            & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_85))))) 
                                  << 2U)) | ((((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_43)) 
                                               & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_90)) 
                                                  & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_89)) 
                                                     & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_56)) 
                                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_88))))) 
                                              << 1U) 
                                             | ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_92)) 
                                                & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_142)) 
                                                   & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_141)) 
                                                      & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_120)) 
                                                         & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_91))))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w 
        = (((((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_36) 
                | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_69) 
                   | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68) 
                      | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_49) 
                         | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_103) 
                            | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_67)))))) 
               << 4U) | ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37) 
                           | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_72) 
                              | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_71) 
                                 | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_50) 
                                    | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_102) 
                                       | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_70)))))) 
                          << 3U) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38) 
                                     | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_75) 
                                        | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_74) 
                                           | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_51) 
                                              | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_101) 
                                                 | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_73)))))) 
                                    << 2U))) | ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39) 
                                                  | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_78) 
                                                     | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_77) 
                                                        | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52) 
                                                           | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_100) 
                                                              | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_76)))))) 
                                                 << 1U) 
                                                | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_40) 
                                                   | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_81) 
                                                      | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_80) 
                                                         | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_53) 
                                                            | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_99) 
                                                               | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_79)))))))) 
            << 4U) | (((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_41) 
                         | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_84) 
                            | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_83) 
                               | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_54) 
                                  | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_98) 
                                     | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_82)))))) 
                        << 3U) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_42) 
                                   | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_87) 
                                      | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_86) 
                                         | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_55) 
                                            | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_97) 
                                               | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_85)))))) 
                                  << 2U)) | ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_43) 
                                               | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_90) 
                                                  | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_89) 
                                                     | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_56) 
                                                        | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_96) 
                                                           | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_88)))))) 
                                              << 1U) 
                                             | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_92) 
                                                | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_142) 
                                                   | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_120) 
                                                      | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_91) 
                                                         | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95) 
                                                            | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_141)))))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
        = (((QData)((IData)((0x0000000fU & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_36)
                                             ? ((IData)(3U) 
                                                + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))
                                             : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_69)
                                                 ? 
                                                ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)
                                                  ? 
                                                 (1U 
                                                  & (- (IData)(
                                                               (1U 
                                                                & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                                                   >> 8U)))))
                                                  : 2U)
                                                 : 
                                                ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68)
                                                  ? 9U
                                                  : 
                                                 (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_67)
                                                    ? 0x0aU
                                                    : 
                                                   ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_103)
                                                     ? 
                                                    ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wtxla_r)
                                                      ? 0x0cU
                                                      : 0x0bU)
                                                     : 3U)) 
                                                  & (- (IData)(
                                                               (1U 
                                                                & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_49)))))))))))) 
            << 0x00000020U) | (QData)((IData)((((((0x000000f0U 
                                                   & (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37)
                                                        ? 
                                                       ((IData)(3U) 
                                                        + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))
                                                        : 
                                                       ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_72)
                                                         ? 
                                                        ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)
                                                          ? 
                                                         (1U 
                                                          & (- (IData)(
                                                                       (1U 
                                                                        & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                                                           >> 7U)))))
                                                          : 2U)
                                                         : 
                                                        ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_71)
                                                          ? 9U
                                                          : 
                                                         (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_70)
                                                            ? 0x0aU
                                                            : 
                                                           ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_102)
                                                             ? 
                                                            ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wtxla_r)
                                                              ? 0x0cU
                                                              : 0x0bU)
                                                             : 3U)) 
                                                          & (- (IData)(
                                                                       (1U 
                                                                        & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_50))))))))) 
                                                      << 4U)) 
                                                  | (0x0000000fU 
                                                     & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38)
                                                         ? 
                                                        ((IData)(3U) 
                                                         + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))
                                                         : 
                                                        ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_75)
                                                          ? 
                                                         ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)
                                                           ? 
                                                          (1U 
                                                           & (- (IData)(
                                                                        (1U 
                                                                         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                                                            >> 6U)))))
                                                           : 2U)
                                                          : 
                                                         ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_74)
                                                           ? 9U
                                                           : 
                                                          (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_73)
                                                             ? 0x0aU
                                                             : 
                                                            ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_101)
                                                              ? 
                                                             ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wtxla_r)
                                                               ? 0x0cU
                                                               : 0x0bU)
                                                              : 3U)) 
                                                           & (- (IData)(
                                                                        (1U 
                                                                         & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_51))))))))))) 
                                                 << 0x00000018U) 
                                                | (((0x000000f0U 
                                                     & (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39)
                                                          ? 
                                                         ((IData)(3U) 
                                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))
                                                          : 
                                                         ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_78)
                                                           ? 
                                                          ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)
                                                            ? 
                                                           (1U 
                                                            & (- (IData)(
                                                                         (1U 
                                                                          & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                                                             >> 5U)))))
                                                            : 2U)
                                                           : 
                                                          ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_77)
                                                            ? 9U
                                                            : 
                                                           (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_76)
                                                              ? 0x0aU
                                                              : 
                                                             ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_100)
                                                               ? 
                                                              ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wtxla_r)
                                                                ? 0x0cU
                                                                : 0x0bU)
                                                               : 3U)) 
                                                            & (- (IData)(
                                                                         (1U 
                                                                          & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52))))))))) 
                                                        << 4U)) 
                                                    | (0x0000000fU 
                                                       & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_40)
                                                           ? 
                                                          ((IData)(3U) 
                                                           + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))
                                                           : 
                                                          ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_81)
                                                            ? 
                                                           ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)
                                                             ? 
                                                            (1U 
                                                             & (- (IData)(
                                                                          (1U 
                                                                           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                                                              >> 4U)))))
                                                             : 2U)
                                                            : 
                                                           ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_80)
                                                             ? 9U
                                                             : 
                                                            (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_79)
                                                               ? 0x0aU
                                                               : 
                                                              ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_99)
                                                                ? 
                                                               ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wtxla_r)
                                                                 ? 0x0cU
                                                                 : 0x0bU)
                                                                : 3U)) 
                                                             & (- (IData)(
                                                                          (1U 
                                                                           & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_53))))))))))) 
                                                   << 0x00000010U)) 
                                               | ((((0x000000f0U 
                                                     & (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_41)
                                                          ? 
                                                         ((IData)(3U) 
                                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))
                                                          : 
                                                         ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_84)
                                                           ? 
                                                          ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)
                                                            ? 
                                                           (1U 
                                                            & (- (IData)(
                                                                         (1U 
                                                                          & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                                                             >> 3U)))))
                                                            : 2U)
                                                           : 
                                                          ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_83)
                                                            ? 9U
                                                            : 
                                                           (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_82)
                                                              ? 0x0aU
                                                              : 
                                                             ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_98)
                                                               ? 
                                                              ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wtxla_r)
                                                                ? 0x0cU
                                                                : 0x0bU)
                                                               : 3U)) 
                                                            & (- (IData)(
                                                                         (1U 
                                                                          & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_54))))))))) 
                                                        << 4U)) 
                                                    | (0x0000000fU 
                                                       & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_42)
                                                           ? 
                                                          ((IData)(3U) 
                                                           + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))
                                                           : 
                                                          ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_87)
                                                            ? 
                                                           ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)
                                                             ? 
                                                            (1U 
                                                             & (- (IData)(
                                                                          (1U 
                                                                           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                                                              >> 2U)))))
                                                             : 2U)
                                                            : 
                                                           ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_86)
                                                             ? 9U
                                                             : 
                                                            (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_85)
                                                               ? 0x0aU
                                                               : 
                                                              ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_97)
                                                                ? 
                                                               ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wtxla_r)
                                                                 ? 0x0cU
                                                                 : 0x0bU)
                                                                : 3U)) 
                                                             & (- (IData)(
                                                                          (1U 
                                                                           & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_55))))))))))) 
                                                   << 8U) 
                                                  | ((0x000000f0U 
                                                      & (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_43)
                                                           ? 
                                                          ((IData)(3U) 
                                                           + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))
                                                           : 
                                                          ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_90)
                                                            ? 
                                                           ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)
                                                             ? 
                                                            (1U 
                                                             & (- (IData)(
                                                                          (1U 
                                                                           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                                                              >> 1U)))))
                                                             : 2U)
                                                            : 
                                                           ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_89)
                                                             ? 9U
                                                             : 
                                                            (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_88)
                                                               ? 0x0aU
                                                               : 
                                                              ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_96)
                                                                ? 
                                                               ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wtxla_r)
                                                                 ? 0x0cU
                                                                 : 0x0bU)
                                                                : 3U)) 
                                                             & (- (IData)(
                                                                          (1U 
                                                                           & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_56))))))))) 
                                                         << 4U)) 
                                                     | (0x0000000fU 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_92)
                                                            ? 
                                                           ((IData)(3U) 
                                                            + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))
                                                            : 
                                                           ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_142)
                                                             ? 
                                                            ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)
                                                              ? 
                                                             (1U 
                                                              & (- (IData)(
                                                                           (1U 
                                                                            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r)))))
                                                              : 2U)
                                                             : 
                                                            ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_141)
                                                              ? 9U
                                                              : 
                                                             (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_91)
                                                                ? 0x0aU
                                                                : 
                                                               ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95)
                                                                 ? 
                                                                ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wtxla_r)
                                                                  ? 0x0cU
                                                                  : 0x0bU)
                                                                 : 3U)) 
                                                              & (- (IData)(
                                                                           (1U 
                                                                            & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_120))))))))))))))));
    __VdfgRegularize_h6e95ff9d_0_28 = ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_92)) 
                                       & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_142)) 
                                          & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_141)) 
                                             & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_120)) 
                                                & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_91)) 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95))))));
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__ram_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__ram_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__ram_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__res_acts_w 
        = (0x0001ffffU & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_278)
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__dyn_ready_w 
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
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__en_q_r) 
                  >> 2U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w 
            = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w));
    }
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__en_q_r) 
                  >> 3U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w 
            = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w));
    }
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__en_q_r) 
                  >> 4U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w 
            = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w));
    }
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__en_q_r) 
                  >> 5U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w 
            = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w));
    }
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__en_q_r) 
                  >> 6U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w 
            = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w));
    }
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__en_q_r) 
                  >> 7U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w 
            = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w));
    }
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__en_q_r) 
                  >> 8U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w 
            = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w));
    }
    if (((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r)) 
         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_initset_w))) {
        if ((8U >= (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[1U] 
                    >> 0x0000001cU))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w) 
                   | (0x01ffU & ((IData)(1U) << (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[1U] 
                                                 >> 0x0000001cU))));
        }
    }
    if (((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r)) 
         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_initset_w))) {
        if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w) 
                   | (0x01ffU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r))));
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[0U] = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[1U] = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[2U] = 0U;
    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_we_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_waddr_w 
            = (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__init_ix_r));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[2U] = 0U;
    } else if ((1U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
        if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ping_w) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_we_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_waddr_w 
                    = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[1U] 
                       >> 0x0000001cU);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[0U] 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[0U];
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[1U] 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[1U];
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[2U] 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[2U];
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
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_da_w 
            = (0x0000ffffffffffffULL & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[1U])) 
                                         << 0x00000020U) 
                                        | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[0U]))));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_open_w 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_open_w;
    } else if ((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_da_w 
            = (0x0000ffffffffffffULL & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[1U])) 
                                         << 0x00000020U) 
                                        | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[0U]))));
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
                & (4U != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_415))) 
               << 3U) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_valid_w) 
                          & (4U != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_414))) 
                         << 2U)) | ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_v_r) 
                                      & (4U != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_413))) 
                                     << 1U) | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_valid_w) 
                                               & (4U 
                                                  != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_412))))) 
            << 4U) | (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_valid_w) 
                         & (4U != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_411))) 
                        << 3U) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_valid_w) 
                                   & (4U != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_410))) 
                                  << 2U)) | ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_valid_w) 
                                               & (4U 
                                                  != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_409))) 
                                              << 1U) 
                                             | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_valid_w) 
                                                & (4U 
                                                   != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_408))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_arm_w = 0U;
    if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_valid_w) 
         & (9U > ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w) 
                  - (IData)(0x00000013U))))) {
        if ((8U >= (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w) 
                                   - (IData)(3U))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_arm_w 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_arm_w) 
                   | (0x01ffU & ((IData)(1U) << (0x0000000fU 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w) 
                                                    - (IData)(3U))))));
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U] 
        = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_cancel_w)) 
                    << 0x0000002fU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_slot_w)) 
                                        << 0x00000028U) 
                                       | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_owner_w)) 
                                           << 0x00000020U) 
                                          | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_deadline_w))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U] 
        = ((0xffff0000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U]) 
           | (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_cancel_w)) 
                        << 0x0000002fU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_slot_w)) 
                                            << 0x00000028U) 
                                           | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_owner_w)) 
                                               << 0x00000020U) 
                                              | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_deadline_w))))) 
                      >> 0x00000020U)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U] 
        = ((0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U]) 
           | ((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_cancel_w)) 
                        << 0x0000002fU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w)) 
                                            << 0x00000028U) 
                                           | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_owner_w)) 
                                               << 0x00000020U) 
                                              | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_deadline_w)))))) 
              << 0x00000010U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U] 
        = (((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_cancel_w)) 
                      << 0x0000002fU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w)) 
                                          << 0x00000028U) 
                                         | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_owner_w)) 
                                             << 0x00000020U) 
                                            | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_deadline_w)))))) 
            >> 0x00000010U) | ((IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_cancel_w)) 
                                          << 0x0000002fU) 
                                         | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w)) 
                                             << 0x00000028U) 
                                            | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_owner_w)) 
                                                << 0x00000020U) 
                                               | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_deadline_w))))) 
                                        >> 0x00000020U)) 
                               << 0x00000010U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U] 
        = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_cancel_w)) 
                    << 0x0000002fU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_slot_w)) 
                                        << 0x00000028U) 
                                       | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_slot_w)) 
                                           << 0x00000020U) 
                                          | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_deadline_w))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U] 
        = ((0xffff0000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U]) 
           | (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_cancel_w)) 
                        << 0x0000002fU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_slot_w)) 
                                            << 0x00000028U) 
                                           | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_slot_w)) 
                                               << 0x00000020U) 
                                              | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_deadline_w))))) 
                      >> 0x00000020U)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U] 
        = ((0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U]) 
           | ((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_cancel_w)) 
                        << 0x0000002fU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_slot_w)) 
                                            << 0x00000028U) 
                                           | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_owner_w)) 
                                               << 0x00000020U) 
                                              | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_deadline_w)))))) 
              << 0x00000010U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U] 
        = (((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_cancel_w)) 
                      << 0x0000002fU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_slot_w)) 
                                          << 0x00000028U) 
                                         | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_owner_w)) 
                                             << 0x00000020U) 
                                            | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_deadline_w)))))) 
            >> 0x00000010U) | ((IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_cancel_w)) 
                                          << 0x0000002fU) 
                                         | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_slot_w)) 
                                             << 0x00000028U) 
                                            | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_owner_w)) 
                                                << 0x00000020U) 
                                               | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_deadline_w))))) 
                                        >> 0x00000020U)) 
                               << 0x00000010U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U] 
        = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_cancel_w)) 
                    << 0x0000002fU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_slot_w)) 
                                        << 0x00000028U) 
                                       | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_owner_w)) 
                                           << 0x00000020U) 
                                          | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_deadline_w))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U] 
        = ((0xffff0000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U]) 
           | (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_cancel_w)) 
                        << 0x0000002fU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_slot_w)) 
                                            << 0x00000028U) 
                                           | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_owner_w)) 
                                               << 0x00000020U) 
                                              | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_deadline_w))))) 
                      >> 0x00000020U)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U] 
        = ((0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U]) 
           | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_dl_r 
              << 0x00000010U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U] 
        = ((0xffff0000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U]) 
           | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_dl_r 
              >> 0x00000010U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U] 
        = ((0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U]) 
           | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_c_r) 
               << 0x0000001fU) | ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_ann_r)
                                     ? 0x46U : 0x45U) 
                                   << 0x00000018U) 
                                  | (0x00ff0000U & 
                                     (((IData)(0x90U) 
                                       + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_ann_r)) 
                                      << 0x00000010U)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U] 
        = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_cancel_w)) 
                    << 0x0000002fU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_slot_w)) 
                                        << 0x00000028U) 
                                       | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_owner_w)) 
                                           << 0x00000020U) 
                                          | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_deadline_w))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U] 
        = ((0xffff0000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U]) 
           | (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_cancel_w)) 
                        << 0x0000002fU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_slot_w)) 
                                            << 0x00000028U) 
                                           | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_owner_w)) 
                                               << 0x00000020U) 
                                              | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_deadline_w))))) 
                      >> 0x00000020U)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U] 
        = ((0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U]) 
           | ((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_cancel_w)) 
                        << 0x0000002fU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_slot_w)) 
                                            << 0x00000028U) 
                                           | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_owner_w)) 
                                               << 0x00000020U) 
                                              | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_deadline_w)))))) 
              << 0x00000010U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U] 
        = (((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_cancel_w)) 
                      << 0x0000002fU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_slot_w)) 
                                          << 0x00000028U) 
                                         | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_owner_w)) 
                                             << 0x00000020U) 
                                            | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_deadline_w)))))) 
            >> 0x00000010U) | ((IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_cancel_w)) 
                                          << 0x0000002fU) 
                                         | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_slot_w)) 
                                             << 0x00000028U) 
                                            | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_owner_w)) 
                                                << 0x00000020U) 
                                               | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_deadline_w))))) 
                                        >> 0x00000020U)) 
                               << 0x00000010U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_accept_w 
        = ((~ (IData)(__VdfgRegularize_h6e95ff9d_0_277)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_ok_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_txs_alloc_req_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_txs_gnt_w)) 
           & (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__span_w 
        = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_r) 
                          & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_158)));
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_167 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_is_tkr_w)
                                                   ? 
                                                  ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__gp_valid_r)) 
                                                   & (1U 
                                                      == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r)))
                                                   : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txn_ready_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_wdata_w 
        = (0x000000ffU & ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r))
                           ? (IData)(__VdfgRegularize_h6e95ff9d_0_228)
                           : ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r))
                               ? ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r))
                                   ? (IData)(__VdfgRegularize_h6e95ff9d_0_228)
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mut_req_w 
        = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_op_w)) 
           | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_op_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__eff_len_w 
        = (((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_op_w)) 
            & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_len_w)))
            ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w)
            : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_len_w));
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
        = (0x01feU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
    if ((1U & (~ (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_rx_hit_w)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
                      & (0U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w 
                    = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w 
        = (0x01fdU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
    if ((1U & (~ ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_rx_hit_w) 
                  >> 1U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
                      & (1U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r) 
                        >> 1U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w 
                    = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w 
        = (0x01fbU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
    if ((1U & (~ ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_rx_hit_w) 
                  >> 2U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
                      & (2U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r) 
                        >> 2U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w 
                    = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w 
        = (0x01f7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
    if ((1U & (~ ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_rx_hit_w) 
                  >> 3U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
                      & (3U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r) 
                        >> 3U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w 
                    = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w 
        = (0x01efU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
    if ((1U & (~ ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_rx_hit_w) 
                  >> 4U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
                      & (4U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r) 
                        >> 4U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w 
                    = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w 
        = (0x01dfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
    if ((1U & (~ ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_rx_hit_w) 
                  >> 5U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
                      & (5U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r) 
                        >> 5U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w 
                    = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w 
        = (0x01bfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
    if ((1U & (~ ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_rx_hit_w) 
                  >> 6U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
                      & (6U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r) 
                        >> 6U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w 
                    = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w 
        = (0x017fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
    if ((1U & (~ ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_rx_hit_w) 
                  >> 7U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
                      & (7U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r) 
                        >> 7U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w 
                    = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w 
        = (0x00ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
    if ((1U & (~ ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_rx_hit_w) 
                  >> 8U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
                      & (8U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
            if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r) 
                          >> 8U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w 
                    = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
            }
        }
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_19 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_43)
                                                  ? (IData)(__VdfgRegularize_h6e95ff9d_0_28)
                                                  : 
                                                 ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_90)
                                                   ? (IData)(__VdfgRegularize_h6e95ff9d_0_28)
                                                   : 
                                                  ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_89)
                                                    ? (IData)(__VdfgRegularize_h6e95ff9d_0_28)
                                                    : 
                                                   ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_56)
                                                     ? (IData)(__VdfgRegularize_h6e95ff9d_0_28)
                                                     : 
                                                    ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_88)
                                                      ? (IData)(__VdfgRegularize_h6e95ff9d_0_28)
                                                      : 
                                                     ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_96) 
                                                      | (IData)(__VdfgRegularize_h6e95ff9d_0_28)))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__space_w 
        = (1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__out_vld_r) 
                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__skid_vld_r)) 
                    | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__skid_vld_r) 
                        & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__fetch_r)) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__out_vld_r) 
                          & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__fetch_r) 
                             & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_407)))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__avail_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__rd_ptr_r) 
           != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__wr_cmt_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__take_wr_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__in_range_w) 
            & (0x00010000U == (0x000f0000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w))) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__dyn_ready_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w = 0U;
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
                            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__is_q_field_w) {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_wdata_w 
                                    = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r))
                                        ? (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r 
                                                   >> 0x20U))
                                        : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r));
                            }
                        } else {
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
                        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__is_q_field_w) {
                            if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r))) {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_wdata_w 
                                    = (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r 
                                               >> 0x20U));
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w = 1U;
                            } else {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_wdata_w 
                                    = (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r);
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w = 0U;
                        }
                    }
                }
            } else if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                         >> 0x0000002cU))))) {
                if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                   >> 0x0000002bU)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_wdata_w 
                        = (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxr_data_r);
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w 
                        = (1U & (4U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r)));
                } else {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w 
                        = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxr_valid_r)));
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
                                         ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__dyn_ready_w)
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
                                                            (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_223 
                                                             >> 0x00000020U)))
                                                  : (IData)(
                                                            (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_223 
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
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rb_hold_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w = 1U;
        }
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_5 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_open_w) 
                                                | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_close_w));
    __VdfgRegularize_h6e95ff9d_0_276 = (1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_accept_w) 
                                                 | (IData)(__VdfgRegularize_h6e95ff9d_0_277))));
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
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_data_w 
                        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_pdu_byte_w));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_valid_w 
                        = (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                        = (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r));
                } else {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_data_w 
                        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_wr_data_w));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_valid_w 
                        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__cancel_hit_w)) 
                           & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r)));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_alloc_req_w;
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_data_w 
                    = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__maapeng_txs_wr_data_w));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_valid_w 
                    = (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                    = (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r));
            } else {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_data_w 
                    = (0x000000ffU & ((0x0026U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                       ? ((0x00000020U 
                                           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                           ? ((- (IData)(
                                                         (1U 
                                                          & (~ 
                                                             ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r) 
                                                              >> 3U))))) 
                                              & (((4U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                   ? 
                                                  (((1U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                     ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__raw_ct_r)
                                                     : 
                                                    ((IData)(
                                                             ((8U 
                                                               == 
                                                               (0x0000001cU 
                                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[11U])) 
                                                              & (0U 
                                                                 == 
                                                                 (0x0000000fU 
                                                                  & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[11U] 
                                                                      << 2U) 
                                                                     | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                                                        >> 0x0000001eU))))))
                                                      ? 
                                                     (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__uns_r) 
                                                       << 7U) 
                                                      | (0x0000007fU 
                                                         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__raw_ct_r) 
                                                            >> 8U)))
                                                      : 
                                                     ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__raw_ct_r) 
                                                      >> 8U))) 
                                                   & (- (IData)(
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r) 
                                                                     >> 1U))))))
                                                   : 
                                                  ((2U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                     ? 
                                                    ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[4U] 
                                                      << 0x00000012U) 
                                                     | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[4U] 
                                                        >> 0x0000000eU))
                                                     : 
                                                    ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[4U] 
                                                      << 0x0000000aU) 
                                                     | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[4U] 
                                                        >> 0x00000016U)))
                                                    : 
                                                   ((1U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                     ? 
                                                    ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[7U] 
                                                      << 2U) 
                                                     | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[6U] 
                                                        >> 0x0000001eU))
                                                     : 
                                                    ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[7U] 
                                                      << 0x0000001aU) 
                                                     | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[7U] 
                                                        >> 6U))))) 
                                                 & (- (IData)(
                                                              (1U 
                                                               & (~ 
                                                                  ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r) 
                                                                   >> 4U)))))))
                                           : ((0x00000010U 
                                               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                               ? ((8U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                   ? 
                                                  ((4U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                    ? 
                                                   ((2U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                     ? 
                                                    ((1U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                      ? 
                                                     ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[7U] 
                                                       << 0x00000012U) 
                                                      | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[7U] 
                                                         >> 0x0000000eU))
                                                      : 
                                                     ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[7U] 
                                                       << 0x0000000aU) 
                                                      | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[7U] 
                                                         >> 0x00000016U)))
                                                     : 
                                                    ((1U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                      ? 
                                                     ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[8U] 
                                                       << 2U) 
                                                      | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[7U] 
                                                         >> 0x0000001eU))
                                                      : 
                                                     ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[8U] 
                                                       << 0x0000001aU) 
                                                      | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[8U] 
                                                         >> 6U))))
                                                    : 
                                                   ((2U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                     ? 
                                                    ((1U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                      ? 
                                                     ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[8U] 
                                                       << 0x00000012U) 
                                                      | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[8U] 
                                                         >> 0x0000000eU))
                                                      : 
                                                     ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[8U] 
                                                       << 0x0000000aU) 
                                                      | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[8U] 
                                                         >> 0x00000016U)))
                                                     : 
                                                    ((1U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                      ? vlSelfRef.milan_datapath__DOT__csr__DOT__adp_eidlo
                                                      : 
                                                     (vlSelfRef.milan_datapath__DOT__csr__DOT__adp_eidlo 
                                                      >> 8U))))
                                                   : 
                                                  ((4U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                    ? 
                                                   ((2U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                     ? 
                                                    ((1U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                      ? 
                                                     (vlSelfRef.milan_datapath__DOT__csr__DOT__adp_eidlo 
                                                      >> 0x00000010U)
                                                      : 
                                                     (vlSelfRef.milan_datapath__DOT__csr__DOT__adp_eidlo 
                                                      >> 0x00000018U))
                                                     : 
                                                    ((1U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                      ? vlSelfRef.milan_datapath__DOT__csr__DOT__adp_eidhi
                                                      : 
                                                     (vlSelfRef.milan_datapath__DOT__csr__DOT__adp_eidhi 
                                                      >> 8U)))
                                                    : 
                                                   ((2U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                     ? 
                                                    ((1U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                      ? 
                                                     (vlSelfRef.milan_datapath__DOT__csr__DOT__adp_eidhi 
                                                      >> 0x00000010U)
                                                      : 
                                                     (vlSelfRef.milan_datapath__DOT__csr__DOT__adp_eidhi 
                                                      >> 0x00000018U))
                                                     : 
                                                    ((1U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                      ? 
                                                     ((IData)(0x0cU) 
                                                      + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r))
                                                      : 
                                                     (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__status_r) 
                                                       << 3U) 
                                                      | (7U 
                                                         & (((IData)(0x000cU) 
                                                             + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r)) 
                                                            >> 8U)))))))
                                               : ((8U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                   ? 
                                                  ((4U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                    ? 
                                                   ((2U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                     ? 
                                                    ((1U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                      ? 
                                                     (0x0000000fU 
                                                      & (1U 
                                                         | ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[11U] 
                                                             << 2U) 
                                                            | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                                               >> 0x0000001eU))))
                                                      : 0xfbU)
                                                     : 
                                                    ((1U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                      ? 0xf0U
                                                      : 0x22U))
                                                    : 
                                                   ((2U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                     ? 
                                                    ((1U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                      ? 
                                                     (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ahi 
                                                      >> 8U)
                                                      : vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ahi)
                                                     : 
                                                    ((1U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                      ? 
                                                     (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_alo 
                                                      >> 0x00000018U)
                                                      : 
                                                     (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_alo 
                                                      >> 0x00000010U))))
                                                   : 
                                                  ((4U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                    ? 
                                                   ((2U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                     ? 
                                                    ((1U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                      ? 
                                                     (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_alo 
                                                      >> 8U)
                                                      : vlSelfRef.milan_datapath__DOT__csr__DOT__mac_alo)
                                                     : 
                                                    ((1U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                      ? 
                                                     ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[9U] 
                                                       << 2U) 
                                                      | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[8U] 
                                                         >> 0x0000001eU))
                                                      : 
                                                     ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[9U] 
                                                       << 0x0000001aU) 
                                                      | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[9U] 
                                                         >> 6U))))
                                                    : 
                                                   ((2U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                     ? 
                                                    ((1U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                      ? 
                                                     ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[9U] 
                                                       << 0x00000012U) 
                                                      | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[9U] 
                                                         >> 0x0000000eU))
                                                      : 
                                                     ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[9U] 
                                                       << 0x0000000aU) 
                                                      | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[9U] 
                                                         >> 0x00000016U)))
                                                     : 
                                                    ((1U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r))
                                                      ? 
                                                     ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                                       << 2U) 
                                                      | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[9U] 
                                                         >> 0x0000001eU))
                                                      : 
                                                     ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                                       << 0x0000001aU) 
                                                      | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[10U] 
                                                         >> 6U))))))))
                                       : (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_133)
                                            ? ((0U 
                                                == 
                                                (0x000007ffU 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r) 
                                                    - (IData)(0x0026U))))
                                                ? ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r) 
                                                   >> 8U)
                                                : (
                                                   (1U 
                                                    == 
                                                    (0x000007ffU 
                                                     & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r) 
                                                        - (IData)(0x0026U))))
                                                    ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)
                                                    : 
                                                   ((2U 
                                                     == 
                                                     (0x000007ffU 
                                                      & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r) 
                                                         - (IData)(0x0026U))))
                                                     ? 
                                                    ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r) 
                                                     >> 8U)
                                                     : 
                                                    ((3U 
                                                      == 
                                                      (0x000007ffU 
                                                       & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r) 
                                                          - (IData)(0x0026U))))
                                                      ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r)
                                                      : 
                                                     ((4U 
                                                       == 
                                                       (0x000007ffU 
                                                        & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r) 
                                                           - (IData)(0x0026U))))
                                                       ? 
                                                      ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_emit_count_w) 
                                                       >> 8U)
                                                       : 
                                                      ((5U 
                                                        == 
                                                        (0x000007ffU 
                                                         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r) 
                                                            - (IData)(0x0026U))))
                                                        ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_emit_count_w)
                                                        : 
                                                       ((IData)(
                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r 
                                                                 >> 
                                                                 (0x0000003fU 
                                                                  & (((IData)(0x3fU) 
                                                                      - 
                                                                      (0x00000038U 
                                                                       & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r) 
                                                                           - (IData)(6U)) 
                                                                          << 3U))) 
                                                                     - (IData)(7U))))) 
                                                        & (- (IData)(
                                                                     (1U 
                                                                      & (~ 
                                                                         ((6U 
                                                                           == 
                                                                           (0x000007ffU 
                                                                            & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r) 
                                                                               - (IData)(0x0026U)))) 
                                                                          | (7U 
                                                                             == 
                                                                             (0x000007ffU 
                                                                              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r) 
                                                                                - (IData)(0x0026U))))))))))))))))
                                            : ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r)
                                                ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)
                                                : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_rd_data_w))) 
                                          & (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pay_w))))));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_valid_w 
                    = ((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r)) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__byte_ok_w));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                    = (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r));
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_data_w 
                    = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_pdu_byte_w));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_valid_w 
                    = (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                    = (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r));
            } else {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_data_w 
                    = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_valid_w 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_txs_alloc_req_w;
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_data_w 
                = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txs_wr_data_w));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_valid_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txs_wr_valid_w;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txs_alloc_req_w;
        } else {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_data_w 
                = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_txs_wr_data_w));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_valid_w 
                = (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                = (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_alloc_wait_r) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w = 0U;
        }
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_18 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_valid_w) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_prng_busy_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__busy_r) 
              | (0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_candidate_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_valid_r) 
           & ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_st_r)) 
              & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_active_r)) 
                 & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_167))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_now_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r)) 
           & ((~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_hold_r) 
                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__arm_ok_w)) 
                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mut_req_w))) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_req_w)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_273 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__eff_len_w) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_offset_w));
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
    __VdfgRegularize_h6e95ff9d_0_20 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_42)
                                        ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_19)
                                        : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_87)
                                            ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_19)
                                            : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_86)
                                                ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_19)
                                                : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_55)
                                                    ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_19)
                                                    : 
                                                   ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_85)
                                                     ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_19)
                                                     : 
                                                    ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_19) 
                                                     | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_97)))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__advance_e_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_e_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_stri_out_w 
        = (((((4U & ((0x03fffffcU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w) 
                                     >> 6U)) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_5) 
                                                 & (8U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_src_w))) 
                                                << 2U))) 
              | ((2U & ((0x03fffffeU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w) 
                                        >> 6U)) | (
                                                   ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_5) 
                                                    & (7U 
                                                       == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_src_w))) 
                                                   << 1U))) 
                 | (1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w) 
                           >> 6U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_5) 
                                     & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_src_w))))))) 
             << 6U) | (((2U & ((0x0ffffffeU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w) 
                                               >> 4U)) 
                               | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_5) 
                                   & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_src_w))) 
                                  << 1U))) | (1U & 
                                              (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w) 
                                                >> 4U) 
                                               | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_5) 
                                                  & (4U 
                                                     == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_src_w)))))) 
                       << 4U)) | ((((2U & ((0x3ffffffeU 
                                            & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w) 
                                               >> 2U)) 
                                           | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_5) 
                                               & (3U 
                                                  == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_src_w))) 
                                              << 1U))) 
                                    | (1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w) 
                                              >> 2U) 
                                             | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_5) 
                                                & (2U 
                                                   == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_src_w)))))) 
                                   << 2U) | ((2U & 
                                              ((0xfffffffeU 
                                                & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w)) 
                                               | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_5) 
                                                   & (1U 
                                                      == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_src_w))) 
                                                  << 1U))) 
                                             | (1U 
                                                & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w) 
                                                   | ((0U 
                                                       == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_src_w)) 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_5)))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_iss_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__cancel_hit_w)) 
           & ((IData)(__VdfgRegularize_h6e95ff9d_0_276) 
              & ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r)) 
                 & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ok_w)) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__free_ok_w)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_exp_w 
        = ((IData)(__VdfgRegularize_h6e95ff9d_0_276) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ok_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__grant_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__pick_ok_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_prng_valid_w 
        = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_owner_r)) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_18));
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
           & ((vlSelfRef.__VdfgRegularize_h6e95ff9d_0_273 
               <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w)) 
              & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
                  + vlSelfRef.__VdfgRegularize_h6e95ff9d_0_273) 
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
    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__xs_r))) {
        VL_ASSIGN_W(384, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w, Vmilan_datapath__ConstPool__CONST_h997e551f_0);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__recwr_addr_w 
            = (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__init_cnt_r));
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
                = (0x0000ff00U & (((IData)(0x0aU) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r)) 
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
                   | ((0x0000ff00U & (((IData)(0x0aU) 
                                       + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r)) 
                                      << 8U)) | (0x000000ffU 
                                                 & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[11U])));
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__recwr_addr_w 
            = (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__go_take_w 
        = ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__go_pend_r) 
              | (vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_ctrl_r 
                 >> 1U)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_402 = ((3U 
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
    __VdfgRegularize_h6e95ff9d_0_21 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_41)
                                        ? (IData)(__VdfgRegularize_h6e95ff9d_0_20)
                                        : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_84)
                                            ? (IData)(__VdfgRegularize_h6e95ff9d_0_20)
                                            : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_83)
                                                ? (IData)(__VdfgRegularize_h6e95ff9d_0_20)
                                                : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_54)
                                                    ? (IData)(__VdfgRegularize_h6e95ff9d_0_20)
                                                    : 
                                                   ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_82)
                                                     ? (IData)(__VdfgRegularize_h6e95ff9d_0_20)
                                                     : 
                                                    ((IData)(__VdfgRegularize_h6e95ff9d_0_20) 
                                                     | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_98)))))));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_acmp_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_aecp_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_candidate_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_opmut_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_now_w) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mut_req_w) 
              & ((0U != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_len_r) 
                 & ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__eff_len_w)) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__span_ok_w)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_wr_req_w 
        = (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
            & (9U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__init_cnt_r))) 
           | ((~ ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r)) 
                  & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r) 
                     >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r)))) 
              & (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r))));
    vlSelfRef.milan_datapath__DOT__pp_restore_busy_w 
        = ((8U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
           | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_402));
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_ev_si_w 
        = ((2U <= (0x000000ffU & ((IData)(vlSelfRef.milan_datapath__DOT__avtprx_seq) 
                                  - (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__exp_seq_r)))) 
           & (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_ev_sm_w));
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
    __VdfgRegularize_h6e95ff9d_0_22 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_40)
                                        ? (IData)(__VdfgRegularize_h6e95ff9d_0_21)
                                        : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_81)
                                            ? (IData)(__VdfgRegularize_h6e95ff9d_0_21)
                                            : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_80)
                                                ? (IData)(__VdfgRegularize_h6e95ff9d_0_21)
                                                : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_53)
                                                    ? (IData)(__VdfgRegularize_h6e95ff9d_0_21)
                                                    : 
                                                   ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_79)
                                                     ? (IData)(__VdfgRegularize_h6e95ff9d_0_21)
                                                     : 
                                                    ((IData)(__VdfgRegularize_h6e95ff9d_0_21) 
                                                     | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_99)))))));
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
                 | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_153)));
    __VdfgRegularize_h6e95ff9d_0_399 = ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_cnt_r)) 
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
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_acmp_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_aecp_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_key_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_class_w = 0U;
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_acmp_w) {
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_23 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39)
                                                  ? (IData)(__VdfgRegularize_h6e95ff9d_0_22)
                                                  : 
                                                 ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_78)
                                                   ? (IData)(__VdfgRegularize_h6e95ff9d_0_22)
                                                   : 
                                                  ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_77)
                                                    ? (IData)(__VdfgRegularize_h6e95ff9d_0_22)
                                                    : 
                                                   ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52)
                                                     ? (IData)(__VdfgRegularize_h6e95ff9d_0_22)
                                                     : 
                                                    ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_76)
                                                      ? (IData)(__VdfgRegularize_h6e95ff9d_0_22)
                                                      : 
                                                     ((IData)(__VdfgRegularize_h6e95ff9d_0_22) 
                                                      | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_100)))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__accept_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_start_abort_w)) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_283));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_401 = ((1U 
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
                            & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_380)) 
                               | (IData)(__VdfgRegularize_h6e95ff9d_0_399)))))) 
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
                & ((~ (IData)(__VdfgRegularize_h6e95ff9d_0_399)) 
                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_380))) 
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w = 0U;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[0U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[0U];
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
    if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w = 1U;
    }
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[1U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[1U];
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
          >> 1U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w = 1U;
    }
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[2U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[2U];
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
            goto __Vlabel2;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
             & (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
            goto __Vlabel2;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
             | (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__same_key_v;
            goto __Vlabel2;
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
            goto __Vlabel2;
        }
        if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls) 
             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls))) {
            if (((7U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
                 | (8U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
                goto __Vlabel2;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__same_key_v;
            goto __Vlabel2;
        }
        if ((((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
              & (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls))) 
             | ((3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
                & (2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel2;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
        __Vlabel2: ;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
          >> 2U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w = 1U;
    }
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[3U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[3U];
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
            goto __Vlabel3;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
             & (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
            goto __Vlabel3;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
             | (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__same_key_v;
            goto __Vlabel3;
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
            goto __Vlabel3;
        }
        if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls) 
             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls))) {
            if (((7U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
                 | (8U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
                goto __Vlabel3;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__same_key_v;
            goto __Vlabel3;
        }
        if ((((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
              & (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls))) 
             | ((3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
                & (2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel3;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
        __Vlabel3: ;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
          >> 3U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w = 1U;
    }
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[4U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[4U];
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
            goto __Vlabel4;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
             & (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
            goto __Vlabel4;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
             | (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__same_key_v;
            goto __Vlabel4;
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
            goto __Vlabel4;
        }
        if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls) 
             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls))) {
            if (((7U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
                 | (8U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
                goto __Vlabel4;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__same_key_v;
            goto __Vlabel4;
        }
        if ((((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
              & (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls))) 
             | ((3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
                & (2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel4;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
        __Vlabel4: ;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
          >> 4U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w = 1U;
    }
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[5U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[5U];
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
            goto __Vlabel5;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
             & (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
            goto __Vlabel5;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
             | (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__same_key_v;
            goto __Vlabel5;
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
            goto __Vlabel5;
        }
        if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls) 
             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls))) {
            if (((7U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
                 | (8U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
                goto __Vlabel5;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__same_key_v;
            goto __Vlabel5;
        }
        if ((((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
              & (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls))) 
             | ((3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
                & (2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel5;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
        __Vlabel5: ;
    }
}
