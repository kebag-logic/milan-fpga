// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim_sim___ico_comb__TOP__sim__3(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___ico_comb__TOP__sim__3\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ KL_mbx__DOT____VlemCall_229__mbx_place_f;
    IData/*31:0*/ KL_mbx__DOT____VlemCall_228__mbx_place_f;
    IData/*31:0*/ KL_mbx__DOT____VlemCall_227__mbx_place_f;
    IData/*31:0*/ KL_mbx__DOT____VlemCall_226__mbx_place_f;
    IData/*31:0*/ KL_mbx__DOT____VlemCall_225__mbx_place_f;
    IData/*31:0*/ KL_mbx__DOT____VlemCall_224__mbx_place_f;
    IData/*31:0*/ KL_mbx__DOT____VlemCall_223__mbx_place_f;
    IData/*31:0*/ KL_mbx__DOT____VlemCall_222__mbx_place_f;
    IData/*31:0*/ KL_mbx__DOT____VlemCall_221__mbx_place_f;
    IData/*31:0*/ KL_mbx__DOT____VlemCall_220__mbx_place_f;
    IData/*31:0*/ KL_mbx__DOT____VlemCall_219__mbx_place_f;
    IData/*31:0*/ KL_mbx__DOT____VlemCall_218__mbx_place_f;
    IData/*31:0*/ KL_mbx__DOT____VlemCall_217__mbx_place_f;
    IData/*31:0*/ KL_mbx__DOT____VlemCall_216__mbx_place_f;
    IData/*31:0*/ KL_mbx__DOT____VlemCall_215__mbx_place_f;
    IData/*31:0*/ __Vfunc_mbx_place_f__200__value;
    __Vfunc_mbx_place_f__200__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__201__value;
    __Vfunc_mbx_place_f__201__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__202__value;
    __Vfunc_mbx_place_f__202__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__203__value;
    __Vfunc_mbx_place_f__203__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__204__value;
    __Vfunc_mbx_place_f__204__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__205__value;
    __Vfunc_mbx_place_f__205__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__206__value;
    __Vfunc_mbx_place_f__206__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__207__value;
    __Vfunc_mbx_place_f__207__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__208__value;
    __Vfunc_mbx_place_f__208__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__209__value;
    __Vfunc_mbx_place_f__209__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__210__value;
    __Vfunc_mbx_place_f__210__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__211__value;
    __Vfunc_mbx_place_f__211__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__212__value;
    __Vfunc_mbx_place_f__212__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__213__value;
    __Vfunc_mbx_place_f__213__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__214__value;
    __Vfunc_mbx_place_f__214__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__215__value;
    __Vfunc_mbx_place_f__215__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__216__value;
    __Vfunc_mbx_place_f__216__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__217__value;
    __Vfunc_mbx_place_f__217__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__218__value;
    __Vfunc_mbx_place_f__218__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__219__value;
    __Vfunc_mbx_place_f__219__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__220__value;
    __Vfunc_mbx_place_f__220__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__221__value;
    __Vfunc_mbx_place_f__221__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__222__value;
    __Vfunc_mbx_place_f__222__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__223__value;
    __Vfunc_mbx_place_f__223__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__224__value;
    __Vfunc_mbx_place_f__224__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__225__value;
    __Vfunc_mbx_place_f__225__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__226__value;
    __Vfunc_mbx_place_f__226__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__227__value;
    __Vfunc_mbx_place_f__227__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__228__value;
    __Vfunc_mbx_place_f__228__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__229__value;
    __Vfunc_mbx_place_f__229__value = 0;
    // Body
    vlSelfRef.KL_mbx__DOT____VlemCall_199__mbx_place_f 
        = (0x0000ffffU & vlSelfRef.__Vfunc_mbx_place_f__199__value);
    __Vfunc_mbx_place_f__200__value = vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[1U];
    vlSelfRef.KL_mbx__DOT____VlemCall_200__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__200__value);
    __Vfunc_mbx_place_f__201__value = (vlSelfRef.__PVT__KL_mbx__DOT__tx_tail_w[0U] 
                                       >> 0x00000010U);
    vlSelfRef.KL_mbx__DOT____VlemCall_201__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__201__value);
    __Vfunc_mbx_place_f__202__value = (vlSelfRef.__PVT__KL_mbx__DOT__rx_drop_w[0U] 
                                       >> 0x00000010U);
    vlSelfRef.KL_mbx__DOT____VlemCall_202__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__202__value);
    __Vfunc_mbx_place_f__203__value = (vlSelfRef.__PVT__KL_mbx__DOT__rate_drop_w[0U] 
                                       >> 0x00000010U);
    vlSelfRef.KL_mbx__DOT____VlemCall_203__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__203__value);
    __Vfunc_mbx_place_f__204__value = (vlSelfRef.__PVT__KL_mbx__DOT__tx_err_w[0U] 
                                       >> 0x00000010U);
    vlSelfRef.KL_mbx__DOT____VlemCall_204__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__204__value);
    __Vfunc_mbx_place_f__205__value = (vlSelfRef.__PVT__KL_mbx__DOT__rx_pass_w[0U] 
                                       >> 0x00000010U);
    vlSelfRef.KL_mbx__DOT____VlemCall_205__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__205__value);
    __Vfunc_mbx_place_f__206__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__rx_head_w[1U]);
    vlSelfRef.KL_mbx__DOT____VlemCall_206__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__206__value);
    __Vfunc_mbx_place_f__207__value = vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[2U];
    vlSelfRef.KL_mbx__DOT____VlemCall_207__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__207__value);
    __Vfunc_mbx_place_f__208__value = vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[2U];
    vlSelfRef.KL_mbx__DOT____VlemCall_208__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__208__value);
    __Vfunc_mbx_place_f__209__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__tx_tail_w[1U]);
    vlSelfRef.KL_mbx__DOT____VlemCall_209__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__209__value);
    __Vfunc_mbx_place_f__210__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__rx_drop_w[1U]);
    vlSelfRef.KL_mbx__DOT____VlemCall_210__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__210__value);
    __Vfunc_mbx_place_f__211__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__rate_drop_w[1U]);
    vlSelfRef.KL_mbx__DOT____VlemCall_211__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__211__value);
    __Vfunc_mbx_place_f__212__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__tx_err_w[1U]);
    vlSelfRef.KL_mbx__DOT____VlemCall_212__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__212__value);
    __Vfunc_mbx_place_f__213__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__rx_pass_w[1U]);
    vlSelfRef.KL_mbx__DOT____VlemCall_213__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__213__value);
    __Vfunc_mbx_place_f__214__value = (vlSelfRef.__PVT__KL_mbx__DOT__rx_head_w[1U] 
                                       >> 0x00000010U);
    vlSelfRef.KL_mbx__DOT____VlemCall_214__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__214__value);
    __Vfunc_mbx_place_f__215__value = vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[3U];
    KL_mbx__DOT____VlemCall_215__mbx_place_f = (0x0000ffffU 
                                                & __Vfunc_mbx_place_f__215__value);
    __Vfunc_mbx_place_f__216__value = vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[3U];
    KL_mbx__DOT____VlemCall_216__mbx_place_f = (0x0000ffffU 
                                                & __Vfunc_mbx_place_f__216__value);
    __Vfunc_mbx_place_f__217__value = (vlSelfRef.__PVT__KL_mbx__DOT__tx_tail_w[1U] 
                                       >> 0x00000010U);
    KL_mbx__DOT____VlemCall_217__mbx_place_f = (0x0000ffffU 
                                                & __Vfunc_mbx_place_f__217__value);
    __Vfunc_mbx_place_f__218__value = (vlSelfRef.__PVT__KL_mbx__DOT__rx_drop_w[1U] 
                                       >> 0x00000010U);
    KL_mbx__DOT____VlemCall_218__mbx_place_f = (0x0000ffffU 
                                                & __Vfunc_mbx_place_f__218__value);
    __Vfunc_mbx_place_f__219__value = (vlSelfRef.__PVT__KL_mbx__DOT__rate_drop_w[1U] 
                                       >> 0x00000010U);
    KL_mbx__DOT____VlemCall_219__mbx_place_f = (0x0000ffffU 
                                                & __Vfunc_mbx_place_f__219__value);
    __Vfunc_mbx_place_f__220__value = (vlSelfRef.__PVT__KL_mbx__DOT__tx_err_w[1U] 
                                       >> 0x00000010U);
    KL_mbx__DOT____VlemCall_220__mbx_place_f = (0x0000ffffU 
                                                & __Vfunc_mbx_place_f__220__value);
    __Vfunc_mbx_place_f__221__value = (vlSelfRef.__PVT__KL_mbx__DOT__rx_pass_w[1U] 
                                       >> 0x00000010U);
    KL_mbx__DOT____VlemCall_221__mbx_place_f = (0x0000ffffU 
                                                & __Vfunc_mbx_place_f__221__value);
    __Vfunc_mbx_place_f__222__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__rx_head_w[2U]);
    KL_mbx__DOT____VlemCall_222__mbx_place_f = (0x0000ffffU 
                                                & __Vfunc_mbx_place_f__222__value);
    __Vfunc_mbx_place_f__223__value = vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[4U];
    KL_mbx__DOT____VlemCall_223__mbx_place_f = (0x0000ffffU 
                                                & __Vfunc_mbx_place_f__223__value);
    __Vfunc_mbx_place_f__224__value = vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[4U];
    KL_mbx__DOT____VlemCall_224__mbx_place_f = (0x0000ffffU 
                                                & __Vfunc_mbx_place_f__224__value);
    __Vfunc_mbx_place_f__225__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__tx_tail_w[2U]);
    KL_mbx__DOT____VlemCall_225__mbx_place_f = (0x0000ffffU 
                                                & __Vfunc_mbx_place_f__225__value);
    __Vfunc_mbx_place_f__226__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__rx_drop_w[2U]);
    KL_mbx__DOT____VlemCall_226__mbx_place_f = (0x0000ffffU 
                                                & __Vfunc_mbx_place_f__226__value);
    __Vfunc_mbx_place_f__227__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__rate_drop_w[2U]);
    KL_mbx__DOT____VlemCall_227__mbx_place_f = (0x0000ffffU 
                                                & __Vfunc_mbx_place_f__227__value);
    __Vfunc_mbx_place_f__228__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__tx_err_w[2U]);
    KL_mbx__DOT____VlemCall_228__mbx_place_f = (0x0000ffffU 
                                                & __Vfunc_mbx_place_f__228__value);
    __Vfunc_mbx_place_f__229__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__rx_pass_w[2U]);
    KL_mbx__DOT____VlemCall_229__mbx_place_f = (0x0000ffffU 
                                                & __Vfunc_mbx_place_f__229__value);
    vlSelfRef.__PVT__KL_mbx__DOT__reg_rdata_w = (((
                                                   (((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((0x4d420204U 
                                                                                & (- (IData)(
                                                                                (1U 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U])))) 
                                                                                | (0x00061015U 
                                                                                & (- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 1U)))))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 2U)))) 
                                                                                & ((vlSelfRef.KL_mbx__DOT____VlemCall_161__mbx_place_f 
                                                                                | vlSelfRef.KL_mbx__DOT____VlemCall_162__mbx_place_f) 
                                                                                | vlSelfRef.KL_mbx__DOT____VlemCall_163__mbx_place_f))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 3U)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__irq_enable_r)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 4U)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_164__mbx_place_f)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 5U)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_165__mbx_place_f)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 6U)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__tick_ctl_r)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 7U)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__own_eid_lo_r)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 8U)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__own_eid_hi_r)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 9U)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__filter_en_r)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x0000000aU)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__maap_base_lo_r)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x0000000bU)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__maap_base_hi_r)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x0000000cU)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__maap_count_r)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x0000000dU)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__tmr_deadline_r)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x0000000eU)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_166__mbx_place_f)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x0000000fU)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__evt_tail_r)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x00000010U)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_167__mbx_place_f)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x00000011U)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_168__mbx_place_f)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x00000012U)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_169__mbx_place_f)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x00000013U)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_170__mbx_place_f)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x00000014U)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_171__mbx_place_f)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x00000015U)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__own_mac_lo_r[0U])) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x00000016U)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__own_mac_hi_r[0U])) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x00000017U)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_172__mbx_place_f)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x00000018U)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_mem_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w])) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x00000019U)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__pub_da_gate_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x0000001aU)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__pub_licence_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x0000001bU)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__pub_idle_slope_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x0000001cU)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__pub_sr_domain_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x0000001dU)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__pub_talker_decl_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x0000001eU)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_lo_r
                                                                                [
                                                                                ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w)) 
                                                                                && (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w))]
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_s_w])) 
                                                                                | ((- (IData)(
                                                                                (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] 
                                                                                >> 0x0000001fU))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__pub_src_sid_hi_r
                                                                                [
                                                                                ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w)) 
                                                                                && (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w))]
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_s_w])) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_lo_r
                                                                                [
                                                                                ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w)) 
                                                                                && (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w))]
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_k_w])) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 1U)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__pub_sid_hi_r
                                                                                [
                                                                                ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w)) 
                                                                                && (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w))]
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_k_w])) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 2U)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__pub_binding_r
                                                                                [
                                                                                ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w)) 
                                                                                && (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w))]
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_k_w])) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 3U)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                                                                && vlSelfRef.__PVT__KL_mbx__DOT__face_f_ctrl_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 4U)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__face_f_entity_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 5U)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__face_f_clock_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 6U)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__face_f_aecp_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 7U)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__face_f_restore_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 8U)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__face_f_nvm_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 9U)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_173__mbx_place_f)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x0000000aU)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__face_ctr_req_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x0000000bU)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__face_ctr_word_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x0000000cU)))) 
                                                                                & (((vlSelfRef.KL_mbx__DOT____VlemCall_174__mbx_place_f 
                                                                                | vlSelfRef.KL_mbx__DOT____VlemCall_175__mbx_place_f) 
                                                                                | vlSelfRef.KL_mbx__DOT____VlemCall_176__mbx_place_f) 
                                                                                | vlSelfRef.KL_mbx__DOT____VlemCall_177__mbx_place_f))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x0000000dU)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__ctr_data_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x0000000eU)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__face_amap_req_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x0000000fU)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__face_amap_page_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x00000010U)))) 
                                                                                & (((vlSelfRef.KL_mbx__DOT____VlemCall_178__mbx_place_f 
                                                                                | vlSelfRef.KL_mbx__DOT____VlemCall_179__mbx_place_f) 
                                                                                | vlSelfRef.KL_mbx__DOT____VlemCall_180__mbx_place_f) 
                                                                                | vlSelfRef.KL_mbx__DOT____VlemCall_181__mbx_place_f))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x00000011U)))) 
                                                                                & (IData)(
                                                                                ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__amap_data_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0ULL)))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x00000012U)))) 
                                                                                & (IData)(
                                                                                (((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__amap_data_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0ULL) 
                                                                                >> 0x20U)))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x00000013U)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__face_edit_req_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x00000014U)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__face_edit_beat_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x00000015U)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__face_edit_record_lo_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x00000016U)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__face_edit_record_hi_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x00000017U)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__face_edit_value_lo_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x00000018U)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__face_edit_value_hi_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x00000019U)))) 
                                                                                & (((vlSelfRef.KL_mbx__DOT____VlemCall_182__mbx_place_f 
                                                                                | vlSelfRef.KL_mbx__DOT____VlemCall_183__mbx_place_f) 
                                                                                | vlSelfRef.KL_mbx__DOT____VlemCall_184__mbx_place_f) 
                                                                                | vlSelfRef.KL_mbx__DOT____VlemCall_185__mbx_place_f))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x0000001aU)))) 
                                                                                & (IData)(
                                                                                ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__edit_data_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0ULL)))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x0000001bU)))) 
                                                                                & (IData)(
                                                                                (((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__edit_data_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0ULL) 
                                                                                >> 0x20U)))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x0000001cU)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__face_gsi_req_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x0000001dU)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__face_gsi_sel_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x0000001eU)))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__face_gsi_prop_lo_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] 
                                                                                >> 0x0000001fU))) 
                                                                                & ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__face_gsi_prop_hi_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0U))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]))) 
                                                                                & (((vlSelfRef.KL_mbx__DOT____VlemCall_186__mbx_place_f 
                                                                                | vlSelfRef.KL_mbx__DOT____VlemCall_187__mbx_place_f) 
                                                                                | vlSelfRef.KL_mbx__DOT____VlemCall_188__mbx_place_f) 
                                                                                | vlSelfRef.KL_mbx__DOT____VlemCall_189__mbx_place_f))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 1U)))) 
                                                                                & (IData)(
                                                                                ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__gsi_data_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0ULL)))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 2U)))) 
                                                                                & (IData)(
                                                                                (((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))
                                                                                 ? vlSelfRef.__PVT__KL_mbx__DOT__gsi_data_r
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w]
                                                                                 : 0ULL) 
                                                                                >> 0x20U)))) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 3U)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__face_f_pt_offset_r
                                                                                [
                                                                                ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                                                                && (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))]
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_s_w])) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 4U)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_lo_r
                                                                                [
                                                                                ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                                                                && (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))]
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_s_w])) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 5U)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_out_hi_r
                                                                                [
                                                                                ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                                                                && (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))]
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_s_w])) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 6U)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__face_f_src_valid_r
                                                                                [
                                                                                ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                                                                && (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))]
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_s_w])) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 7U)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_lo_r
                                                                                [
                                                                                ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                                                                && (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))]
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_k_w])) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 8U)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__face_f_fmt_in_hi_r
                                                                                [
                                                                                ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                                                                && (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))]
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_k_w])) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 9U)))) 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__face_f_snk_valid_r
                                                                                [
                                                                                ((0U 
                                                                                >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                                                                && (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))]
                                                                                [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_k_w])) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x0000000aU)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_190__mbx_place_f)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x0000000bU)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_191__mbx_place_f)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x0000000cU)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_192__mbx_place_f)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x0000000dU)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_193__mbx_place_f)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x0000000eU)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_194__mbx_place_f)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x0000000fU)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_195__mbx_place_f)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x00000010U)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_196__mbx_place_f)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x00000011U)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_197__mbx_place_f)) 
                                                                                | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x00000012U)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_198__mbx_place_f)) 
                                                                               | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x00000013U)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_199__mbx_place_f)) 
                                                                              | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x00000014U)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_200__mbx_place_f)) 
                                                                             | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x00000015U)))) 
                                                                                & vlSelfRef.KL_mbx__DOT____VlemCall_201__mbx_place_f)) 
                                                                            | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x00000016U)))) 
                                                                               & vlSelfRef.KL_mbx__DOT____VlemCall_202__mbx_place_f)) 
                                                                           | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x00000017U)))) 
                                                                              & vlSelfRef.KL_mbx__DOT____VlemCall_203__mbx_place_f)) 
                                                                          | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x00000018U)))) 
                                                                             & vlSelfRef.KL_mbx__DOT____VlemCall_204__mbx_place_f)) 
                                                                         | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x00000019U)))) 
                                                                            & vlSelfRef.KL_mbx__DOT____VlemCall_205__mbx_place_f)) 
                                                                        | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x0000001aU)))) 
                                                                           & vlSelfRef.KL_mbx__DOT____VlemCall_206__mbx_place_f)) 
                                                                       | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x0000001bU)))) 
                                                                          & vlSelfRef.KL_mbx__DOT____VlemCall_207__mbx_place_f)) 
                                                                      | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x0000001cU)))) 
                                                                         & vlSelfRef.KL_mbx__DOT____VlemCall_208__mbx_place_f)) 
                                                                     | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x0000001dU)))) 
                                                                        & vlSelfRef.KL_mbx__DOT____VlemCall_209__mbx_place_f)) 
                                                                    | ((- (IData)(
                                                                                (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x0000001eU)))) 
                                                                       & vlSelfRef.KL_mbx__DOT____VlemCall_210__mbx_place_f)) 
                                                                   | ((- (IData)(
                                                                                (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] 
                                                                                >> 0x0000001fU))) 
                                                                      & vlSelfRef.KL_mbx__DOT____VlemCall_211__mbx_place_f)) 
                                                                  | ((- (IData)(
                                                                                (1U 
                                                                                & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U]))) 
                                                                     & vlSelfRef.KL_mbx__DOT____VlemCall_212__mbx_place_f)) 
                                                                 | ((- (IData)(
                                                                               (1U 
                                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] 
                                                                                >> 1U)))) 
                                                                    & vlSelfRef.KL_mbx__DOT____VlemCall_213__mbx_place_f)) 
                                                                | ((- (IData)(
                                                                              (1U 
                                                                               & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] 
                                                                                >> 2U)))) 
                                                                   & vlSelfRef.KL_mbx__DOT____VlemCall_214__mbx_place_f)) 
                                                               | ((- (IData)(
                                                                             (1U 
                                                                              & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] 
                                                                                >> 3U)))) 
                                                                  & KL_mbx__DOT____VlemCall_215__mbx_place_f)) 
                                                              | ((- (IData)(
                                                                            (1U 
                                                                             & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] 
                                                                                >> 4U)))) 
                                                                 & KL_mbx__DOT____VlemCall_216__mbx_place_f)) 
                                                             | ((- (IData)(
                                                                           (1U 
                                                                            & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] 
                                                                               >> 5U)))) 
                                                                & KL_mbx__DOT____VlemCall_217__mbx_place_f)) 
                                                            | ((- (IData)(
                                                                          (1U 
                                                                           & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] 
                                                                              >> 6U)))) 
                                                               & KL_mbx__DOT____VlemCall_218__mbx_place_f)) 
                                                           | ((- (IData)(
                                                                         (1U 
                                                                          & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] 
                                                                             >> 7U)))) 
                                                              & KL_mbx__DOT____VlemCall_219__mbx_place_f)) 
                                                          | ((- (IData)(
                                                                        (1U 
                                                                         & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] 
                                                                            >> 8U)))) 
                                                             & KL_mbx__DOT____VlemCall_220__mbx_place_f)) 
                                                         | ((- (IData)(
                                                                       (1U 
                                                                        & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] 
                                                                           >> 9U)))) 
                                                            & KL_mbx__DOT____VlemCall_221__mbx_place_f)) 
                                                        | ((- (IData)(
                                                                      (1U 
                                                                       & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] 
                                                                          >> 0x0000000aU)))) 
                                                           & KL_mbx__DOT____VlemCall_222__mbx_place_f)) 
                                                       | ((- (IData)(
                                                                     (1U 
                                                                      & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] 
                                                                         >> 0x0000000bU)))) 
                                                          & KL_mbx__DOT____VlemCall_223__mbx_place_f)) 
                                                      | ((- (IData)(
                                                                    (1U 
                                                                     & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] 
                                                                        >> 0x0000000cU)))) 
                                                         & KL_mbx__DOT____VlemCall_224__mbx_place_f)) 
                                                     | ((- (IData)(
                                                                   (1U 
                                                                    & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] 
                                                                       >> 0x0000000dU)))) 
                                                        & KL_mbx__DOT____VlemCall_225__mbx_place_f)) 
                                                    | ((- (IData)(
                                                                  (1U 
                                                                   & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] 
                                                                      >> 0x0000000eU)))) 
                                                       & KL_mbx__DOT____VlemCall_226__mbx_place_f)) 
                                                   | ((- (IData)(
                                                                 (1U 
                                                                  & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] 
                                                                     >> 0x0000000fU)))) 
                                                      & KL_mbx__DOT____VlemCall_227__mbx_place_f)) 
                                                  | ((- (IData)(
                                                                (1U 
                                                                 & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] 
                                                                    >> 0x00000010U)))) 
                                                     & KL_mbx__DOT____VlemCall_228__mbx_place_f)) 
                                                 | ((- (IData)(
                                                               (1U 
                                                                & (vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] 
                                                                   >> 0x00000011U)))) 
                                                    & KL_mbx__DOT____VlemCall_229__mbx_place_f));
}

