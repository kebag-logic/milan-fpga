// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim_sim___nba_sequent__TOP__sim__43(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__43\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __Vfunc_mbx_place_f__177__value;
    __Vfunc_mbx_place_f__177__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__178__value;
    __Vfunc_mbx_place_f__178__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__179__value;
    __Vfunc_mbx_place_f__179__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__180__value;
    __Vfunc_mbx_place_f__180__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__181__value;
    __Vfunc_mbx_place_f__181__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__182__value;
    __Vfunc_mbx_place_f__182__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__183__value;
    __Vfunc_mbx_place_f__183__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__184__value;
    __Vfunc_mbx_place_f__184__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__185__value;
    __Vfunc_mbx_place_f__185__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__186__value;
    __Vfunc_mbx_place_f__186__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__187__value;
    __Vfunc_mbx_place_f__187__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__188__value;
    __Vfunc_mbx_place_f__188__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__189__value;
    __Vfunc_mbx_place_f__189__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__190__value;
    __Vfunc_mbx_place_f__190__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__191__value;
    __Vfunc_mbx_place_f__191__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__192__value;
    __Vfunc_mbx_place_f__192__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__193__value;
    __Vfunc_mbx_place_f__193__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__194__value;
    __Vfunc_mbx_place_f__194__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__195__value;
    __Vfunc_mbx_place_f__195__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__196__value;
    __Vfunc_mbx_place_f__196__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__197__value;
    __Vfunc_mbx_place_f__197__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__198__value;
    __Vfunc_mbx_place_f__198__value = 0;
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
    // Body
    vlSelfRef.KL_mbx__DOT____VlemCall_176__mbx_place_f 
        = (4U & (vlSelfRef.__Vfunc_mbx_place_f__176__value 
                 << 2U));
    if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))) {
        __Vfunc_mbx_place_f__177__value = vlSelfRef.__PVT__KL_mbx__DOT__ctr_tag_r
            [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w];
        __Vfunc_mbx_place_f__181__value = vlSelfRef.__PVT__KL_mbx__DOT__amap_tag_r
            [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w];
        __Vfunc_mbx_place_f__185__value = vlSelfRef.__PVT__KL_mbx__DOT__edit_tag_r
            [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w];
        __Vfunc_mbx_place_f__189__value = vlSelfRef.__PVT__KL_mbx__DOT__gsi_tag_r
            [vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w];
    } else {
        __Vfunc_mbx_place_f__177__value = 0U;
        __Vfunc_mbx_place_f__181__value = 0U;
        __Vfunc_mbx_place_f__185__value = 0U;
        __Vfunc_mbx_place_f__189__value = 0U;
    }
    vlSelfRef.KL_mbx__DOT____VlemCall_177__mbx_place_f 
        = (0x00000f00U & (__Vfunc_mbx_place_f__177__value 
                          << 8U));
    __Vfunc_mbx_place_f__178__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__amap_busy_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_178__mbx_place_f 
        = (1U & __Vfunc_mbx_place_f__178__value);
    __Vfunc_mbx_place_f__179__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__amap_done_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_179__mbx_place_f 
        = (2U & (__Vfunc_mbx_place_f__179__value << 1U));
    __Vfunc_mbx_place_f__180__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__amap_tmo_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_180__mbx_place_f 
        = (4U & (__Vfunc_mbx_place_f__180__value << 2U));
    vlSelfRef.KL_mbx__DOT____VlemCall_181__mbx_place_f 
        = (0x00000f00U & (__Vfunc_mbx_place_f__181__value 
                          << 8U));
    __Vfunc_mbx_place_f__182__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__edit_busy_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_182__mbx_place_f 
        = (1U & __Vfunc_mbx_place_f__182__value);
    __Vfunc_mbx_place_f__183__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__edit_done_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_183__mbx_place_f 
        = (2U & (__Vfunc_mbx_place_f__183__value << 1U));
    __Vfunc_mbx_place_f__184__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__edit_tmo_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_184__mbx_place_f 
        = (4U & (__Vfunc_mbx_place_f__184__value << 2U));
    vlSelfRef.KL_mbx__DOT____VlemCall_185__mbx_place_f 
        = (0x00000f00U & (__Vfunc_mbx_place_f__185__value 
                          << 8U));
    __Vfunc_mbx_place_f__186__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__gsi_busy_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_186__mbx_place_f 
        = (1U & __Vfunc_mbx_place_f__186__value);
    __Vfunc_mbx_place_f__187__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__gsi_done_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_187__mbx_place_f 
        = (2U & (__Vfunc_mbx_place_f__187__value << 1U));
    __Vfunc_mbx_place_f__188__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__gsi_tmo_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_188__mbx_place_f 
        = (4U & (__Vfunc_mbx_place_f__188__value << 2U));
    vlSelfRef.KL_mbx__DOT____VlemCall_189__mbx_place_f 
        = (0x00000f00U & (__Vfunc_mbx_place_f__189__value 
                          << 8U));
    __Vfunc_mbx_place_f__190__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__rx_head_w[0U]);
    vlSelfRef.KL_mbx__DOT____VlemCall_190__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__190__value);
    __Vfunc_mbx_place_f__191__value = vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[0U];
    vlSelfRef.KL_mbx__DOT____VlemCall_191__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__191__value);
    __Vfunc_mbx_place_f__192__value = vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[0U];
    vlSelfRef.KL_mbx__DOT____VlemCall_192__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__192__value);
    __Vfunc_mbx_place_f__193__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__tx_tail_w[0U]);
    vlSelfRef.KL_mbx__DOT____VlemCall_193__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__193__value);
    __Vfunc_mbx_place_f__194__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__rx_drop_w[0U]);
    vlSelfRef.KL_mbx__DOT____VlemCall_194__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__194__value);
    __Vfunc_mbx_place_f__195__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__rate_drop_w[0U]);
    vlSelfRef.KL_mbx__DOT____VlemCall_195__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__195__value);
    __Vfunc_mbx_place_f__196__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__tx_err_w[0U]);
    vlSelfRef.KL_mbx__DOT____VlemCall_196__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__196__value);
    __Vfunc_mbx_place_f__197__value = (0x0000ffffU 
                                       & vlSelfRef.__PVT__KL_mbx__DOT__rx_pass_w[0U]);
    vlSelfRef.KL_mbx__DOT____VlemCall_197__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__197__value);
    __Vfunc_mbx_place_f__198__value = (vlSelfRef.__PVT__KL_mbx__DOT__rx_head_w[0U] 
                                       >> 0x00000010U);
    vlSelfRef.KL_mbx__DOT____VlemCall_198__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__198__value);
    vlSelfRef.__Vfunc_mbx_place_f__199__value = vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[1U];
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
}