void Vsim_sim___ico_comb__TOP__sim__4(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___ico_comb__TOP__sim__4\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dtype = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dindex = 0U;
    if ((0x10U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dtype = 5U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dindex 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w;
    }
    if (((0x10U <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w)) 
         & (0x20U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dtype = 6U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dindex 
            = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w) 
               - (IData)(0x00000010U));
    }
    if (((0x20U <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w)) 
         & (0x21U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dtype = 9U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dindex 
            = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w) 
               - (IData)(0x00000020U));
    }
    if (((0x21U <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w)) 
         & (0x22U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dtype = 0x00000024U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dindex 
            = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w) 
               - (IData)(0x00000021U));
    }
    if ((4U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))) {
        if ((2U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))) {
            if ((1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))) {
                vlSelfRef.__Vfunc_mbx_place_f__238__value 
                    = (0x22U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w));
                vlSelfRef.__Vfunc_mbx_place_f__238__Vfuncout 
                    = (1U & vlSelfRef.__Vfunc_mbx_place_f__238__value);
                vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w2_w 
                    = vlSelfRef.__Vfunc_mbx_place_f__238__Vfuncout;
                vlSelfRef.__Vfunc_mbx_place_f__236__value 
                    = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dtype;
                vlSelfRef.KL_mbx__DOT__u_evt__DOT____VlemCall_0__mbx_place_f 
                    = (0x0000ffffU & vlSelfRef.__Vfunc_mbx_place_f__236__value);
                vlSelfRef.__Vfunc_mbx_place_f__237__value 
                    = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dindex;
                vlSelfRef.KL_mbx__DOT__u_evt__DOT____VlemCall_1__mbx_place_f 
                    = (vlSelfRef.__Vfunc_mbx_place_f__237__value 
                       << 0x00000010U);
                vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w1_w 
                    = (vlSelfRef.KL_mbx__DOT__u_evt__DOT____VlemCall_0__mbx_place_f 
                       | vlSelfRef.KL_mbx__DOT__u_evt__DOT____VlemCall_1__mbx_place_f);
            } else {
                vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w2_w = 0U;
                vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w1_w 
                    = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w))
                        ? vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__asp_cnt_r
                       [vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w]
                        : 0U);
            }
        } else {
            vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w2_w = 0U;
            vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w1_w 
                = ((1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))
                    ? ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w))
                        ? vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__avb_cnt_r
                       [vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w]
                        : 0U) : ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w))
                                  ? vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__amap_cnt_r
                                 [vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w]
                                  : 0U));
        }
    } else if ((2U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))) {
        if ((1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))) {
            vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w2_w = 0U;
            vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w1_w 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tick_cnt_r;
        } else {
            vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w2_w 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__dl_r
                [vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w];
            vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w1_w 
                = (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tag_r
                   [vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w] 
                   | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w) 
                      << 0x00000010U));
        }
    } else if ((1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w2_w 
            = (IData)((vlSymsp->TOP.mbx_gm_id >> (0x0000003fU 
                                                  & ((IData)(0x20U) 
                                                     + 
                                                     ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w) 
                                                      << 6U)))));
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w1_w 
            = (IData)(vlSymsp->TOP.mbx_gm_id);
    } else {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w2_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w1_w 
            = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w)) 
               && (1U & ((IData)(vlSymsp->TOP.mbx_link_up) 
                         >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w))));
    }
}