void Vsim_sim___nba_sequent__TOP__sim__44(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__44\n"); );
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

void Vsim_sim___nba_sequent__TOP__sim__45(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__45\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__add_devices_master_status_status 
        = (((IData)(vlSelfRef.__PVT__add_devices_master_rx_fifo_pipe_valid_source_valid) 
            << 1U) | (1U & ((~ (IData)(vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_valid)) 
                            | (IData)(vlSelfRef.__PVT__builder_litespi_tx_mux_endpoint1_sink_ready))));
    vlSelfRef.__PVT__add_devices_mmap_bus_dat_r = 0U;
    vlSelfRef.__PVT__add_devices_mmap_burst_adr_subfragments_next_value_ce3 = 0U;
    vlSelfRef.__PVT__add_devices_mmap_bus_ack = 0U;
    if ((8U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                      >> 2U)))) {
            if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                          >> 1U)))) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_litespi_state)))) {
                    vlSelfRef.__PVT__add_devices_mmap_bus_dat_r 
                        = ((((0x0000ff00U & (vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_payload_data 
                                             << 8U)) 
                             | (0x000000ffU & (vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_payload_data 
                                               >> 8U))) 
                            << 0x00000010U) | ((0x0000ff00U 
                                                & (vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_payload_data 
                                                   >> 8U)) 
                                               | (vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_payload_data 
                                                  >> 0x18U)));
                    if (vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_valid) {
                        vlSelfRef.__PVT__add_devices_mmap_burst_adr_subfragments_next_value_ce3 = 1U;
                        vlSelfRef.__PVT__add_devices_mmap_bus_ack = 1U;
                    }
                }
            }
        }
    } else if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                         >> 2U)))) {
        if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_burst_adr_subfragments_next_value_ce3 = 1U;
        }
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j 
        = (0x0000000fU & VL_MULS_III(32, (IData)(3U), (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
           >= ((IData)(8U) + ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                               ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_OFFSET_TBL_C
                              [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                               : 0U)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__own_end 
        = (0x0001ffffffffffffULL & ((vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__maap_base_i 
                                     + (QData)((IData)(
                                                       (0x0000ffffU 
                                                        & vlSelfRef.__PVT__KL_mbx__DOT__maap_count_r)))) 
                                    - 1ULL));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__req_end 
        = (0x0001ffffffffffffULL & (((((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                        ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                                       [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                        : 0ULL) >> 0x10U) 
                                     + (QData)((IData)(
                                                       (0x0000ffffU 
                                                        & (IData)(
                                                                  ((0x0eU 
                                                                    >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                                    ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                                                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                                    : 0ULL)))))) 
                                    - 1ULL));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__overlap 
        = ((((0U != (0x0000ffffU & (IData)(((0x0eU 
                                             >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                             ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                                            [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                             : 0ULL)))) 
             & (0U != (0x0000ffffU & vlSelfRef.__PVT__KL_mbx__DOT__maap_count_r))) 
            & ((((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                  ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                  : 0ULL) >> 0x10U) <= vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__own_end)) 
           & (vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__maap_base_i 
              <= vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__req_end));
    if ((1U & (((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                 ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_MASK_TBL_C
                [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                 : 0U) >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__msg_r)))) {
        if ((1U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                     ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                    [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                     : 0U))) {
            vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
        } else if ((2U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)) 
                    && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r) 
                              >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)))))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        } else if ((3U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)) 
                    && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r) 
                              >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)))))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        } else if ((4U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__overlap))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        } else if ((5U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__bound_hit_w))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        }
        if ((1U & (~ VL_ONEHOT_I(((((5U == ((0x0eU 
                                             >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                             ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                            [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                             : 0U)) 
                                    << 4U) | (((4U 
                                                == 
                                                ((0x0eU 
                                                  >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                  ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                  : 0U)) 
                                               << 3U) 
                                              | ((3U 
                                                  == 
                                                  ((0x0eU 
                                                    >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                    ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                    : 0U)) 
                                                 << 2U))) 
                                  | (((2U == ((0x0eU 
                                               >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                               ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                              [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                               : 0U)) 
                                      << 1U) | (1U 
                                                == 
                                                ((0x0eU 
                                                  >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                  ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                  : 0U)))))))) {
            if ((0U != ((((5U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                   ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                  [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                   : 0U)) << 4U) | 
                         (((4U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                    ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                    : 0U)) << 3U) | 
                          ((3U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                    ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                    : 0U)) << 2U))) 
                        | (((2U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                     ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                    [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                     : 0U)) << 1U) 
                           | (1U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                      ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                     [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                      : 0U)))))) {
                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                    VL_WRITEF_NX("[%0t] %%Error: KL_mbx_rx.sv:496: Assertion failed in %m: unique case, but multiple matches found for '32'h%X'\n",4, 'M',vlSymsp->name(),"sim.KL_mbx.u_rx.verdict.unnamedblk11.unnamedblk12", 'T',-9
                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                 , '#',32,((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                            : 0U));
                    VL_STOP_MT("$LANES/cicd4-cand-egress/hdl/milan/mailbox/KL_mbx_rx.sv", 496, "");
                }
            }
        }
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j 
        = (0x0000000fU & ((IData)(1U) + VL_MULS_III(32, (IData)(3U), (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
           >= ((IData)(8U) + ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                               ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_OFFSET_TBL_C
                              [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                               : 0U)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__own_end 
        = (0x0001ffffffffffffULL & ((vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__maap_base_i 
                                     + (QData)((IData)(
                                                       (0x0000ffffU 
                                                        & vlSelfRef.__PVT__KL_mbx__DOT__maap_count_r)))) 
                                    - 1ULL));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__req_end 
        = (0x0001ffffffffffffULL & (((((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                        ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                                       [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                        : 0ULL) >> 0x10U) 
                                     + (QData)((IData)(
                                                       (0x0000ffffU 
                                                        & (IData)(
                                                                  ((0x0eU 
                                                                    >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                                    ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                                                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                                    : 0ULL)))))) 
                                    - 1ULL));
}

void Vsim_sim___nba_sequent__TOP__sim__46(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__46\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__overlap 
        = ((((0U != (0x0000ffffU & (IData)(((0x0eU 
                                             >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                             ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                                            [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                             : 0ULL)))) 
             & (0U != (0x0000ffffU & vlSelfRef.__PVT__KL_mbx__DOT__maap_count_r))) 
            & ((((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                  ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                  : 0ULL) >> 0x10U) <= vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__own_end)) 
           & (vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__maap_base_i 
              <= vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__req_end));
    if ((1U & (((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                 ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_MASK_TBL_C
                [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                 : 0U) >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__msg_r)))) {
        if ((1U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                     ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                    [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                     : 0U))) {
            vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
        } else if ((2U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)) 
                    && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r) 
                              >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)))))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        } else if ((3U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)) 
                    && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r) 
                              >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)))))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        } else if ((4U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__overlap))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        } else if ((5U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__bound_hit_w))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        }
        if ((1U & (~ VL_ONEHOT_I(((((5U == ((0x0eU 
                                             >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                             ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                            [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                             : 0U)) 
                                    << 4U) | (((4U 
                                                == 
                                                ((0x0eU 
                                                  >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                  ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                  : 0U)) 
                                               << 3U) 
                                              | ((3U 
                                                  == 
                                                  ((0x0eU 
                                                    >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                    ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                    : 0U)) 
                                                 << 2U))) 
                                  | (((2U == ((0x0eU 
                                               >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                               ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                              [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                               : 0U)) 
                                      << 1U) | (1U 
                                                == 
                                                ((0x0eU 
                                                  >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                  ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                  : 0U)))))))) {
            if ((0U != ((((5U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                   ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                  [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                   : 0U)) << 4U) | 
                         (((4U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                    ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                    : 0U)) << 3U) | 
                          ((3U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                    ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                    : 0U)) << 2U))) 
                        | (((2U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                     ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                    [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                     : 0U)) << 1U) 
                           | (1U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                      ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                     [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                      : 0U)))))) {
                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                    VL_WRITEF_NX("[%0t] %%Error: KL_mbx_rx.sv:496: Assertion failed in %m: unique case, but multiple matches found for '32'h%X'\n",4, 'M',vlSymsp->name(),"sim.KL_mbx.u_rx.verdict.unnamedblk11.unnamedblk12", 'T',-9
                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                 , '#',32,((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                            : 0U));
                    VL_STOP_MT("$LANES/cicd4-cand-egress/hdl/milan/mailbox/KL_mbx_rx.sv", 496, "");
                }
            }
        }
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j 
        = (0x0000000fU & ((IData)(2U) + VL_MULS_III(32, (IData)(3U), (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
           >= ((IData)(8U) + ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                               ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_OFFSET_TBL_C
                              [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                               : 0U)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__own_end 
        = (0x0001ffffffffffffULL & ((vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__maap_base_i 
                                     + (QData)((IData)(
                                                       (0x0000ffffU 
                                                        & vlSelfRef.__PVT__KL_mbx__DOT__maap_count_r)))) 
                                    - 1ULL));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__req_end 
        = (0x0001ffffffffffffULL & (((((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                        ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                                       [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                        : 0ULL) >> 0x10U) 
                                     + (QData)((IData)(
                                                       (0x0000ffffU 
                                                        & (IData)(
                                                                  ((0x0eU 
                                                                    >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                                    ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                                                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                                    : 0ULL)))))) 
                                    - 1ULL));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__overlap 
        = ((((0U != (0x0000ffffU & (IData)(((0x0eU 
                                             >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                             ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                                            [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                             : 0ULL)))) 
             & (0U != (0x0000ffffU & vlSelfRef.__PVT__KL_mbx__DOT__maap_count_r))) 
            & ((((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                  ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r
                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                  : 0ULL) >> 0x10U) <= vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__own_end)) 
           & (vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__maap_base_i 
              <= vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__req_end));
    if ((1U & (((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                 ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_MASK_TBL_C
                [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                 : 0U) >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__msg_r)))) {
        if ((1U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                     ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                    [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                     : 0U))) {
            vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
        } else if ((2U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)) 
                    && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqown_r) 
                              >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)))))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        } else if ((3U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)) 
                    && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eqzero_r) 
                              >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j)))))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        } else if ((4U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__overlap))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        } else if ((5U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                            : 0U))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok) 
                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__bound_hit_w))) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w = 1U;
            }
        }
        if ((1U & (~ VL_ONEHOT_I(((((5U == ((0x0eU 
                                             >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                             ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                            [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                             : 0U)) 
                                    << 4U) | (((4U 
                                                == 
                                                ((0x0eU 
                                                  >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                  ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                  : 0U)) 
                                               << 3U) 
                                              | ((3U 
                                                  == 
                                                  ((0x0eU 
                                                    >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                    ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                    : 0U)) 
                                                 << 2U))) 
                                  | (((2U == ((0x0eU 
                                               >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                               ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                              [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                               : 0U)) 
                                      << 1U) | (1U 
                                                == 
                                                ((0x0eU 
                                                  >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                                  ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                                  : 0U)))))))) {
            if ((0U != ((((5U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                   ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                  [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                   : 0U)) << 4U) | 
                         (((4U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                    ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                    : 0U)) << 3U) | 
                          ((3U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                    ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                    : 0U)) << 2U))) 
                        | (((2U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                     ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                    [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                     : 0U)) << 1U) 
                           | (1U == ((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                      ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                     [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                      : 0U)))))) {
                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                    VL_WRITEF_NX("[%0t] %%Error: KL_mbx_rx.sv:496: Assertion failed in %m: unique case, but multiple matches found for '32'h%X'\n",4, 'M',vlSymsp->name(),"sim.KL_mbx.u_rx.verdict.unnamedblk11.unnamedblk12", 'T',-9
                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                 , '#',32,((0x0eU >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j))
                                            ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_TERM_TEST_TBL_C
                                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j]
                                            : 0U));
                    VL_STOP_MT("$LANES/cicd4-cand-egress/hdl/milan/mailbox/KL_mbx_rx.sv", 496, "");
                }
            }
        }
    }
}

void Vsim_sim___nba_sequent__TOP__sim__47(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__47\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__builder_shared_ack = ((((((IData)(vlSelfRef.__PVT__ctrlmemory0_sram0_bus_ack) 
                                               | (IData)(vlSelfRef.__PVT__ctrlmemory0_sram1_bus_ack)) 
                                              | ((IData)(vlSelfRef.__PVT__ctrlmemory1_sram2_bus_ack) 
                                                 | ((IData)(vlSelfRef.__PVT__ctrlmemory1_sram3_bus_ack) 
                                                    | (IData)(vlSelfRef.__PVT__ctrlmemory1_sram4_bus_ack)))) 
                                             | ((IData)(vlSelfRef.__PVT__KL_mbx_wb__DOT__busy_r) 
                                                & (IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma5))) 
                                            | (IData)(vlSelfRef.__PVT__add_devices_mmap_bus_ack)) 
                                           | (IData)(vlSelfRef.__PVT__builder_interface0_ack));
    if ((0U == vlSelfRef.__PVT__builder_count)) {
        vlSelfRef.__PVT__builder_shared_ack = 1U;
    }
    vlSelfRef.__PVT__soc_data_socbushandler_next_value_ce1 = 0U;
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_ar_ready = 0U;
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_aw_ready = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_state) 
                  >> 2U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_state) 
                      >> 1U)))) {
            if ((1U & (IData)(vlSelfRef.__PVT__builder_state))) {
                if (vlSelfRef.__PVT__builder_shared_ack) {
                    vlSelfRef.__PVT__soc_data_socbushandler_next_value_ce1 = 1U;
                    vlSelfRef.__PVT__soc_vexiiriscv_pbus_ar_ready = 1U;
                }
            }
        }
        if ((2U & (IData)(vlSelfRef.__PVT__builder_state))) {
            if ((1U & (IData)(vlSelfRef.__PVT__builder_state))) {
                if (vlSelfRef.__PVT__builder_shared_ack) {
                    vlSelfRef.__PVT__soc_vexiiriscv_pbus_aw_ready = 1U;
                }
            }
        }
    }
}

void Vsim_sim___nba_sequent__TOP__sim__48(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__48\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*4:0*/ __Vfunc_KL_mbx_dma__DOT__chunk_of__241__Vfuncout;
    __Vfunc_KL_mbx_dma__DOT__chunk_of__241__Vfuncout = 0;
    SData/*10:0*/ __Vfunc_KL_mbx_dma__DOT__chunk_of__241__words;
    __Vfunc_KL_mbx_dma__DOT__chunk_of__241__words = 0;
    CData/*3:0*/ __Vfunc_KL_mbx_dma__DOT__chunk_of__241__word_in_line;
    __Vfunc_KL_mbx_dma__DOT__chunk_of__241__word_in_line = 0;
    CData/*4:0*/ __Vfunc_KL_mbx_dma__DOT__chunk_of__241__room;
    __Vfunc_KL_mbx_dma__DOT__chunk_of__241__room = 0;
    CData/*4:0*/ __Vfunc_KL_mbx_dma__DOT__chunk_of__242__Vfuncout;
    __Vfunc_KL_mbx_dma__DOT__chunk_of__242__Vfuncout = 0;
    SData/*10:0*/ __Vfunc_KL_mbx_dma__DOT__chunk_of__242__words;
    __Vfunc_KL_mbx_dma__DOT__chunk_of__242__words = 0;
    CData/*3:0*/ __Vfunc_KL_mbx_dma__DOT__chunk_of__242__word_in_line;
    __Vfunc_KL_mbx_dma__DOT__chunk_of__242__word_in_line = 0;
    CData/*4:0*/ __Vfunc_KL_mbx_dma__DOT__chunk_of__242__room;
    __Vfunc_KL_mbx_dma__DOT__chunk_of__242__room = 0;
    SData/*12:0*/ __Vfunc_KL_mbx_dma__DOT__ring_word__243__Vfuncout;
    __Vfunc_KL_mbx_dma__DOT__ring_word__243__Vfuncout = 0;
    SData/*12:0*/ __Vfunc_KL_mbx_dma__DOT__ring_word__243__base;
    __Vfunc_KL_mbx_dma__DOT__ring_word__243__base = 0;
    SData/*15:0*/ __Vfunc_KL_mbx_dma__DOT__ring_word__243__mask;
    __Vfunc_KL_mbx_dma__DOT__ring_word__243__mask = 0;
    SData/*15:0*/ __Vfunc_KL_mbx_dma__DOT__ring_word__243__index;
    __Vfunc_KL_mbx_dma__DOT__ring_word__243__index = 0;
    CData/*4:0*/ __Vfunc_KL_mbx_dma__DOT__chunk_of__244__Vfuncout;
    __Vfunc_KL_mbx_dma__DOT__chunk_of__244__Vfuncout = 0;
    SData/*10:0*/ __Vfunc_KL_mbx_dma__DOT__chunk_of__244__words;
    __Vfunc_KL_mbx_dma__DOT__chunk_of__244__words = 0;
    CData/*3:0*/ __Vfunc_KL_mbx_dma__DOT__chunk_of__244__word_in_line;
    __Vfunc_KL_mbx_dma__DOT__chunk_of__244__word_in_line = 0;
    CData/*4:0*/ __Vfunc_KL_mbx_dma__DOT__chunk_of__244__room;
    __Vfunc_KL_mbx_dma__DOT__chunk_of__244__room = 0;
    // Body
    vlSelfRef.__PVT__soc_adapted_interface_dat_w = 0U;
    vlSelfRef.__PVT__soc_adapted_interface_sel = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_state) 
                  >> 2U)))) {
        if ((2U & (IData)(vlSelfRef.__PVT__builder_state))) {
            if ((1U & (IData)(vlSelfRef.__PVT__builder_state))) {
                vlSelfRef.__PVT__soc_adapted_interface_dat_w 
                    = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_data;
                vlSelfRef.__PVT__soc_adapted_interface_sel 
                    = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_mask;
            }
        } else if ((1U & (IData)(vlSelfRef.__PVT__builder_state))) {
            vlSelfRef.__PVT__soc_adapted_interface_sel = 0x0fU;
        }
    }
    if (vlSelfRef.__VdlySet__KL_mbx_dma__DOT__buf_r__v0) {
        vlSelfRef.__PVT__KL_mbx_dma__DOT__buf_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__buf_r[1U] = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__buf_r[2U] = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__buf_r[3U] = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__buf_r[4U] = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__buf_r[5U] = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__buf_r[6U] = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__buf_r[7U] = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__buf_r[8U] = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__buf_r[9U] = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__buf_r[10U] = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__buf_r[11U] = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__buf_r[12U] = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__buf_r[13U] = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__buf_r[14U] = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__buf_r[15U] = 0U;
    }
    if (vlSelfRef.__VdlySet__KL_mbx_dma__DOT__buf_r__v16) {
        vlSelfRef.__PVT__KL_mbx_dma__DOT__buf_r[vlSelfRef.__VdlyDim0__KL_mbx_dma__DOT__buf_r__v16] 
            = vlSelfRef.__VdlyVal__KL_mbx_dma__DOT__buf_r__v16;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__take_w 
        = ((IData)(vlSymsp->TOP.mbx_rx_valid) & (IData)(vlSymsp->TOP.mbx_rx_ready));
    vlSelfRef.__PVT__builder_rhs_self1 = vlSelfRef.__PVT__soc_adapted_interface_dat_w;
    vlSelfRef.__PVT__builder_rhs_self2 = vlSelfRef.__PVT__soc_adapted_interface_sel;
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__Vdly__KL_mbx_dma__DOT__state_r = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__base_r = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__mask_r = 0U;
        vlSelfRef.__Vdly__KL_mbx_dma__DOT__index_r = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__ring_addr_r = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__word_addr_r = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__left_r = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__tail_be_r = 0x0fU;
        vlSelfRef.__Vdly__KL_mbx_dma__DOT__chunk_r = 0U;
        vlSelfRef.__Vdly__KL_mbx_dma__DOT__count_r = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__err_r = 0U;
        vlSelfRef.__Vdly__KL_mbx_dma__DOT__rerr_r = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__hold_wdata_r = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__hold_last_r = 0U;
    } else {
        if ((4U & (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r))) {
            if ((2U & (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r))) {
                if ((1U & (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r))) {
                    vlSelfRef.__Vdly__KL_mbx_dma__DOT__state_r = 0U;
                } else {
                    if (vlSelfRef.__PVT__KL_mbx_dma__DOT__beat_w) {
                        vlSelfRef.__Vdly__KL_mbx_dma__DOT__count_r 
                            = (0x0000001fU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__count_r)));
                        if ((2U & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bridge_up_r_s2mPipe_rData_resp))) {
                            vlSelfRef.__PVT__KL_mbx_dma__DOT__err_r = 1U;
                            vlSelfRef.__Vdly__KL_mbx_dma__DOT__rerr_r = 1U;
                        }
                        if (vlSelfRef.__PVT__KL_mbx_dma__DOT__ring_wr_w) {
                            vlSelfRef.__PVT__KL_mbx_dma__DOT__hold_wdata_r 
                                = vlSelfRef.__PVT__KL_mbx_dma__DOT__beat_data_w;
                            vlSelfRef.__PVT__KL_mbx_dma__DOT__hold_last_r 
                                = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bridge_up_r_s2mPipe_rData_last;
                        }
                    }
                    if (vlSelfRef.__PVT__KL_mbx_dma__DOT__hold_r) {
                        vlSelfRef.__Vdly__KL_mbx_dma__DOT__index_r 
                            = (0x0000ffffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__index_r)));
                        vlSelfRef.__PVT__KL_mbx_dma__DOT__ring_addr_r 
                            = vlSelfRef.__PVT__KL_mbx_dma__DOT__ring_addr_next_w;
                    }
                    if (vlSelfRef.__PVT__KL_mbx_dma__DOT__chunk_end_w) {
                        vlSelfRef.__PVT__KL_mbx_dma__DOT__left_r 
                            = vlSelfRef.__PVT__KL_mbx_dma__DOT__left_next_w;
                        vlSelfRef.__PVT__KL_mbx_dma__DOT__word_addr_r 
                            = vlSelfRef.__PVT__KL_mbx_dma__DOT__word_addr_next_w;
                        vlSelfRef.__Vdly__KL_mbx_dma__DOT__count_r = 0U;
                        if ((((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__last_chunk_w) 
                              | (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__rerr_r)) 
                             | ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__beat_w) 
                                & ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bridge_up_r_s2mPipe_rData_resp) 
                                   >> 1U)))) {
                            vlSelfRef.__Vdly__KL_mbx_dma__DOT__state_r = 0U;
                        } else {
                            __Vfunc_KL_mbx_dma__DOT__chunk_of__241__word_in_line 
                                = (0x0000000fU & vlSelfRef.__PVT__KL_mbx_dma__DOT__word_addr_next_w);
                            __Vfunc_KL_mbx_dma__DOT__chunk_of__241__words 
                                = vlSelfRef.__PVT__KL_mbx_dma__DOT__left_next_w;
                            __Vfunc_KL_mbx_dma__DOT__chunk_of__241__room 
                                = (0x0000001fU & ((IData)(0x10U) 
                                                  - (IData)(__Vfunc_KL_mbx_dma__DOT__chunk_of__241__word_in_line)));
                            vlSelfRef.__Vdly__KL_mbx_dma__DOT__state_r = 5U;
                            __Vfunc_KL_mbx_dma__DOT__chunk_of__241__Vfuncout 
                                = (0x0000001fU & (((IData)(__Vfunc_KL_mbx_dma__DOT__chunk_of__241__words) 
                                                   < (IData)(__Vfunc_KL_mbx_dma__DOT__chunk_of__241__room))
                                                   ? (IData)(__Vfunc_KL_mbx_dma__DOT__chunk_of__241__words)
                                                   : (IData)(__Vfunc_KL_mbx_dma__DOT__chunk_of__241__room)));
                            vlSelfRef.__Vdly__KL_mbx_dma__DOT__chunk_r 
                                = __Vfunc_KL_mbx_dma__DOT__chunk_of__241__Vfuncout;
                        }
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r))) {
                if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bus_arready) {
                    vlSelfRef.__Vdly__KL_mbx_dma__DOT__state_r = 6U;
                }
            } else if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bridge_up_b_rValid) {
                vlSelfRef.__PVT__KL_mbx_dma__DOT__left_r 
                    = vlSelfRef.__PVT__KL_mbx_dma__DOT__left_next_w;
                vlSelfRef.__PVT__KL_mbx_dma__DOT__word_addr_r 
                    = vlSelfRef.__PVT__KL_mbx_dma__DOT__word_addr_next_w;
                vlSelfRef.__Vdly__KL_mbx_dma__DOT__count_r = 0U;
                if ((2U & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bridge_up_b_rData_resp))) {
                    vlSelfRef.__PVT__KL_mbx_dma__DOT__err_r = 1U;
                    vlSelfRef.__Vdly__KL_mbx_dma__DOT__state_r = 0U;
                } else if (vlSelfRef.__PVT__KL_mbx_dma__DOT__last_chunk_w) {
                    vlSelfRef.__Vdly__KL_mbx_dma__DOT__state_r = 0U;
                } else {
                    __Vfunc_KL_mbx_dma__DOT__chunk_of__242__word_in_line 
                        = (0x0000000fU & vlSelfRef.__PVT__KL_mbx_dma__DOT__word_addr_next_w);
                    __Vfunc_KL_mbx_dma__DOT__chunk_of__242__words 
                        = vlSelfRef.__PVT__KL_mbx_dma__DOT__left_next_w;
                    __Vfunc_KL_mbx_dma__DOT__chunk_of__242__room 
                        = (0x0000001fU & ((IData)(0x10U) 
                                          - (IData)(__Vfunc_KL_mbx_dma__DOT__chunk_of__242__word_in_line)));
                    vlSelfRef.__Vdly__KL_mbx_dma__DOT__state_r = 1U;
                    __Vfunc_KL_mbx_dma__DOT__chunk_of__242__Vfuncout 
                        = (0x0000001fU & (((IData)(__Vfunc_KL_mbx_dma__DOT__chunk_of__242__words) 
                                           < (IData)(__Vfunc_KL_mbx_dma__DOT__chunk_of__242__room))
                                           ? (IData)(__Vfunc_KL_mbx_dma__DOT__chunk_of__242__words)
                                           : (IData)(__Vfunc_KL_mbx_dma__DOT__chunk_of__242__room)));
                    vlSelfRef.__Vdly__KL_mbx_dma__DOT__chunk_r 
                        = __Vfunc_KL_mbx_dma__DOT__chunk_of__242__Vfuncout;
                }
            }
        } else if ((2U & (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r))) {
            if ((1U & (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r))) {
                if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bus_wready) {
                    vlSelfRef.__Vdly__KL_mbx_dma__DOT__count_r 
                        = (0x0000001fU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__count_r)));
                    if (((0x0000001fU & ((IData)(1U) 
                                         + (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__count_r))) 
                         == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__chunk_r))) {
                        vlSelfRef.__Vdly__KL_mbx_dma__DOT__state_r = 4U;
                    }
                }
            } else if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__dma_bus_awready) {
                vlSelfRef.__Vdly__KL_mbx_dma__DOT__state_r = 3U;
            }
        } else if ((1U & (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r))) {
            if (vlSelfRef.__PVT__KL_mbx_dma__DOT__hold_r) {
                vlSelfRef.__Vdly__KL_mbx_dma__DOT__index_r 
                    = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__index_r)));
                vlSelfRef.__PVT__KL_mbx_dma__DOT__ring_addr_r 
                    = vlSelfRef.__PVT__KL_mbx_dma__DOT__ring_addr_next_w;
                vlSelfRef.__Vdly__KL_mbx_dma__DOT__count_r 
                    = (0x0000001fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__count_r)));
                if (((0x0000001fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__count_r))) 
                     == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__chunk_r))) {
                    vlSelfRef.__Vdly__KL_mbx_dma__DOT__count_r = 0U;
                    vlSelfRef.__Vdly__KL_mbx_dma__DOT__state_r = 2U;
                }
            }
        } else if (vlSelfRef.__PVT__add_devices_ctrlmailboxdma16) {
            if ((0U != (3U & vlSelfRef.__PVT__add_devices_ctrlmailboxdma_mem_storage))) {
                vlSelfRef.__PVT__KL_mbx_dma__DOT__err_r = 1U;
            } else {
                __Vfunc_KL_mbx_dma__DOT__ring_word__243__index 
                    = (0x0000ffffU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cmd_storage);
                __Vfunc_KL_mbx_dma__DOT__ring_word__243__mask 
                    = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cfg_storage 
                       >> 0x00000010U);
                vlSelfRef.__PVT__KL_mbx_dma__DOT__err_r = 0U;
                vlSelfRef.__Vdly__KL_mbx_dma__DOT__rerr_r = 0U;
                vlSelfRef.__PVT__KL_mbx_dma__DOT__base_r 
                    = (0x00001fffU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cfg_storage);
                vlSelfRef.__PVT__KL_mbx_dma__DOT__mask_r 
                    = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cfg_storage 
                       >> 0x00000010U);
                vlSelfRef.__Vdly__KL_mbx_dma__DOT__index_r 
                    = (0x0000ffffU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cmd_storage);
                __Vfunc_KL_mbx_dma__DOT__ring_word__243__base 
                    = (0x00001fffU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cfg_storage);
                vlSelfRef.__PVT__KL_mbx_dma__DOT__word_addr_r 
                    = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma_mem_storage 
                       >> 2U);
                vlSelfRef.__PVT__KL_mbx_dma__DOT__left_r 
                    = (0x000007ffU & (((IData)(3U) 
                                       + (0x00000fffU 
                                          & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cmd_storage 
                                             >> 0x00000010U))) 
                                      >> 2U));
                vlSelfRef.__PVT__KL_mbx_dma__DOT__tail_be_r 
                    = (0x0000000fU & ((((IData)(1U) 
                                        << (3U & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cmd_storage 
                                                  >> 0x00000010U))) 
                                       - (IData)(1U)) 
                                      | (- (IData)(
                                                   (0U 
                                                    == 
                                                    (3U 
                                                     & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cmd_storage 
                                                        >> 0x00000010U)))))));
                vlSelfRef.__Vdly__KL_mbx_dma__DOT__count_r = 0U;
                if ((0U != (0x00000fffU & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cmd_storage 
                                           >> 0x00000010U)))) {
                    __Vfunc_KL_mbx_dma__DOT__chunk_of__244__word_in_line 
                        = (0x0000000fU & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma_mem_storage 
                                          >> 2U));
                    __Vfunc_KL_mbx_dma__DOT__chunk_of__244__words 
                        = (0x000007ffU & (((IData)(3U) 
                                           + (0x00000fffU 
                                              & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cmd_storage 
                                                 >> 0x00000010U))) 
                                          >> 2U));
                    __Vfunc_KL_mbx_dma__DOT__chunk_of__244__room 
                        = (0x0000001fU & ((IData)(0x10U) 
                                          - (IData)(__Vfunc_KL_mbx_dma__DOT__chunk_of__244__word_in_line)));
                    vlSelfRef.__Vdly__KL_mbx_dma__DOT__state_r 
                        = ((vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cmd_storage 
                            >> 0x0000001fU) ? 5U : 1U);
                    __Vfunc_KL_mbx_dma__DOT__chunk_of__244__Vfuncout 
                        = (0x0000001fU & (((IData)(__Vfunc_KL_mbx_dma__DOT__chunk_of__244__words) 
                                           < (IData)(__Vfunc_KL_mbx_dma__DOT__chunk_of__244__room))
                                           ? (IData)(__Vfunc_KL_mbx_dma__DOT__chunk_of__244__words)
                                           : (IData)(__Vfunc_KL_mbx_dma__DOT__chunk_of__244__room)));
                    vlSelfRef.__Vdly__KL_mbx_dma__DOT__chunk_r 
                        = __Vfunc_KL_mbx_dma__DOT__chunk_of__244__Vfuncout;
                }
                __Vfunc_KL_mbx_dma__DOT__ring_word__243__Vfuncout 
                    = (0x00001fffU & ((IData)(__Vfunc_KL_mbx_dma__DOT__ring_word__243__base) 
                                      + ((IData)(__Vfunc_KL_mbx_dma__DOT__ring_word__243__index) 
                                         & (IData)(__Vfunc_KL_mbx_dma__DOT__ring_word__243__mask))));
                vlSelfRef.__PVT__KL_mbx_dma__DOT__ring_addr_r 
                    = __Vfunc_KL_mbx_dma__DOT__ring_word__243__Vfuncout;
            }
        }
        if (((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma16) 
             & (0U != (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r)))) {
            vlSelfRef.__PVT__KL_mbx_dma__DOT__err_r = 1U;
        }
    }
}