void Vsim_sim___ico_comb__TOP__sim__5(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___ico_comb__TOP__sim__5\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w3_w 
        = ((4U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))
            ? vlSelfRef.__PVT__KL_mbx__DOT__now_ms_r
            : ((2U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))
                ? vlSelfRef.__PVT__KL_mbx__DOT__now_ms_r
                : ((1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))
                    ? (0x000000ffU & (IData)(vlSymsp->TOP.mbx_domain))
                    : vlSelfRef.__PVT__KL_mbx__DOT__now_ms_r)));
}

void Vsim_sim___nba_sequent__TOP__sim__0(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__0\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VdlySet__storage_2__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt_ring__DOT__mem_r__v0 = 0U;
    vlSelfRef.__VdlySet__storage_1__v0 = 0U;
    vlSelfRef.__Vdly__soc_bus_errors = vlSelfRef.__PVT__soc_bus_errors;
    vlSelfRef.__Vdly__soc_tx_fifo_consume = vlSelfRef.__PVT__soc_tx_fifo_consume;
    vlSelfRef.__Vdly__soc_rx_fifo_consume = vlSelfRef.__PVT__soc_rx_fifo_consume;
    vlSelfRef.__Vdly__soc_rx_fifo_level0 = vlSelfRef.__PVT__soc_rx_fifo_level0;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r__v0 = 0U;
    vlSelfRef.__Vdly__add_devices_stimulusmailbox_ms_cnt 
        = vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_cnt;
    vlSelfRef.__Vdly__soc_tx_fifo_level0 = vlSelfRef.__PVT__soc_tx_fifo_level0;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__rec_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__rec_r__v4 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_srp_tx__DOT__mem_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_maap_tx__DOT__mem_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_aecp_tx__DOT__mem_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_acmp_tx__DOT__mem_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_adp_tx__DOT__mem_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__tag_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__tag_r__v16 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__tokens_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__tokens_r__v5 = 0U;
    vlSelfRef.__Vdly__add_devices_stimulusmailbox_waited1 
        = vlSelfRef.__PVT__add_devices_stimulusmailbox_waited1;
    vlSelfRef.__Vdly__add_devices_stimulusmailbox_waited0 
        = vlSelfRef.__PVT__add_devices_stimulusmailbox_waited0;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__ctr_epoch_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_epoch_r;
    vlSelfRef.__Vdly__ctrlmemory1_sram2_bus_ack = vlSelfRef.__PVT__ctrlmemory1_sram2_bus_ack;
    vlSelfRef.__Vdly__ctrlmemory1_sram3_bus_ack = vlSelfRef.__PVT__ctrlmemory1_sram3_bus_ack;
    vlSelfRef.__Vdly__ctrlmemory1_sram4_bus_ack = vlSelfRef.__PVT__ctrlmemory1_sram4_bus_ack;
    vlSelfRef.__VdlySet__KL_mbx__DOT__ctr_data_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__amap_data_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__gsi_data_r__v0 = 0U;
    vlSelfRef.__Vdly__ctrlmemory0_sram1_bus_ack = vlSelfRef.__PVT__ctrlmemory0_sram1_bus_ack;
    vlSelfRef.__Vdly__ctrlmemory0_sram0_bus_ack = vlSelfRef.__PVT__ctrlmemory0_sram0_bus_ack;
    vlSelfRef.__Vdly__add_devices_tx_pipe_valid_source_valid 
        = vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_valid;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__seq_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__seq_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__k_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__k_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__busy_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__busy_r;
    vlSelfRef.__VdlySet__sram_bank0__v0 = 0U;
    vlSelfRef.__VdlySet__sram_bank0__v1 = 0U;
    vlSelfRef.__VdlySet__sram_bank0__v2 = 0U;
    vlSelfRef.__VdlySet__sram_bank0__v3 = 0U;
    vlSelfRef.__VdlySet__sram_bank1__v0 = 0U;
    vlSelfRef.__VdlySet__sram_bank1__v1 = 0U;
    vlSelfRef.__VdlySet__sram_bank1__v2 = 0U;
    vlSelfRef.__VdlySet__sram_bank1__v3 = 0U;
    vlSelfRef.__VdlySet__sram_bank2__v0 = 0U;
    vlSelfRef.__VdlySet__sram_bank2__v1 = 0U;
    vlSelfRef.__VdlySet__sram_bank2__v2 = 0U;
    vlSelfRef.__VdlySet__sram_bank2__v3 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v5 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v6 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v7 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v8 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v9 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v10 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v11 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v12 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v13 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v14 = 0U;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__mismatch_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__mismatch_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__bus_err_r = vlSelfRef.__PVT__KL_mbx__DOT__bus_err_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__head_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__head_r;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__rb_mem_r__v0 = 0U;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__armed_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__armed_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__scan_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__scan_r;
    vlSelfRef.__Vdly__add_devices_rx_pipe_valid_source_valid 
        = vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_valid;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v5 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v6 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v7 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v8 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v9 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v10 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v11 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v12 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v13 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v14 = 0U;
    vlSelfRef.__Vdly__KL_mbx__DOT__now_ms_r = vlSelfRef.__PVT__KL_mbx__DOT__now_ms_r;
    vlSelfRef.__Vdly__value = vlSelfRef.__PVT__value;
    vlSelfRef.__Vdly__KL_mbx__DOT__fw_busy_r = vlSelfRef.__PVT__KL_mbx__DOT__fw_busy_r;
    vlSelfRef.__VdlySet__KL_mbx__DOT__own_mac_lo_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__own_mac_lo_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__own_mac_hi_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__own_mac_hi_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__dl_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__dl_r__v16 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_talker_decl_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_talker_decl_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_idle_slope_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_idle_slope_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_da_gate_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_da_gate_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_licence_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_licence_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_sr_domain_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_sr_domain_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__avb_cnt_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__avb_cnt_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__avb_cnt_r__v2 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__asp_cnt_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__asp_cnt_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__asp_cnt_r__v2 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__amap_cnt_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__amap_cnt_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__amap_cnt_r__v2 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__wr_head_r__v5 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__wr_head_r__v6 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__wr_head_r__v7 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__wr_head_r__v8 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__wr_head_r__v9 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v5 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v6 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v7 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v8 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v9 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v10 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v11 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v12 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v13 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v14 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v0 = 0U;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__tick_div_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tick_div_r;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_value_hi_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_value_hi_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_value_lo_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_value_lo_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_ctrl_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_ctrl_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_record_lo_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_record_lo_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_clock_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_clock_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_prop_lo_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_prop_lo_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_record_hi_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_record_hi_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_prop_hi_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_prop_hi_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_ctr_word_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_ctr_word_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_entity_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_entity_r__v1 = 0U;
}

void Vsim_sim___nba_sequent__TOP__sim__1(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__1\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_req_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_req_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_amap_req_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_amap_req_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_req_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_req_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_aecp_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_aecp_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_ctr_req_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_ctr_req_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_sel_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_sel_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_amap_page_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_amap_page_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_beat_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_beat_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_src_sid_lo_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_src_sid_lo_r__v16 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_src_sid_hi_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_src_sid_hi_r__v16 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_sid_lo_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_sid_lo_r__v16 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_sid_hi_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_sid_hi_r__v16 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_nvm_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_nvm_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_binding_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_binding_r__v16 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_restore_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_restore_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_in_hi_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_in_hi_r__v16 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_in_lo_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_in_lo_r__v16 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_snk_valid_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_snk_valid_r__v16 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_out_lo_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_out_lo_r__v16 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_out_hi_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_out_hi_r__v16 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_pt_offset_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_pt_offset_r__v16 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_src_valid_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_src_valid_r__v16 = 0U;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__tick_cnt_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tick_cnt_r;
    vlSelfRef.__Vdly__KL_mbx_dma__DOT__pend_r = vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_r;
    vlSelfRef.__VdlySet__KL_mbx_dma__DOT__buf_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx_dma__DOT__buf_r__v16 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__ctr_wait_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__ctr_wait_r__v2 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__amap_wait_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__amap_wait_r__v2 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__gsi_wait_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__gsi_wait_r__v2 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__ctr_tag_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__amap_tag_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__gsi_tag_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__ctr_tag_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__amap_tag_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__gsi_tag_r__v0 = 0U;
    vlSelfRef.__Vdly__KL_mbx__DOT__ctr_busy_r = vlSelfRef.__PVT__KL_mbx__DOT__ctr_busy_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__amap_busy_r = vlSelfRef.__PVT__KL_mbx__DOT__amap_busy_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__gsi_busy_r = vlSelfRef.__PVT__KL_mbx__DOT__gsi_busy_r;
    vlSelfRef.__VdlySet__KL_mbx__DOT__edit_wait_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__edit_wait_r__v2 = 0U;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__cp_busy_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_busy_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__owed_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r;
    vlSelfRef.__VdlySet__KL_mbx__DOT__edit_data_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__edit_tag_r__v1 = 0U;
    vlSelfRef.__Vdly__KL_mbx__DOT__edit_busy_r = vlSelfRef.__PVT__KL_mbx__DOT__edit_busy_r;
    vlSelfRef.__VdlySet__KL_mbx__DOT__rx_tail_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__rx_tail_r__v5 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__rx_tail_r__v6 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__rx_tail_r__v7 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__rx_tail_r__v8 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__rx_tail_r__v9 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__drop_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__drop_r__v5 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__drop_r__v6 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__drop_r__v7 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__drop_r__v8 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__drop_r__v9 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v5 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v6 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v7 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v8 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v9 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__edit_tag_r__v0 = 0U;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__widx_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__widx_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__hit_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hit_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__q_wr_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_wr_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__lane_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__lane_r;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__q_data_r__v4 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__q_idx_r__v4 = 0U;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__dst_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__dst_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__q_rd_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_rd_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__q_cnt_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_cnt_r;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v15 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v16 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v17 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v18 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v19 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v20 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v21 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v22 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v23 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v24 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v25 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v26 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v27 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v28 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v29 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v30 = 0U;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__st_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v0 = 0U;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__cp_k_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__cp_b_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_b_r;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_pub_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_pub_r__v5 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__tx_head_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__tx_head_r__v5 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__tx_head_r__v6 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__tx_head_r__v7 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__tx_head_r__v8 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__tx_head_r__v9 = 0U;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__cnt_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__scan_v_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_v_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__scan_c_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_c_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__best_seq_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_seq_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__best_v_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_v_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__widx_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__widx_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__left_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__left_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__lane_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__lane_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__best_ch_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__best_ch_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__ch_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__ch_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__scan_k_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__scan_k_r;
    vlSelfRef.__Vdly__KL_mbx__DOT__u_tx__DOT__st_r 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_tx__DOT__err_r__v5 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_tx__DOT__tail_r__v5 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_tx__DOT__tail_r__v6 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_tx__DOT__tail_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v5 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v6 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v7 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v8 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v9 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v10 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v11 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v12 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v13 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v14 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_maap_rx__DOT__mem_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_aecp_rx__DOT__mem_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_acmp_rx__DOT__mem_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_adp_rx__DOT__mem_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__u_srp_rx__DOT__mem_r__v0 = 0U;
    vlSelfRef.__Vdly__KL_mbx_dma__DOT__index_r = vlSelfRef.__PVT__KL_mbx_dma__DOT__index_r;
    vlSelfRef.__Vdly__KL_mbx_dma__DOT__rerr_r = vlSelfRef.__PVT__KL_mbx_dma__DOT__rerr_r;
    vlSelfRef.__Vdly__KL_mbx_dma__DOT__count_r = vlSelfRef.__PVT__KL_mbx_dma__DOT__count_r;
    vlSelfRef.__Vdly__KL_mbx_dma__DOT__chunk_r = vlSelfRef.__PVT__KL_mbx_dma__DOT__chunk_r;
    vlSelfRef.__VdlySet__KL_mbx__DOT__gm_hi_snap_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__gm_hi_snap_r__v1 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__domain_snap_r__v0 = 0U;
    vlSelfRef.__VdlySet__KL_mbx__DOT__domain_snap_r__v1 = 0U;
}