void Vsim_sim___nba_sequent__TOP__sim__49(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__49\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cmp_w 
        = ((8U > ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                  - (IData)(0x00000012U))) & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__take_w));
    vlSelfRef.__PVT__builder_basiclowerer_self = vlSelfRef.__PVT__builder_rhs_self1;
    vlSelfRef.__PVT__builder_csr_data_width = 0U;
    if ((0U != (IData)(vlSelfRef.__PVT__builder_rhs_self2))) {
        vlSelfRef.__PVT__builder_csr_data_width = 0U;
    }
    vlSelfRef.__PVT__KL_mbx_dma__DOT__index_r = vlSelfRef.__Vdly__KL_mbx_dma__DOT__index_r;
    vlSelfRef.__PVT__KL_mbx_dma__DOT__rerr_r = vlSelfRef.__Vdly__KL_mbx_dma__DOT__rerr_r;
    vlSelfRef.__PVT__KL_mbx_dma__DOT__count_r = vlSelfRef.__Vdly__KL_mbx_dma__DOT__count_r;
    vlSelfRef.__PVT__KL_mbx_dma__DOT__chunk_r = vlSelfRef.__Vdly__KL_mbx_dma__DOT__chunk_r;
    vlSelfRef.__PVT__builder_interface0_dat_r = 0U;
    if (vlSelfRef.__PVT__builder_wishbone2csr_state) {
        vlSelfRef.__PVT__builder_interface0_dat_r = 0U;
        if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_csr_data_width)))) {
            vlSelfRef.__PVT__builder_interface0_dat_r 
                = (vlSelfRef.__PVT__builder_csr_bankarray_interface0_bank_bus_dat_r 
                   | (vlSelfRef.__PVT__builder_csr_bankarray_interface1_bank_bus_dat_r 
                      | (vlSelfRef.__PVT__builder_csr_bankarray_interface2_bank_bus_dat_r 
                         | (vlSelfRef.__PVT__builder_csr_bankarray_interface3_bank_bus_dat_r 
                            | (vlSelfRef.__PVT__builder_csr_bankarray_interface4_bank_bus_dat_r 
                               | (vlSelfRef.__PVT__builder_csr_bankarray_sram_bus_dat_r 
                                  | vlSelfRef.__PVT__builder_csr_bankarray_interface5_bank_bus_dat_r))))));
        }
    }
    vlSelfRef.__PVT__KL_mbx_dma__DOT__ring_addr_next_w 
        = (0x00001fffU & ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__base_r) 
                          + ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__mask_r) 
                             & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__index_r)))));
    vlSelfRef.__PVT__KL_mbx_dma__DOT__left_next_w = 
        (0x000007ffU & ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__left_r) 
                        - (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__chunk_r)));
    vlSelfRef.__PVT__KL_mbx_dma__DOT__word_addr_next_w 
        = (0x3fffffffU & (vlSelfRef.__PVT__KL_mbx_dma__DOT__word_addr_r 
                          + (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__chunk_r)));
    vlSelfRef.__PVT__KL_mbx_dma__DOT__last_chunk_w 
        = ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__left_r) 
           == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__chunk_r));
    if (vlSelfRef.__PVT__builder_csr_bankarray_csrbank1_mem_re) {
        vlSelfRef.__PVT__add_devices_ctrlmailboxdma_mem_storage 
            = vlSelfRef.__PVT__builder_interface1_dat_w;
    }
    if (vlSelfRef.__PVT__builder_csr_bankarray_csrbank1_cfg_re) {
        vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cfg_storage 
            = vlSelfRef.__PVT__builder_interface1_dat_w;
    }
    if (vlSelfRef.__PVT__builder_csr_bankarray_csrbank1_cmd_re) {
        vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cmd_storage 
            = vlSelfRef.__PVT__builder_interface1_dat_w;
    }
    vlSelfRef.__PVT__add_devices_ctrlmailboxdma16 = vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cmd_wr_stb;
    vlSelfRef.__PVT__KL_mbx_dma__DOT__hold_r = ((1U 
                                                 & (~ (IData)(vlSymsp->TOP.sys_reset))) 
                                                && ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__fill_req_w) 
                                                    | (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__ring_wr_w)));
    vlSelfRef.__PVT__builder_interface1_dat_w = 0U;
    if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_wishbone2csr_state)))) {
        vlSelfRef.__PVT__builder_interface1_dat_w = vlSelfRef.__PVT__builder_basiclowerer_self;
    }
    vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cmd_wr_stb 
        = vlSelfRef.__PVT__builder_csr_bankarray_csrbank1_cmd_re;
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__PVT__add_devices_ctrlmailboxdma_mem_storage = 0U;
        vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cfg_storage = 0U;
        vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cmd_storage = 0U;
        vlSelfRef.__PVT__add_devices_ctrlmailboxdma16 = 0U;
        vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cmd_wr_stb = 0U;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_101 = (1U 
                                                  & (~ 
                                                     ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__hold_r) 
                                                      | (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__cpu_wait_r))));
}