void Vsim_sim___nba_sequent__TOP__sim__2(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__2\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__Vdly__KL_mbx_dma__DOT__state_r = vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r;
    if (((IData)(vlSymsp->TOP.serial_sink_valid) & (IData)(vlSymsp->TOP.serial_sink_ready))) {
        vlSelfRef.__VdlyVal__storage_2__v0 = vlSymsp->TOP.serial_sink_data;
        vlSelfRef.__VdlyDim0__storage_2__v0 = vlSelfRef.__PVT__soc_rx_fifo_wrport_adr;
        vlSelfRef.__VdlySet__storage_2__v0 = 1U;
        vlSelfRef.__PVT__soc_rx_fifo_produce = (0x0000000fU 
                                                & ((IData)(1U) 
                                                   + (IData)(vlSelfRef.__PVT__soc_rx_fifo_produce)));
        if ((1U & (~ (IData)(vlSelfRef.__PVT__soc_rx_fifo_do_read)))) {
            vlSelfRef.__Vdly__soc_rx_fifo_level0 = 
                (0x0000001fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__soc_rx_fifo_level0)));
        }
    } else if (vlSelfRef.__PVT__soc_rx_fifo_do_read) {
        vlSelfRef.__Vdly__soc_rx_fifo_level0 = (0x0000001fU 
                                                & ((IData)(vlSelfRef.__PVT__soc_rx_fifo_level0) 
                                                   - (IData)(1U)));
    }
    if (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__busy_r) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt_ring__DOT__mem_r__v0 
            = vlSelfRef.KL_mbx__DOT__u_evt__DOT__wr_data_o;
        vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_evt_ring__DOT__mem_r__v0 
            = vlSelfRef.KL_mbx__DOT__u_evt__DOT__wr_addr_o;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt_ring__DOT__mem_r__v0 = 1U;
    }
    if (((IData)(vlSelfRef.__PVT__soc_rxtx_re) & (0x10U 
                                                  != (IData)(vlSelfRef.__PVT__soc_tx_fifo_level0)))) {
        vlSelfRef.__VdlyVal__storage_1__v0 = (0x000000ffU 
                                              & vlSelfRef.__PVT__builder_interface1_dat_w);
        vlSelfRef.__VdlyDim0__storage_1__v0 = vlSelfRef.__PVT__soc_tx_fifo_wrport_adr;
        vlSelfRef.__VdlySet__storage_1__v0 = 1U;
        vlSelfRef.__PVT__soc_tx_fifo_produce = (0x0000000fU 
                                                & ((IData)(1U) 
                                                   + (IData)(vlSelfRef.__PVT__soc_tx_fifo_produce)));
    }
    if ((0xffffffffU != vlSelfRef.__PVT__soc_bus_errors)) {
        if (vlSelfRef.__PVT__builder_error) {
            vlSelfRef.__Vdly__soc_bus_errors = ((IData)(1U) 
                                                + vlSelfRef.__PVT__soc_bus_errors);
        }
    }
    if (vlSelfRef.__PVT__soc_tx_fifo_do_read) {
        vlSelfRef.__Vdly__soc_tx_fifo_consume = (0x0000000fU 
                                                 & ((IData)(1U) 
                                                    + (IData)(vlSelfRef.__PVT__soc_tx_fifo_consume)));
    }
    if (vlSelfRef.__PVT__soc_rx_fifo_do_read) {
        vlSelfRef.__Vdly__soc_rx_fifo_consume = (0x0000000fU 
                                                 & ((IData)(1U) 
                                                    + (IData)(vlSelfRef.__PVT__soc_rx_fifo_consume)));
    }
    if (vlSelfRef.__PVT__add_devices_mmap_wait) {
        if ((0U != (IData)(vlSelfRef.__PVT__add_devices_mmap_count))) {
            vlSelfRef.__PVT__add_devices_mmap_count 
                = (0x000001ffU & ((IData)(vlSelfRef.__PVT__add_devices_mmap_count) 
                                  - (IData)(1U)));
        }
    } else {
        vlSelfRef.__PVT__add_devices_mmap_count = 0x0100U;
    }
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__Vdly__soc_bus_errors = 0U;
        vlSelfRef.__Vdly__soc_tx_fifo_consume = 0U;
        vlSelfRef.__Vdly__soc_rx_fifo_consume = 0U;
        vlSelfRef.__PVT__add_devices_mmap_count = 0x0100U;
        vlSelfRef.__PVT__soc_rx_fifo_produce = 0U;
        vlSelfRef.__PVT__soc_tx_fifo_produce = 0U;
    }
}

void Vsim_sim___nba_sequent__TOP__sim__3(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__3\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__Vdly__soc_rx_fifo_level0 = 0U;
    }
    if ((1U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_sh_w))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_d_w;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v0 = 1U;
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v1 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r[0U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v2 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r[1U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v3 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r[2U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v4 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r[3U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v5 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r[4U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v6 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r[5U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r__v7 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r[6U];
    }
    if ((2U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_sh_w))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_d_w;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v0 = 1U;
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v1 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r[0U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v2 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r[1U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v3 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r[2U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v4 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r[3U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v5 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r[4U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v6 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r[5U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r__v7 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r[6U];
    }
    if ((4U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_sh_w))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_d_w;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v0 = 1U;
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v1 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r[0U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v2 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r[1U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v3 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r[2U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v4 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r[3U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v5 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r[4U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v6 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r[5U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r__v7 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r[6U];
    }
    if ((8U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_sh_w))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_d_w;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v0 = 1U;
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v1 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r[0U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v2 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r[1U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v3 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r[2U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v4 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r[3U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v5 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r[4U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v6 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r[5U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r__v7 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r[6U];
    }
    if ((0x00000010U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_sh_w))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_d_w;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v0 = 1U;
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v1 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r[0U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v2 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r[1U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v3 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r[2U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v4 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r[3U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v5 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r[4U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v6 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r[5U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r__v7 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r[6U];
    }
    if ((0x00000020U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_sh_w))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_d_w;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v0 = 1U;
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v1 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r[0U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v2 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r[1U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v3 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r[2U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v4 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r[3U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v5 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r[4U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v6 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r[5U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r__v7 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r[6U];
    }
    if ((0x00000040U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_sh_w))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_d_w;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v0 = 1U;
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v1 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r[0U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v2 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r[1U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v3 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r[2U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v4 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r[3U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v5 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r[4U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v6 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r[5U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r__v7 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r[6U];
    }
    if ((0x00000080U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_sh_w))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_d_w;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v0 = 1U;
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v1 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r[0U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v2 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r[1U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v3 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r[2U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v4 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r[3U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v5 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r[4U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v6 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r[5U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r__v7 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r[6U];
    }
    if ((0x00000100U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_sh_w))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_d_w;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v0 = 1U;
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v1 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r[0U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v2 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r[1U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v3 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r[2U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v4 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r[3U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v5 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r[4U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v6 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r[5U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r__v7 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r[6U];
    }
    if ((0x00000200U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_sh_w))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_d_w;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v0 = 1U;
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v1 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r[0U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v2 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r[1U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v3 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r[2U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v4 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r[3U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v5 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r[4U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v6 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r[5U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r__v7 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r[6U];
    }
    if ((0x00000400U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_sh_w))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_d_w;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v0 = 1U;
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v1 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r[0U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v2 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r[1U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v3 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r[2U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v4 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r[3U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v5 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r[4U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v6 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r[5U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r__v7 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r[6U];
    }
}

void Vsim_sim___nba_sequent__TOP__sim__4(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__4\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((0x00000800U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_sh_w))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_d_w;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v0 = 1U;
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v1 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r[0U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v2 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r[1U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v3 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r[2U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v4 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r[3U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v5 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r[4U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v6 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r[5U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r__v7 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r[6U];
    }
    if ((0x00001000U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_sh_w))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_d_w;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v0 = 1U;
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v1 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r[0U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v2 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r[1U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v3 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r[2U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v4 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r[3U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v5 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r[4U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v6 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r[5U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r__v7 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r[6U];
    }
    if ((0x00002000U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_sh_w))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_d_w;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v0 = 1U;
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v1 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r[0U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v2 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r[1U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v3 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r[2U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v4 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r[3U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v5 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r[4U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v6 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r[5U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r__v7 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r[6U];
    }
    if ((0x00004000U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_sh_w))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_d_w;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v0 = 1U;
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v1 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r[0U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v2 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r[1U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v3 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r[2U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v4 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r[3U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v5 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r[4U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v6 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r[5U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r__v7 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r[6U];
    }
    if ((0x00008000U & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_sh_w))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_d_w;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r__v0 = 1U;
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r__v1 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r[0U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r__v2 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r[1U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r__v3 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r[2U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r__v4 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r[3U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r__v5 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r[4U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r__v6 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r[5U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r__v7 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r[6U];
    }
    if (((IData)(vlSelfRef.__PVT__soc_rxtx_re) & (0x10U 
                                                  != (IData)(vlSelfRef.__PVT__soc_tx_fifo_level0)))) {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__soc_tx_fifo_do_read)))) {
            vlSelfRef.__Vdly__soc_tx_fifo_level0 = 
                (0x0000001fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__soc_tx_fifo_level0)));
        }
    } else if (vlSelfRef.__PVT__soc_tx_fifo_do_read) {
        vlSelfRef.__Vdly__soc_tx_fifo_level0 = (0x0000001fU 
                                                & ((IData)(vlSelfRef.__PVT__soc_tx_fifo_level0) 
                                                   - (IData)(1U)));
    }
    if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
         & ((0x5000U <= ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                         << 2U)) & (0x5800U > ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                               << 2U))))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_srp_tx__DOT__mem_r__v0 
            = vlSelfRef.__PVT__add_devices_ctrlmailboxdma10;
        vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_srp_tx__DOT__mem_r__v0 
            = (0x000001ffU & ((((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                << 2U) - (IData)(0x5000U)) 
                              >> 2U));
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_srp_tx__DOT__mem_r__v0 = 1U;
    }
    if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
         & ((0x3200U <= ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                         << 2U)) & (0x3400U > ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                               << 2U))))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_maap_tx__DOT__mem_r__v0 
            = vlSelfRef.__PVT__add_devices_ctrlmailboxdma10;
        vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_maap_tx__DOT__mem_r__v0 
            = (0x0000007fU & ((((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                << 2U) - (IData)(0x3200U)) 
                              >> 2U));
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_maap_tx__DOT__mem_r__v0 = 1U;
    }
    if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
         & ((0x2800U <= ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                         << 2U)) & (0x3000U > ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                               << 2U))))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_aecp_tx__DOT__mem_r__v0 
            = vlSelfRef.__PVT__add_devices_ctrlmailboxdma10;
        vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_aecp_tx__DOT__mem_r__v0 
            = (0x000001ffU & ((((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                << 2U) - (IData)(0x2800U)) 
                              >> 2U));
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_aecp_tx__DOT__mem_r__v0 = 1U;
    }
    if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
         & ((0x1c00U <= ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                         << 2U)) & (0x2000U > ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                               << 2U))))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_acmp_tx__DOT__mem_r__v0 
            = vlSelfRef.__PVT__add_devices_ctrlmailboxdma10;
        vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_acmp_tx__DOT__mem_r__v0 
            = (0x000000ffU & ((((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                << 2U) - (IData)(0x1c00U)) 
                              >> 2U));
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_acmp_tx__DOT__mem_r__v0 = 1U;
    }
    if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
         & ((0x1400U <= ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                         << 2U)) & (0x1600U > ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                               << 2U))))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_adp_tx__DOT__mem_r__v0 
            = vlSelfRef.__PVT__add_devices_ctrlmailboxdma10;
        vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_adp_tx__DOT__mem_r__v0 
            = (0x0000007fU & ((((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                << 2U) - (IData)(0x1400U)) 
                              >> 2U));
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_adp_tx__DOT__mem_r__v0 = 1U;
    }
    if (vlSelfRef.__PVT__KL_mbx__DOT__edit_busy_r) {
        if ((0x3fU != (IData)(vlSelfRef.__PVT__add_devices_stimulusmailbox_waited1))) {
            vlSelfRef.__Vdly__add_devices_stimulusmailbox_waited1 
                = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__add_devices_stimulusmailbox_waited1)));
        }
    } else {
        vlSelfRef.__Vdly__add_devices_stimulusmailbox_waited1 = 0U;
    }
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__Vdly__soc_tx_fifo_level0 = 0U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__rec_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__tag_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__tokens_r__v0 = 1U;
        vlSelfRef.__Vdly__add_devices_stimulusmailbox_waited1 = 0U;
    } else {
        if (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__start_w) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__rec_r__v4 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w0_w;
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__rec_r__v4 = 1U;
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__rec_r__v5 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w1_w;
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__rec_r__v6 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w2_w;
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__rec_r__v7 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__w3_w;
        }
        if (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__cmd_ok_w) {
            if ((1U == (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                        >> 0x0000001eU))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__tag_r__v16 
                    = (0x0000ffffU & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                                      >> 8U));
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_evt__DOT__tag_r__v16 
                    = (0x0000000fU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10);
                vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__tag_r__v16 = 1U;
            }
        }
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__tokens_r__v5 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_nx_w[0U];
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__tokens_r__v5 = 1U;
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__tokens_r__v6 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_nx_w[1U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__tokens_r__v7 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_nx_w[2U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__tokens_r__v8 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_nx_w[3U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__tokens_r__v9 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_nx_w[4U];
    }
    if (vlSelfRef.__PVT__KL_mbx__DOT__fw_busy_r) {
        if ((0x40U != (IData)(vlSelfRef.__PVT__add_devices_stimulusmailbox_waited0))) {
            vlSelfRef.__Vdly__add_devices_stimulusmailbox_waited0 
                = (0x0000007fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__add_devices_stimulusmailbox_waited0)));
        }
    } else {
        vlSelfRef.__Vdly__add_devices_stimulusmailbox_waited0 = 0U;
    }
}

void Vsim_sim___nba_sequent__TOP__sim__5(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__5\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__Vdly__add_devices_stimulusmailbox_waited0 = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__ctr_epoch_r = 0U;
    } else {
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r 
            = ((0xfffeU & (IData)(vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r)) 
               | (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cmp_w)
                         ? (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w) 
                             & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eq_w)) 
                            & ((0x0012U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                               | (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r)))
                         : ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                            & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w)))));
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r 
            = ((0xfffdU & (IData)(vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r)) 
               | (2U & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cmp_w)
                          ? ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w) 
                               & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eq_w)) 
                              >> 1U) & ((0x0012U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                                        | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                           >> 1U)))
                          : (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                              & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w)) 
                             >> 1U)) << 1U)));
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r 
            = ((0xfffbU & (IData)(vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r)) 
               | (4U & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cmp_w)
                          ? ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w) 
                               & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eq_w)) 
                              >> 2U) & ((0x0012U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                                        | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                           >> 2U)))
                          : (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                              & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w)) 
                             >> 2U)) << 2U)));
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r 
            = ((0xfff7U & (IData)(vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r)) 
               | (8U & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cmp_w)
                          ? ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w) 
                               & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eq_w)) 
                              >> 3U) & ((0x0012U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                                        | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                           >> 3U)))
                          : (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                              & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w)) 
                             >> 3U)) << 3U)));
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r 
            = ((0xffefU & (IData)(vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r)) 
               | (0x00000010U & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cmp_w)
                                   ? ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w) 
                                        & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eq_w)) 
                                       >> 4U) & ((0x0012U 
                                                  == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                                                 | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                                    >> 4U)))
                                   : (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w)) 
                                      >> 4U)) << 4U)));
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r 
            = ((0xffdfU & (IData)(vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r)) 
               | (0x00000020U & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cmp_w)
                                   ? ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w) 
                                        & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eq_w)) 
                                       >> 5U) & ((0x0012U 
                                                  == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                                                 | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                                    >> 5U)))
                                   : (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w)) 
                                      >> 5U)) << 5U)));
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r 
            = ((0xffbfU & (IData)(vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r)) 
               | (0x00000040U & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cmp_w)
                                   ? ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w) 
                                        & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eq_w)) 
                                       >> 6U) & ((0x0012U 
                                                  == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                                                 | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                                    >> 6U)))
                                   : (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w)) 
                                      >> 6U)) << 6U)));
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r 
            = ((0xff7fU & (IData)(vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r)) 
               | (0x00000080U & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cmp_w)
                                   ? ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w) 
                                        & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eq_w)) 
                                       >> 7U) & ((0x0012U 
                                                  == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                                                 | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                                    >> 7U)))
                                   : (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w)) 
                                      >> 7U)) << 7U)));
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r 
            = ((0xfeffU & (IData)(vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r)) 
               | (0x00000100U & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cmp_w)
                                   ? ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w) 
                                        & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eq_w)) 
                                       >> 8U) & ((0x0012U 
                                                  == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                                                 | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                                    >> 8U)))
                                   : (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w)) 
                                      >> 8U)) << 8U)));
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r 
            = ((0xfdffU & (IData)(vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r)) 
               | (0x00000200U & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cmp_w)
                                   ? ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w) 
                                        & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eq_w)) 
                                       >> 9U) & ((0x0012U 
                                                  == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                                                 | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                                    >> 9U)))
                                   : (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w)) 
                                      >> 9U)) << 9U)));
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r 
            = ((0xfbffU & (IData)(vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r)) 
               | (0x00000400U & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cmp_w)
                                   ? ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w) 
                                        & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eq_w)) 
                                       >> 0x0aU) & 
                                      ((0x0012U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                                       | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                          >> 0x0aU)))
                                   : (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w)) 
                                      >> 0x0aU)) << 0x0000000aU)));
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r 
            = ((0xf7ffU & (IData)(vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r)) 
               | (0x00000800U & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cmp_w)
                                   ? ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w) 
                                        & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eq_w)) 
                                       >> 0x0bU) & 
                                      ((0x0012U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                                       | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                          >> 0x0bU)))
                                   : (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w)) 
                                      >> 0x0bU)) << 0x0000000bU)));
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r 
            = ((0xefffU & (IData)(vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r)) 
               | (0x00001000U & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cmp_w)
                                   ? ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w) 
                                        & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eq_w)) 
                                       >> 0x0cU) & 
                                      ((0x0012U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                                       | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                          >> 0x0cU)))
                                   : (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w)) 
                                      >> 0x0cU)) << 0x0000000cU)));
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r 
            = ((0xdfffU & (IData)(vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r)) 
               | (0x00002000U & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cmp_w)
                                   ? ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w) 
                                        & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eq_w)) 
                                       >> 0x0dU) & 
                                      ((0x0012U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                                       | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                          >> 0x0dU)))
                                   : (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w)) 
                                      >> 0x0dU)) << 0x0000000dU)));
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r 
            = ((0xbfffU & (IData)(vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r)) 
               | (0x00004000U & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cmp_w)
                                   ? ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w) 
                                        & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eq_w)) 
                                       >> 0x0eU) & 
                                      ((0x0012U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                                       | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                          >> 0x0eU)))
                                   : (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w)) 
                                      >> 0x0eU)) << 0x0000000eU)));
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r 
            = ((0x7fffU & (IData)(vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__match_r)) 
               | (0x00008000U & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cmp_w)
                                   ? ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w) 
                                        & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eq_w)) 
                                       >> 0x0fU) & 
                                      ((0x0012U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
                                       | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                          >> 0x0fU)))
                                   : (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w)) 
                                      >> 0x0fU)) << 0x0000000fU)));
        if (vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) {
            vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__ctr_epoch_r 
                = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_roll_w)
                    ? 0U : (0x0000ffffU & ((IData)(1U) 
                                           + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_epoch_r))));
        }
    }
    if (vlSelfRef.__PVT__builder_litespi_grant) {
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_request) 
                      >> 1U)))) {
            if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_request))) {
                vlSelfRef.__PVT__builder_litespi_grant = 0U;
            }
        }
    } else if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_litespi_request)))) {
        if ((2U & (IData)(vlSelfRef.__PVT__builder_litespi_request))) {
            vlSelfRef.__PVT__builder_litespi_grant = 1U;
        }
    }
}
