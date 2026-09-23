// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

extern const VlUnpacked<CData/*0:0*/, 32> Vmilan_datapath__ConstPool__TABLE_h5f1389fb_0;
extern const VlUnpacked<CData/*2:0*/, 32> Vmilan_datapath__ConstPool__TABLE_h6dff1152_0;
extern const VlWide<9>/*287:0*/ Vmilan_datapath__ConstPool__CONST_h9a2fc1c8_0;
extern const VlWide<14>/*447:0*/ Vmilan_datapath__ConstPool__CONST_hb0e0ad07_0;
extern const VlWide<9>/*287:0*/ Vmilan_datapath__ConstPool__CONST_h11ab053c_0;
extern const VlWide<8>/*255:0*/ Vmilan_datapath__ConstPool__CONST_h9e67c271_0;

void Vmilan_datapath___024root___nba_sequent__TOP__1(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___nba_sequent__TOP__1\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c;
    __Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c = 0;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st = 0;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev = 0;
    CData/*0:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__reg_in_i;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__reg_in_i = 0;
    CData/*0:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p = 0;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx = 0;
    CData/*4:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_next__68__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_next__68__Vfuncout = 0;
    CData/*4:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_next__68__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_next__68__s = 0;
    CData/*7:0*/ __Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__306__Vfuncout;
    __Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__306__Vfuncout = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__306__n;
    __Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__306__n = 0;
    // Body
    if (vlSelfRef.axis_resetn) {
        if (vlSelfRef.milan_datapath__DOT__csr__DOT__i2spb_clro_p) {
            vlSelfRef.__Vdly__milan_datapath__DOT__i2spb_overruns 
                = ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_drop_w)
                    ? 1U : 0U);
        } else if (vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_drop_w) {
            vlSelfRef.__Vdly__milan_datapath__DOT__i2spb_overruns 
                = (0x0000ffffU & ((0x0000ffffU == (IData)(vlSelfRef.milan_datapath__DOT__i2spb_overruns))
                                   ? (IData)(vlSelfRef.milan_datapath__DOT__i2spb_overruns)
                                   : ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__i2spb_overruns))));
        }
        if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_rec_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_assem_r = 0ULL;
        } else {
            if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_amap_edit_req_w) 
                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxr_valid_r)) 
                 & (1U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_amap_edit_phase_w)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_rec_r = 0U;
            } else if (((((((IData)(vlSelfRef.milan_datapath__DOT__pp_amap_req_w) 
                            & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_sel_w) 
                               >> 4U)) | ((IData)(vlSelfRef.milan_datapath__DOT__pp_amap_edit_req_w) 
                                          & (4U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_amap_edit_phase_w)))) 
                          | ((IData)(vlSelfRef.milan_datapath__DOT__pp_gsi_req_w) 
                             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_sel_w) 
                                >> 3U))) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxr_valid_r)) 
                        & (0xffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_rec_r)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_rec_r 
                    = (0x000000ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_rec_r)));
            }
            if ((((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r)) 
                  & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_r) 
                     | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sname_r))) 
                 & (0x000bU <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_assem_r 
                    = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_assem_r 
                        << 8U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)));
                if ((7U == (7U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                  - (IData)(0x000bU))))) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_r__v0 
                        = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_assem_r 
                            << 8U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o)));
                    vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_r__v0 
                        = (0x000000ffU & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r) 
                                           - (IData)(0x000bU)) 
                                          >> 3U));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_r__v0 = 1U;
                }
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_eff_notify_stb_nc_w) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmd_class_ok_w))) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmd_push_w) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_class_r__v0 
                    = (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r));
                vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_class_r__v0 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_wr_r;
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_class_r__v0 = 1U;
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_type_r__v0 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r) 
                       & (- (IData)((1U != (0x0000000fU 
                                            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r))))));
                vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_type_r__v0 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_wr_r;
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_index_r__v0 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r) 
                       & (- (IData)((1U != (0x0000000fU 
                                            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r))))));
                vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_index_r__v0 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_wr_r;
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_arg0_r__v0 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_eff_notify_arg0_w;
                vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_arg0_r__v0 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_wr_r;
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_arg1_r__v0 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_eff_notify_arg1_w;
                vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_arg1_r__v0 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_wr_r;
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_excl_r__v0 
                    = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[8U])) 
                        << 0x00000022U) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[7U])) 
                                            << 2U) 
                                           | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[6U])) 
                                              >> 0x0000001eU)));
                vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_excl_r__v0 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_wr_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_wr_r 
                    = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_wr_r)));
            }
        }
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a 
            = (0x0000007fU & (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w) 
                               & (0U == (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i)))
                               ? (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_data_i)
                               : vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[0U]));
        if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_en_w) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a) 
                == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_addr_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v0 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp1_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v0 = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_en_w) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a) 
                       == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_addr_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v1 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp0_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v1 = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w) 
                    & (0U == (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v2 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_seed_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v2 = 1U;
        }
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a 
            = (0x0000007fU & (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w) 
                               & (1U == (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i)))
                               ? (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_data_i)
                               : vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[1U]));
        if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_en_w) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a) 
                == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_addr_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v3 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp1_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v3 = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_en_w) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a) 
                       == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_addr_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v4 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp0_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v4 = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w) 
                    & (1U == (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v5 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_seed_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v5 = 1U;
        }
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a 
            = (0x0000007fU & (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w) 
                               & (2U == (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i)))
                               ? (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_data_i)
                               : vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[2U]));
        if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_en_w) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a) 
                == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_addr_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v6 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp1_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v6 = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_en_w) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a) 
                       == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_addr_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v7 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp0_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v7 = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w) 
                    & (2U == (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v8 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_seed_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v8 = 1U;
        }
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a 
            = (0x0000007fU & (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w) 
                               & (3U == (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i)))
                               ? (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_data_i)
                               : vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[3U]));
        if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_en_w) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a) 
                == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_addr_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v9 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp1_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v9 = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_en_w) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a) 
                       == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_addr_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v10 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp0_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v10 = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w) 
                    & (3U == (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v11 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_seed_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v11 = 1U;
        }
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a 
            = (0x0000007fU & (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w) 
                               & (4U == (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i)))
                               ? (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_data_i)
                               : vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[4U]));
        if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_en_w) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a) 
                == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_addr_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v12 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp1_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v12 = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_en_w) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a) 
                       == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_addr_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v13 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp0_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v13 = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w) 
                    & (4U == (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v14 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_seed_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v14 = 1U;
        }
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a 
            = (0x0000007fU & (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w) 
                               & (5U == (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i)))
                               ? (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_data_i)
                               : vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[5U]));
        if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_en_w) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a) 
                == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_addr_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v15 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp1_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v15 = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_en_w) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a) 
                       == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_addr_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v16 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp0_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v16 = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w) 
                    & (5U == (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v17 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_seed_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v17 = 1U;
        }
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a 
            = (0x0000007fU & (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w) 
                               & (6U == (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i)))
                               ? (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_data_i)
                               : vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[6U]));
        if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_en_w) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a) 
                == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_addr_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v18 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp1_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v18 = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_en_w) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a) 
                       == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_addr_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v19 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp0_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v19 = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w) 
                    & (6U == (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v20 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_seed_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v20 = 1U;
        }
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a 
            = (0x0000007fU & (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w) 
                               & (7U == (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i)))
                               ? (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_data_i)
                               : vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[7U]));
        if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_en_w) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a) 
                == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_addr_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v21 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp1_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v21 = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_en_w) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a) 
                       == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_addr_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v22 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp0_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v22 = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w) 
                    & (7U == (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v23 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_seed_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v23 = 1U;
        }
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a 
            = (0x0000007fU & (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w) 
                               & (8U == (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i)))
                               ? (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_data_i)
                               : vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[8U]));
        if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_en_w) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a) 
                == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_addr_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v24 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp1_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v24 = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_en_w) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a) 
                       == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_addr_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v25 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp0_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v25 = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w) 
                    & (8U == (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v26 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_seed_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v26 = 1U;
        }
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a 
            = (0x0000007fU & (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w) 
                               & (9U == (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i)))
                               ? (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_data_i)
                               : vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[9U]));
        if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_en_w) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a) 
                == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_addr_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v27 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp1_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v27 = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_en_w) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__source_track__DOT__unnamedblk7__DOT__track_one__DOT__a) 
                       == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_addr_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v28 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp0_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v28 = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w) 
                    & (9U == (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v29 
                = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_seed_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v29 = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__overflow_reg) {
            vlSelfRef.milan_datapath__DOT__pcmrx_drops 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pcmrx_drops)));
        }
        if (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_act_w) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v0 
                = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r
                                          [(0x0000001fU 
                                            & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r))]) 
                                  - (IData)(1U)));
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v0 
                = (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r));
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v0 = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__push_ram_w) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v1 
                = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__push_drop_w)
                                   ? (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__push_cnt1_w)
                                   : ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__push_cnt1_w))));
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v1 
                = vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_addr_r
                [vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_rp_r];
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v1 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                   | (0x00000000ffffffffULL & ((IData)(1U) 
                                               << vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_addr_r
                                               [vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_rp_r])));
        }
        if ((1U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v2 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v1 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xfffffffeU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((2U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v3 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v2 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xfffffffdU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((4U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v4 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v3 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xfffffffbU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((8U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v5 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v4 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xfffffff7U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x00000010U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v6 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v5 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xffffffefU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x00000020U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v7 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v6 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xffffffdfU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x00000040U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v8 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v7 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xffffffbfU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x00000080U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v9 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v8 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xffffff7fU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x00000100U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v10 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v9 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xfffffeffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x00000200U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v11 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v10 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xfffffdffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x00000400U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v12 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v11 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xfffffbffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x00000800U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v13 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v12 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xfffff7ffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x00001000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v14 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v13 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xffffefffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x00002000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v15 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v14 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xffffdfffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x00004000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v16 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v15 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xffffbfffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x00008000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v17 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v16 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xffff7fffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x00010000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v18 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v17 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xfffeffffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x00020000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v19 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v18 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xfffdffffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x00040000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v20 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v19 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xfffbffffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x00080000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v21 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v20 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xfff7ffffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x00100000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v22 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v21 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xffefffffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x00200000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v23 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v22 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xffdfffffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x00400000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v24 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v23 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xffbfffffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x00800000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v25 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v24 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xff7fffffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x01000000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v26 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v25 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xfeffffffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x02000000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v27 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v26 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xfdffffffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x04000000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v28 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v27 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xfbffffffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x08000000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v29 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v28 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xf7ffffffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x10000000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v30 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v29 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xefffffffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x20000000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v31 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v30 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xdfffffffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((0x40000000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v32 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v31 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0xbfffffffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
        }
        if ((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w 
             >> 0x1fU)) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v33 = 1U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v32 = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                = (0x7fffffffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r);
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
                                                                                (1U 
                                                                                & vlSelfRef.s_axi_wdata)) {
                                                                                vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v0 
                                                                                = vlSelfRef.milan_datapath__DOT__stats_counts[0U];
                                                                                vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__stat_snap__v0 = 1U;
                                                                                vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v1 
                                                                                = vlSelfRef.milan_datapath__DOT__stats_counts[1U];
                                                                                vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v2 
                                                                                = vlSelfRef.milan_datapath__DOT__stats_counts[2U];
                                                                                vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v3 
                                                                                = vlSelfRef.milan_datapath__DOT__stats_counts[3U];
                                                                                vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v4 
                                                                                = vlSelfRef.milan_datapath__DOT__stats_counts[4U];
                                                                                vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v5 
                                                                                = vlSelfRef.milan_datapath__DOT__stats_counts[5U];
                                                                                vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v6 
                                                                                = vlSelfRef.milan_datapath__DOT__stats_counts[6U];
                                                                                vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v7 
                                                                                = vlSelfRef.milan_datapath__DOT__stats_counts[7U];
                                                                                vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v8 
                                                                                = vlSelfRef.milan_datapath__DOT__stats_counts[8U];
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__b_valid = 1U;
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
        if (((~ (IData)(vlSelfRef.o_mac_reinit)) & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_reinit_q))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__stat_snap__v9 = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__ser_start_w) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__run_r = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__fetch_idx_r = 0U;
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v3 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__slot_r;
            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v3 = 1U;
        } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__run_r) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__rd_en_w) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__fetch_idx_r 
                    = (0x000007ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__fetch_idx_r)));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_valid_r = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_last_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__fetch_idx_r) 
                       == (0x000007ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r
                                                  [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__cur_slot_r]) 
                                          - (IData)(1U))));
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__consume_w) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_valid_r = 0U;
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_last_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_last_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__run_r = 0U;
                }
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_load_p) 
             | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_adj_p))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__ptp_clock_validity__DOT__hold_r = 2U;
        } else if (((0x0fffU == (IData)(vlSelfRef.milan_datapath__DOT__ptp_clock_validity__DOT__qdiv_r)) 
                    & (0U != (IData)(vlSelfRef.milan_datapath__DOT__ptp_clock_validity__DOT__hold_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__ptp_clock_validity__DOT__hold_r 
                = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__ptp_clock_validity__DOT__hold_r) 
                         - (IData)(1U)));
        }
        if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_st_r))) {
            if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_valid_r) 
                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_need_r))) {
                if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__txp_valid_r)))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_idx_r = 1U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_st_r = 1U;
                }
            }
        } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_st_r))) {
            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__txp_valid_r)))) {
                if ((0x0dU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_idx_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_st_r = 2U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_idx_r 
                        = (0x0000000fU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_idx_r)));
                }
            }
        } else if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_st_r))) {
            if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_valid_r) 
                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_tx_eof_w)) 
                 & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__txp_valid_r)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_st_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_idx_r = 0U;
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_st_r = 0U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
             & (0U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v0 
                = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__c_in_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v0 = 1U;
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v0 
                = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v0 = 1U;
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
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
             & (1U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v1 
                = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__c_in_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v1 = 1U;
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v1 
                = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v1 = 1U;
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
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
             & (2U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v2 
                = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__c_in_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v2 = 1U;
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v2 
                = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v2 = 1U;
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
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
             & (3U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v3 
                = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__c_in_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v3 = 1U;
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v3 
                = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v3 = 1U;
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
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
             & (4U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v4 
                = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__c_in_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v4 = 1U;
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v4 
                = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v4 = 1U;
            if (vlSelfRef.milan_datapath__DOT__dpkt_pcm_tlast_w) {
                if ((vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[4U] 
                     | vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[4U])) {
                    if ((0x0eU <= (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w))) {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v17 
                            = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w) 
                                              - (IData)(0x0eU)));
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v17 = 1U;
                    } else if (vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[4U]) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v22 = 1U;
                    }
                } else {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v26 
                        = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__in_band_w;
                    vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v26 = 1U;
                    if ((0x14U < (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w))) {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v18 
                            = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w) 
                                              - (IData)(0x0eU)));
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v18 = 1U;
                    } else if ((0x0000000eU > ((IData)(6U) 
                                               + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w)))) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v23 = 1U;
                    }
                }
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
             & (5U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v5 
                = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__c_in_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v5 = 1U;
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v5 
                = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v5 = 1U;
            if (vlSelfRef.milan_datapath__DOT__dpkt_pcm_tlast_w) {
                if ((vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[5U] 
                     | vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[5U])) {
                    if ((0x0eU <= (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w))) {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v21 
                            = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w) 
                                              - (IData)(0x0eU)));
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v21 = 1U;
                    } else if (vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[5U]) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v27 = 1U;
                    }
                } else {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v32 
                        = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__in_band_w;
                    vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v32 = 1U;
                    if ((0x14U < (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w))) {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v22 
                            = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w) 
                                              - (IData)(0x0eU)));
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v22 = 1U;
                    } else if ((0x0000000eU > ((IData)(6U) 
                                               + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w)))) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v28 = 1U;
                    }
                }
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
             & (6U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v6 
                = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__c_in_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v6 = 1U;
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v6 
                = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v6 = 1U;
            if (vlSelfRef.milan_datapath__DOT__dpkt_pcm_tlast_w) {
                if ((vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[6U] 
                     | vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[6U])) {
                    if ((0x0eU <= (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w))) {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v25 
                            = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w) 
                                              - (IData)(0x0eU)));
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v25 = 1U;
                    } else if (vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[6U]) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v32 = 1U;
                    }
                } else {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v38 
                        = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__in_band_w;
                    vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v38 = 1U;
                    if ((0x14U < (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w))) {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v26 
                            = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w) 
                                              - (IData)(0x0eU)));
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v26 = 1U;
                    } else if ((0x0000000eU > ((IData)(6U) 
                                               + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w)))) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v33 = 1U;
                    }
                }
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
             & (7U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v7 
                = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__c_in_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v7 = 1U;
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v7 
                = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v7 = 1U;
            if (vlSelfRef.milan_datapath__DOT__dpkt_pcm_tlast_w) {
                if ((vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[7U] 
                     | vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[7U])) {
                    if ((0x0eU <= (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w))) {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v29 
                            = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w) 
                                              - (IData)(0x0eU)));
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v29 = 1U;
                    } else if (vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[7U]) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v37 = 1U;
                    }
                } else {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v44 
                        = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__in_band_w;
                    vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v44 = 1U;
                    if ((0x14U < (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w))) {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v30 
                            = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w) 
                                              - (IData)(0x0eU)));
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v30 = 1U;
                    } else if ((0x0000000eU > ((IData)(6U) 
                                               + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w)))) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v38 = 1U;
                    }
                }
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__rd_en_w) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_valid_r = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_valid_r) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_txn_ready_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_valid_r = 0U;
        }
        if ((((~ (IData)(vlSelfRef.i_resp_mem_wr_ready)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wreq_r)) 
             | (((~ (IData)(vlSelfRef.i_resp_mem_wr_done)) 
                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wbusy_r)) 
                | (((~ (IData)(vlSelfRef.i_resp_mem_req_ready)) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rreq_r)) 
                   | ((~ (IData)(vlSelfRef.i_resp_mem_rsp_valid)) 
                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_285)))))) {
            if ((0x1000U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__tmo_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__tmo_r 
                    = (0x00001fffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__tmo_r)));
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__tmo_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_open_w) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__tmo_r = 0U;
        }
        if (((vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][2U] 
              >> 8U) & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__pop_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r 
                = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r)));
        }
        if (vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_wr_p) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action__v0 
                = (0x000000ffU & vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_act);
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action__v0 
                = (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_wr_index));
            vlSelfRef.__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action__v0 = 1U;
            vlSelfRef.__VdlyVal__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid__v0 
                = vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_wr_valid_r;
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid__v0 
                = (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_wr_index));
            vlSelfRef.__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid__v0 = 1U;
            vlSelfRef.__VdlyVal__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask__v0 
                = (((QData)((IData)((0x0000ffffU & vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_mhi))) 
                    << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_mlo)));
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask__v0 
                = (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_wr_index));
            vlSelfRef.__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask__v0 = 1U;
            vlSelfRef.__VdlyVal__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key__v0 
                = (((QData)((IData)((0x0000ffffU & vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_khi))) 
                    << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_klo)));
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key__v0 
                = (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_wr_index));
            vlSelfRef.__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key__v0 = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_ret_v_r) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v0 
                = vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rdata_r;
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v0 
                = vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_ret_pair_r;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v0 = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__rd_en_w) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_valid_r = 1U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_valid_r) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_txn_ready_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_valid_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_done_avail_w) {
            if ((0U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_if_r))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r__v0 
                    = ((IData)(1U) + ((0U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_if_r))
                                       ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r
                                      [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_if_r]
                                       : 0U));
                vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r__v0 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_if_r;
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r__v0 = 1U;
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_dep_r) 
             & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r)))) {
            if ((0U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_if_r))) {
                vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r__v1 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_if_r;
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r__v1 = 1U;
            }
        }
        if (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__enq0_v_w) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__skid_data_r__v0 
                = ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__cm0_v_w)
                    ? ((1U & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_chpos_r))
                        ? (((QData)((IData)((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__stash_val_r 
                                             & (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__stash_vld_r)))))) 
                            << 0x00000018U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_smp0_w)))
                        : ((QData)((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_smp0_w)) 
                           << 0x00000018U)) : vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__cm1_data_w);
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__skid_data_r__v0 
                = vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_wp_r;
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__skid_data_r__v0 = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__enq1_v_w) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__skid_data_r__v1 
                = vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__cm1_data_w;
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__skid_data_r__v1 
                = (3U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_wp_r)));
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__skid_data_r__v1 = 1U;
        }
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__gnt_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_adp_r 
                = ((0x00e00000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_adp_r) 
                   | (0x001fffffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_adp_r 
                                     >> 3U)));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_adp_push_w) {
            if ((0x17U >= (0x0000001fU & ((IData)(3U) 
                                          * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_adp_mid_w)))))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_adp_r 
                    = (((~ ((IData)(7U) << (0x0000001fU 
                                            & ((IData)(3U) 
                                               * (7U 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_adp_mid_w)))))) 
                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_adp_r) 
                       | (0x00ffffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_slot_r) 
                                         << (0x0000001fU 
                                             & ((IData)(3U) 
                                                * (7U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_adp_mid_w)))))));
            }
        }
        if ((2U == (((IData)(vlSelfRef.milan_datapath__DOT__aafcap_pv_w) 
                     << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__media_tick_p)))) {
            if (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_frame_pend_r) 
                 & (0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__tdm_skip_cnt_w)))) {
                vlSelfRef.milan_datapath__DOT__tdm_skip_cnt_w 
                    = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__tdm_skip_cnt_w)));
            }
        } else if ((1U == (((IData)(vlSelfRef.milan_datapath__DOT__aafcap_pv_w) 
                            << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__media_tick_p)))) {
            if ((((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_fed_r) 
                  & (~ (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_frame_pend_r))) 
                 & (0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__tdm_dup_cnt_w)))) {
                vlSelfRef.milan_datapath__DOT__tdm_dup_cnt_w 
                    = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__tdm_dup_cnt_w)));
            }
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__crf_clk_selected_r) 
              & ((IData)(vlSelfRef.milan_datapath__DOT__crf_mr_toggle_p_w) 
                 | ((~ (IData)(vlSelfRef.milan_datapath__DOT__crf_locked_w)) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__tkd_crflk_q_r)))) 
             | ((IData)(vlSelfRef.milan_datapath__DOT__media_clk_src_r) 
                != (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__clk_src_q_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__media_clock_restart__DOT__tgt_r 
                = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r)));
        }
        if (((((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_p_i) 
               & (9U > (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w))) 
              & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_mr_i) 
                 == ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w)) 
                     && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__mcr_mr_v_w) 
                               >> (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w)))))) 
             & (8U != ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w))
                        ? vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r
                       [vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w]
                        : 0U)))) {
            if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v0 
                    = (0x0000000fU & ((IData)(1U) + 
                                      ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w))
                                        ? vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r
                                       [vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w]
                                        : 0U)));
                vlSelfRef.__VdlyDim0__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v0 
                    = vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w;
                vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v0 = 1U;
            }
        }
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__mcr_streaming_w))) {
            if ((((1U & (IData)(vlSelfRef.milan_datapath__DOT__mcr_mr_v_w)) 
                  != (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r)) 
                 & (8U == vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[0U]))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w 
                    = ((0x01feU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w)) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r));
                vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v1 = 1U;
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w 
                = ((0x01feU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w)) 
                   | (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r));
            vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v2 = 1U;
        }
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__mcr_streaming_w))) {
            if ((((1U & ((IData)(vlSelfRef.milan_datapath__DOT__mcr_mr_v_w) 
                         >> 1U)) != (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r)) 
                 & (8U == vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[1U]))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w 
                    = ((0x01fdU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w)) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r) 
                          << 1U));
                vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v3 = 1U;
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w 
                = ((0x01fdU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w)) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r) 
                      << 1U));
            vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v4 = 1U;
        }
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__mcr_streaming_w))) {
            if ((((1U & ((IData)(vlSelfRef.milan_datapath__DOT__mcr_mr_v_w) 
                         >> 2U)) != (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r)) 
                 & (8U == vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[2U]))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w 
                    = ((0x01fbU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w)) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r) 
                          << 2U));
                vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v5 = 1U;
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w 
                = ((0x01fbU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w)) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r) 
                      << 2U));
            vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v6 = 1U;
        }
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__mcr_streaming_w))) {
            if ((((1U & ((IData)(vlSelfRef.milan_datapath__DOT__mcr_mr_v_w) 
                         >> 3U)) != (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r)) 
                 & (8U == vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[3U]))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w 
                    = ((0x01f7U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w)) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r) 
                          << 3U));
                vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v7 = 1U;
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w 
                = ((0x01f7U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w)) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r) 
                      << 3U));
            vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v8 = 1U;
        }
        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__mcr_streaming_w))) {
            if ((((1U & ((IData)(vlSelfRef.milan_datapath__DOT__mcr_mr_v_w) 
                         >> 4U)) != (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r)) 
                 & (8U == vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[4U]))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w 
                    = ((0x01efU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w)) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r) 
                          << 4U));
                vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v9 = 1U;
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w 
                = ((0x01efU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w)) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r) 
                      << 4U));
            vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v10 = 1U;
        }
        if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__mcr_streaming_w))) {
            if ((((1U & ((IData)(vlSelfRef.milan_datapath__DOT__mcr_mr_v_w) 
                         >> 5U)) != (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r)) 
                 & (8U == vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[5U]))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w 
                    = ((0x01dfU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w)) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r) 
                          << 5U));
                vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v11 = 1U;
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w 
                = ((0x01dfU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w)) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r) 
                      << 5U));
            vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v12 = 1U;
        }
        if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__mcr_streaming_w))) {
            if ((((1U & ((IData)(vlSelfRef.milan_datapath__DOT__mcr_mr_v_w) 
                         >> 6U)) != (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r)) 
                 & (8U == vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[6U]))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w 
                    = ((0x01bfU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w)) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r) 
                          << 6U));
                vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v13 = 1U;
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w 
                = ((0x01bfU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w)) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r) 
                      << 6U));
            vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v14 = 1U;
        }
        if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__mcr_streaming_w))) {
            if ((((1U & ((IData)(vlSelfRef.milan_datapath__DOT__mcr_mr_v_w) 
                         >> 7U)) != (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r)) 
                 & (8U == vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[7U]))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w 
                    = ((0x017fU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w)) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r) 
                          << 7U));
                vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v15 = 1U;
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w 
                = ((0x017fU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w)) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r) 
                      << 7U));
            vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v16 = 1U;
        }
        if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__mcr_streaming_w))) {
            if ((((1U & ((IData)(vlSelfRef.milan_datapath__DOT__mcr_mr_v_w) 
                         >> 8U)) != (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r)) 
                 & (8U == vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[8U]))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w 
                    = ((0x00ffU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w)) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r) 
                          << 8U));
                vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v17 = 1U;
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w 
                = ((0x00ffU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w)) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r) 
                      << 8U));
            vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v18 = 1U;
        }
        vlSelfRef.milan_datapath__DOT__txarb_abort_sticky_r 
            = ((IData)(vlSelfRef.milan_datapath__DOT__txarb_abort_sticky_r) 
               | (((IData)(vlSelfRef.milan_datapath__DOT____Vcellout__adp_tx_mux__abort_evt_o) 
                   << 3U) | (((IData)(vlSelfRef.milan_datapath__DOT____Vcellout__crf_dp_mux__abort_evt_o) 
                              << 2U) | (IData)(vlSelfRef.milan_datapath__DOT____Vcellout__ctl_tx_mux__abort_evt_o))));
        vlSelfRef.milan_datapath__DOT__txarb_stall_sticky_r 
            = ((IData)(vlSelfRef.milan_datapath__DOT__txarb_stall_sticky_r) 
               | (((IData)(vlSelfRef.milan_datapath__DOT____Vcellout__adp_tx_mux__stall_evt_o) 
                   << 3U) | (((IData)(vlSelfRef.milan_datapath__DOT____Vcellout__crf_dp_mux__stall_evt_o) 
                              << 2U) | (IData)(vlSelfRef.milan_datapath__DOT____Vcellout__ctl_tx_mux__stall_evt_o))));
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__grant_w) {
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v0 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__pick_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v0 = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__commit_w) {
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v1 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_slot_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v1 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_hold_valid_w) 
             & (5U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_hold_slot_w)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__held_r 
                = ((IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__held_r) 
                   | (0x00ffU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_hold_slot_w))));
        }
        if ((Vmilan_datapath__ConstPool__TABLE_h5f1389fb_0
             [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w] 
             & (5U > Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w]))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__held_r 
                = ((~ ((IData)(1U) << Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                       [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w])) 
                   & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__held_r));
            if ((3U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r
                 [Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                 [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w]])) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__release_pend_r 
                    = ((IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__release_pend_r) 
                       | (0x00ffU & ((IData)(1U) << Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                                     [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w])));
            } else if (((2U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r
                         [Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                         [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w]]) 
                        | (1U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r
                           [Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                           [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w]]))) {
                vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v2 
                    = Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                    [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w];
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v2 = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__release_pend_r 
                    = ((~ ((IData)(1U) << Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                           [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w])) 
                       & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__release_pend_r));
            }
        }
        if (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_401) 
             & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_153)) 
                & (0U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r
                   [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__slot_r])))) {
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v4 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__slot_r;
            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v4 = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__eof_w) {
            if ((1U & ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__held_r) 
                         >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__cur_slot_r)) 
                        & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__release_pend_r) 
                              >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__cur_slot_r)))) 
                       & (~ (Vmilan_datapath__ConstPool__TABLE_h5f1389fb_0
                             [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w] 
                             & (Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w] 
                                == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__cur_slot_r))))))) {
                vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v5 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__cur_slot_r;
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v5 = 1U;
            } else {
                vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v6 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__cur_slot_r;
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v6 = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__held_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__cur_slot_r))) 
                       & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__held_r));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__release_pend_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__cur_slot_r))) 
                       & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__release_pend_r));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wen_r) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wfull_w)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__mem_r__v0 
                = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wdata_r;
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__mem_r__v0 
                = (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wptr_bin_r));
            vlSelfRef.__VdlySet__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__mem_r__v0 = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__good_frame_reg) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r__v0 
                = vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__tl_idx_r;
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r__v0 
                = vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_wp_r;
            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r__v0 = 1U;
            vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_wp_r 
                = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_wp_r)));
        }
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w))) {
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p = 1U;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__reg_in_i = 0U;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev 
                = (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w));
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st 
                = (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r));
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st;
            if ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                            : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : 0x0bU)))
                                    : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? 0x0bU
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U))
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : 3U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 4U
                                                : 0x0bU))))))
                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                            ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                                ? ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 0U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                                    : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 0U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U))
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__reg_in_i)
                                                    ? 5U
                                                    : 4U)
                                                : 3U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 4U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))))
                                : ((5U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? 4U : ((0x0aU 
                                             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                             ? 9U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                            : 1U) : 
                                       ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                         ? 1U : 0x0bU)))
                                : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? 0x0bU
                                            : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        : 1U) : ((2U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 2U
                                                   : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  : 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                   : 0x0bU))))));
            } else if ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                if ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                        = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 0U : 9U) : 
                                   ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                     : 7U))) : ((4U 
                                                 & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                 ? 
                                                ((2U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                  : 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 4U
                                                   : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))
                                                 : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)));
                } else if ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                    if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p) 
                         & (4U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))) {
                        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx = 5U;
                    }
                } else {
                    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                        = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 0x0aU : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 8U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : 5U)) : ((2U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                   : 
                                                  ((1U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? 
                                                   ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p)
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 9U)
                                                    : 
                                                   ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p)
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 7U)))));
                }
            } else if ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                        : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : 8U) : ((1U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? 7U
                                                  : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : 6U) : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                              ? 6U : 
                                             ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                               ? 0U
                                               : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))));
            } else if ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                        ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                            : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? 1U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : 0x0aU))) : ((4U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 
                                                  ((2U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                     ? 9U
                                                     : 4U)
                                                    : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   : 
                                                  ((2U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                    : 
                                                   ((1U 
                                                     & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 1U))));
            } else if ((1U & (~ ((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)) 
                                 | (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx = 2U;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT____VlemCall_1__app_next_f 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r 
                = ((0x0000000ffffffff0ULL & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r) 
                   | (IData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT____VlemCall_1__app_next_f)));
        }
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w))) {
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p = 1U;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__reg_in_i = 0U;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev 
                = (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                          >> 4U)));
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st 
                = (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r 
                                          >> 4U)));
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st;
            if ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                            : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : 0x0bU)))
                                    : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? 0x0bU
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U))
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : 3U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 4U
                                                : 0x0bU))))))
                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                            ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                                ? ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 0U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                                    : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 0U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U))
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__reg_in_i)
                                                    ? 5U
                                                    : 4U)
                                                : 3U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 4U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))))
                                : ((5U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? 4U : ((0x0aU 
                                             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                             ? 9U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                            : 1U) : 
                                       ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                         ? 1U : 0x0bU)))
                                : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? 0x0bU
                                            : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        : 1U) : ((2U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 2U
                                                   : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  : 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                   : 0x0bU))))));
            } else if ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                if ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                        = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 0U : 9U) : 
                                   ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                     : 7U))) : ((4U 
                                                 & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                 ? 
                                                ((2U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                  : 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 4U
                                                   : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))
                                                 : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)));
                } else if ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                    if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p) 
                         & (4U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))) {
                        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx = 5U;
                    }
                } else {
                    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                        = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 0x0aU : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 8U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : 5U)) : ((2U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                   : 
                                                  ((1U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? 
                                                   ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p)
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 9U)
                                                    : 
                                                   ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p)
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 7U)))));
                }
            } else if ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                        : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : 8U) : ((1U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? 7U
                                                  : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : 6U) : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                              ? 6U : 
                                             ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                               ? 0U
                                               : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))));
            } else if ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                        ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                            : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? 1U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : 0x0aU))) : ((4U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 
                                                  ((2U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                     ? 9U
                                                     : 4U)
                                                    : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   : 
                                                  ((2U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                    : 
                                                   ((1U 
                                                     & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 1U))));
            } else if ((1U & (~ ((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)) 
                                 | (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx = 2U;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT____VlemCall_1__app_next_f 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r 
                = ((0x0000000fffffff0fULL & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT____VlemCall_1__app_next_f)) 
                      << 4U));
        }
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w))) {
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p = 1U;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__reg_in_i = 0U;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev 
                = (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                          >> 8U)));
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st 
                = (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r 
                                          >> 8U)));
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st;
            if ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                            : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : 0x0bU)))
                                    : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? 0x0bU
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U))
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : 3U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 4U
                                                : 0x0bU))))))
                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                            ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                                ? ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 0U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                                    : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 0U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U))
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__reg_in_i)
                                                    ? 5U
                                                    : 4U)
                                                : 3U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 4U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))))
                                : ((5U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? 4U : ((0x0aU 
                                             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                             ? 9U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                            : 1U) : 
                                       ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                         ? 1U : 0x0bU)))
                                : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? 0x0bU
                                            : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        : 1U) : ((2U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 2U
                                                   : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  : 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                   : 0x0bU))))));
            } else if ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                if ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                        = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 0U : 9U) : 
                                   ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                     : 7U))) : ((4U 
                                                 & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                 ? 
                                                ((2U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                  : 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 4U
                                                   : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))
                                                 : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)));
                } else if ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                    if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p) 
                         & (4U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))) {
                        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx = 5U;
                    }
                } else {
                    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                        = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 0x0aU : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 8U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : 5U)) : ((2U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                   : 
                                                  ((1U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? 
                                                   ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p)
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 9U)
                                                    : 
                                                   ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p)
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 7U)))));
                }
            } else if ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                        : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : 8U) : ((1U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? 7U
                                                  : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : 6U) : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                              ? 6U : 
                                             ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                               ? 0U
                                               : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))));
            } else if ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                        ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                            : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? 1U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : 0x0aU))) : ((4U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 
                                                  ((2U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                     ? 9U
                                                     : 4U)
                                                    : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   : 
                                                  ((2U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                    : 
                                                   ((1U 
                                                     & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 1U))));
            } else if ((1U & (~ ((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)) 
                                 | (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx = 2U;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT____VlemCall_1__app_next_f 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r 
                = ((0x0000000ffffff0ffULL & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT____VlemCall_1__app_next_f)) 
                      << 8U));
        }
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w))) {
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p = 1U;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__reg_in_i = 0U;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev 
                = (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                          >> 0x0cU)));
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st 
                = (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r 
                                          >> 0x0cU)));
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st;
            if ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                            : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : 0x0bU)))
                                    : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? 0x0bU
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U))
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : 3U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 4U
                                                : 0x0bU))))))
                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                            ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                                ? ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 0U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                                    : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 0U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U))
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__reg_in_i)
                                                    ? 5U
                                                    : 4U)
                                                : 3U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 4U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))))
                                : ((5U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? 4U : ((0x0aU 
                                             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                             ? 9U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                            : 1U) : 
                                       ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                         ? 1U : 0x0bU)))
                                : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? 0x0bU
                                            : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        : 1U) : ((2U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 2U
                                                   : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  : 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                   : 0x0bU))))));
            } else if ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                if ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                        = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 0U : 9U) : 
                                   ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                     : 7U))) : ((4U 
                                                 & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                 ? 
                                                ((2U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                  : 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 4U
                                                   : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))
                                                 : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)));
                } else if ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                    if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p) 
                         & (4U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))) {
                        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx = 5U;
                    }
                } else {
                    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                        = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 0x0aU : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 8U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : 5U)) : ((2U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                   : 
                                                  ((1U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? 
                                                   ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p)
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 9U)
                                                    : 
                                                   ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p)
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 7U)))));
                }
            } else if ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                        : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : 8U) : ((1U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? 7U
                                                  : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : 6U) : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                              ? 6U : 
                                             ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                               ? 0U
                                               : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))));
            } else if ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                        ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                            : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? 1U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : 0x0aU))) : ((4U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 
                                                  ((2U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                     ? 9U
                                                     : 4U)
                                                    : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   : 
                                                  ((2U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                    : 
                                                   ((1U 
                                                     & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 1U))));
            } else if ((1U & (~ ((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)) 
                                 | (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx = 2U;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT____VlemCall_1__app_next_f 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r 
                = ((0x0000000fffff0fffULL & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT____VlemCall_1__app_next_f)) 
                      << 0x0000000cU));
        }
        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w))) {
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p = 1U;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__reg_in_i = 0U;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev 
                = (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                          >> 0x10U)));
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st 
                = (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r 
                                          >> 0x10U)));
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st;
            if ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                            : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : 0x0bU)))
                                    : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? 0x0bU
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U))
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : 3U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 4U
                                                : 0x0bU))))))
                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                            ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                                ? ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 0U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                                    : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 0U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U))
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__reg_in_i)
                                                    ? 5U
                                                    : 4U)
                                                : 3U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 4U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))))
                                : ((5U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? 4U : ((0x0aU 
                                             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                             ? 9U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                            : 1U) : 
                                       ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                         ? 1U : 0x0bU)))
                                : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? 0x0bU
                                            : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        : 1U) : ((2U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 2U
                                                   : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  : 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                   : 0x0bU))))));
            } else if ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                if ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                        = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 0U : 9U) : 
                                   ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                     : 7U))) : ((4U 
                                                 & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                 ? 
                                                ((2U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                  : 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 4U
                                                   : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))
                                                 : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)));
                } else if ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                    if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p) 
                         & (4U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))) {
                        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx = 5U;
                    }
                } else {
                    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                        = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 0x0aU : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 8U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : 5U)) : ((2U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                   : 
                                                  ((1U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? 
                                                   ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p)
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 9U)
                                                    : 
                                                   ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p)
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 7U)))));
                }
            } else if ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                        : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : 8U) : ((1U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? 7U
                                                  : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : 6U) : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                              ? 6U : 
                                             ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                               ? 0U
                                               : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))));
            } else if ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                        ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                            : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? 1U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : 0x0aU))) : ((4U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 
                                                  ((2U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                     ? 9U
                                                     : 4U)
                                                    : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   : 
                                                  ((2U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                    : 
                                                   ((1U 
                                                     & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 1U))));
            } else if ((1U & (~ ((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)) 
                                 | (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx = 2U;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT____VlemCall_1__app_next_f 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r 
                = ((0x0000000ffff0ffffULL & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT____VlemCall_1__app_next_f)) 
                      << 0x00000010U));
        }
        if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w))) {
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p = 1U;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__reg_in_i = 0U;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev 
                = (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                          >> 0x14U)));
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st 
                = (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r 
                                          >> 0x14U)));
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st;
            if ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                            : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : 0x0bU)))
                                    : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? 0x0bU
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U))
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : 3U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 4U
                                                : 0x0bU))))))
                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                            ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                                ? ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 0U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                                    : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 0U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U))
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__reg_in_i)
                                                    ? 5U
                                                    : 4U)
                                                : 3U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 4U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))))
                                : ((5U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? 4U : ((0x0aU 
                                             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                             ? 9U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                            : 1U) : 
                                       ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                         ? 1U : 0x0bU)))
                                : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? 0x0bU
                                            : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        : 1U) : ((2U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 2U
                                                   : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  : 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                   : 0x0bU))))));
            } else if ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                if ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                        = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 0U : 9U) : 
                                   ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                     : 7U))) : ((4U 
                                                 & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                 ? 
                                                ((2U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                  : 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 4U
                                                   : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))
                                                 : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)));
                } else if ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                    if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p) 
                         & (4U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))) {
                        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx = 5U;
                    }
                } else {
                    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                        = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 0x0aU : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 8U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : 5U)) : ((2U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                   : 
                                                  ((1U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? 
                                                   ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p)
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 9U)
                                                    : 
                                                   ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p)
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 7U)))));
                }
            } else if ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                        : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : 8U) : ((1U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? 7U
                                                  : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : 6U) : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                              ? 6U : 
                                             ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                               ? 0U
                                               : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))));
            } else if ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                        ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                            : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? 1U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : 0x0aU))) : ((4U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 
                                                  ((2U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                     ? 9U
                                                     : 4U)
                                                    : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   : 
                                                  ((2U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                    : 
                                                   ((1U 
                                                     & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 1U))));
            } else if ((1U & (~ ((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)) 
                                 | (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx = 2U;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT____VlemCall_1__app_next_f 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r 
                = ((0x0000000fff0fffffULL & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT____VlemCall_1__app_next_f)) 
                      << 0x00000014U));
        }
        if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w))) {
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p = 1U;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__reg_in_i = 0U;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev 
                = (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                          >> 0x18U)));
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st 
                = (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r 
                                          >> 0x18U)));
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st;
            if ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                            : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : 0x0bU)))
                                    : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? 0x0bU
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U))
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : 3U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 4U
                                                : 0x0bU))))))
                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                            ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                                ? ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 0U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                                    : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 0U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U))
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__reg_in_i)
                                                    ? 5U
                                                    : 4U)
                                                : 3U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 4U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))))
                                : ((5U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? 4U : ((0x0aU 
                                             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                             ? 9U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                            : 1U) : 
                                       ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                         ? 1U : 0x0bU)))
                                : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? 0x0bU
                                            : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        : 1U) : ((2U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 2U
                                                   : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  : 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                   : 0x0bU))))));
            } else if ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                if ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                        = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 0U : 9U) : 
                                   ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                     : 7U))) : ((4U 
                                                 & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                 ? 
                                                ((2U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                  : 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 4U
                                                   : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))
                                                 : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)));
                } else if ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                    if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p) 
                         & (4U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))) {
                        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx = 5U;
                    }
                } else {
                    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                        = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 0x0aU : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 8U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : 5U)) : ((2U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                   : 
                                                  ((1U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? 
                                                   ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p)
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 9U)
                                                    : 
                                                   ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p)
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 7U)))));
                }
            } else if ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                        : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : 8U) : ((1U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? 7U
                                                  : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : 6U) : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                              ? 6U : 
                                             ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                               ? 0U
                                               : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))));
            } else if ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                        ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                            : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? 1U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : 0x0aU))) : ((4U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 
                                                  ((2U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                     ? 9U
                                                     : 4U)
                                                    : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   : 
                                                  ((2U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                    : 
                                                   ((1U 
                                                     & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 1U))));
            } else if ((1U & (~ ((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)) 
                                 | (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx = 2U;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT____VlemCall_1__app_next_f 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r 
                = ((0x0000000ff0ffffffULL & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT____VlemCall_1__app_next_f)) 
                      << 0x00000018U));
        }
        if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w))) {
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p = 1U;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__reg_in_i = 0U;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev 
                = (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                          >> 0x1cU)));
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st 
                = (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r 
                                          >> 0x1cU)));
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st;
            if ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                            : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : 0x0bU)))
                                    : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? 0x0bU
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U))
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : 3U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 4U
                                                : 0x0bU))))))
                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                            ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                                ? ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 0U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                                    : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 0U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U))
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__reg_in_i)
                                                    ? 5U
                                                    : 4U)
                                                : 3U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 4U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))))
                                : ((5U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? 4U : ((0x0aU 
                                             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                             ? 9U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                            : 1U) : 
                                       ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                         ? 1U : 0x0bU)))
                                : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? 0x0bU
                                            : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        : 1U) : ((2U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 2U
                                                   : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  : 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                   : 0x0bU))))));
            } else if ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                if ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                        = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 0U : 9U) : 
                                   ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                     : 7U))) : ((4U 
                                                 & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                 ? 
                                                ((2U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                  : 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 4U
                                                   : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))
                                                 : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)));
                } else if ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                    if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p) 
                         & (4U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))) {
                        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx = 5U;
                    }
                } else {
                    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                        = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 0x0aU : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 8U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : 5U)) : ((2U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                   : 
                                                  ((1U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? 
                                                   ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p)
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 9U)
                                                    : 
                                                   ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p)
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 7U)))));
                }
            } else if ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                        : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : 8U) : ((1U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? 7U
                                                  : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : 6U) : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                              ? 6U : 
                                             ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                               ? 0U
                                               : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))));
            } else if ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                        ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                            : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? 1U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : 0x0aU))) : ((4U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 
                                                  ((2U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                     ? 9U
                                                     : 4U)
                                                    : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   : 
                                                  ((2U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                    : 
                                                   ((1U 
                                                     & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 1U))));
            } else if ((1U & (~ ((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)) 
                                 | (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx = 2U;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT____VlemCall_1__app_next_f 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r 
                = ((0x0000000f0fffffffULL & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT____VlemCall_1__app_next_f)) 
                      << 0x0000001cU));
        }
        if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w))) {
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p = 1U;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__reg_in_i = 0U;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev 
                = (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                          >> 0x20U)));
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st 
                = (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r 
                                          >> 0x20U)));
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st;
            if ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                            : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : 0x0bU)))
                                    : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? 0x0bU
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U))
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : 3U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 4U
                                                : 0x0bU))))))
                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                            ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                                ? ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 0U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 5U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                                    : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 0U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                : 5U))
                                        : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__reg_in_i)
                                                    ? 5U
                                                    : 4U)
                                                : 3U)
                                            : ((1U 
                                                & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                ? 4U
                                                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))))
                                : ((5U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? 4U : ((0x0aU 
                                             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                             ? 9U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                            : 1U) : 
                                       ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                         ? 1U : 0x0bU)))
                                : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                            ? 0x0bU
                                            : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        : 1U) : ((2U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 2U
                                                   : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  : 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                   : 0x0bU))))));
            } else if ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                if ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                        = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 0U : 9U) : 
                                   ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                     : 7U))) : ((4U 
                                                 & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                 ? 
                                                ((2U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                  : 
                                                 ((1U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 4U
                                                   : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))
                                                 : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)));
                } else if ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                    if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p) 
                         & (4U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))) {
                        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx = 5U;
                    }
                } else {
                    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                        = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 0x0aU : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? 8U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : 5U)) : ((2U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                   : 
                                                  ((1U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? 
                                                   ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p)
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 9U)
                                                    : 
                                                   ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__p2p)
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 7U)))));
                }
            } else if ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))
                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                        : ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                        ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                        : 8U) : ((1U 
                                                  & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                  ? 7U
                                                  : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))
                            : ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : 6U) : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                              ? 6U : 
                                             ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                               ? 0U
                                               : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))))));
            } else if ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__ev))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx 
                    = ((8U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                        ? ((4U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                            ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                            : ((2U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                ? ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? 1U : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                : ((1U & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                    : 0x0aU))) : ((4U 
                                                   & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   ? 
                                                  ((2U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? 
                                                   ((1U 
                                                     & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                     ? 9U
                                                     : 4U)
                                                    : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                   : 
                                                  ((2U 
                                                    & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                    : 
                                                   ((1U 
                                                     & (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st))
                                                     ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)
                                                     : 1U))));
            } else if ((1U & (~ ((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)) 
                                 | (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__st)))))) {
                __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx = 2U;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT____VlemCall_1__app_next_f 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_next_f__36__nx;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r 
                = ((0x00000000ffffffffULL & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT____VlemCall_1__app_next_f)) 
                      << 0x00000020U));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__tctx_w0_wr_w) 
             & (IData)(vlSelfRef.milan_datapath__DOT__tctx_wr_rdy_w))) {
            if ((0U == (7U & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r) 
                              >> 4U)))) {
                __Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c 
                    = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_data_r 
                                      >> 1U));
                vlSelfRef.milan_datapath__DOT____VlemCall_14__aaf_chn_clamp 
                    = ((2U > (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                        ? 2U : ((8U <= (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                 ? 8U : (0x0000000fU 
                                         & ((1U & (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                             ? ((IData)(1U) 
                                                + (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                             : (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c)))));
                vlSelfRef.__VdlyVal__milan_datapath__DOT__tctx_chans_r__v0 
                    = vlSelfRef.milan_datapath__DOT____VlemCall_14__aaf_chn_clamp;
                vlSelfRef.__VdlySet__milan_datapath__DOT__tctx_chans_r__v0 = 1U;
            }
            if ((1U == (7U & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r) 
                              >> 4U)))) {
                __Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c 
                    = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_data_r 
                                      >> 1U));
                vlSelfRef.milan_datapath__DOT____VlemCall_14__aaf_chn_clamp 
                    = ((2U > (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                        ? 2U : ((8U <= (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                 ? 8U : (0x0000000fU 
                                         & ((1U & (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                             ? ((IData)(1U) 
                                                + (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                             : (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c)))));
                vlSelfRef.__VdlyVal__milan_datapath__DOT__tctx_chans_r__v1 
                    = vlSelfRef.milan_datapath__DOT____VlemCall_14__aaf_chn_clamp;
                vlSelfRef.__VdlySet__milan_datapath__DOT__tctx_chans_r__v1 = 1U;
            }
            if ((2U == (7U & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r) 
                              >> 4U)))) {
                __Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c 
                    = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_data_r 
                                      >> 1U));
                vlSelfRef.milan_datapath__DOT____VlemCall_14__aaf_chn_clamp 
                    = ((2U > (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                        ? 2U : ((8U <= (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                 ? 8U : (0x0000000fU 
                                         & ((1U & (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                             ? ((IData)(1U) 
                                                + (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                             : (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c)))));
                vlSelfRef.__VdlyVal__milan_datapath__DOT__tctx_chans_r__v2 
                    = vlSelfRef.milan_datapath__DOT____VlemCall_14__aaf_chn_clamp;
                vlSelfRef.__VdlySet__milan_datapath__DOT__tctx_chans_r__v2 = 1U;
            }
            if ((3U == (7U & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r) 
                              >> 4U)))) {
                __Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c 
                    = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_data_r 
                                      >> 1U));
                vlSelfRef.milan_datapath__DOT____VlemCall_14__aaf_chn_clamp 
                    = ((2U > (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                        ? 2U : ((8U <= (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                 ? 8U : (0x0000000fU 
                                         & ((1U & (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                             ? ((IData)(1U) 
                                                + (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                             : (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c)))));
                vlSelfRef.__VdlyVal__milan_datapath__DOT__tctx_chans_r__v3 
                    = vlSelfRef.milan_datapath__DOT____VlemCall_14__aaf_chn_clamp;
                vlSelfRef.__VdlySet__milan_datapath__DOT__tctx_chans_r__v3 = 1U;
            }
            if ((4U == (7U & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r) 
                              >> 4U)))) {
                __Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c 
                    = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_data_r 
                                      >> 1U));
                vlSelfRef.milan_datapath__DOT____VlemCall_14__aaf_chn_clamp 
                    = ((2U > (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                        ? 2U : ((8U <= (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                 ? 8U : (0x0000000fU 
                                         & ((1U & (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                             ? ((IData)(1U) 
                                                + (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                             : (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c)))));
                vlSelfRef.__VdlyVal__milan_datapath__DOT__tctx_chans_r__v4 
                    = vlSelfRef.milan_datapath__DOT____VlemCall_14__aaf_chn_clamp;
                vlSelfRef.__VdlySet__milan_datapath__DOT__tctx_chans_r__v4 = 1U;
            }
            if ((5U == (7U & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r) 
                              >> 4U)))) {
                __Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c 
                    = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_data_r 
                                      >> 1U));
                vlSelfRef.milan_datapath__DOT____VlemCall_14__aaf_chn_clamp 
                    = ((2U > (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                        ? 2U : ((8U <= (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                 ? 8U : (0x0000000fU 
                                         & ((1U & (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                             ? ((IData)(1U) 
                                                + (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                             : (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c)))));
                vlSelfRef.__VdlyVal__milan_datapath__DOT__tctx_chans_r__v5 
                    = vlSelfRef.milan_datapath__DOT____VlemCall_14__aaf_chn_clamp;
                vlSelfRef.__VdlySet__milan_datapath__DOT__tctx_chans_r__v5 = 1U;
            }
            if ((6U == (7U & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r) 
                              >> 4U)))) {
                __Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c 
                    = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_data_r 
                                      >> 1U));
                vlSelfRef.milan_datapath__DOT____VlemCall_14__aaf_chn_clamp 
                    = ((2U > (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                        ? 2U : ((8U <= (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                 ? 8U : (0x0000000fU 
                                         & ((1U & (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                             ? ((IData)(1U) 
                                                + (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                             : (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c)))));
                vlSelfRef.__VdlyVal__milan_datapath__DOT__tctx_chans_r__v6 
                    = vlSelfRef.milan_datapath__DOT____VlemCall_14__aaf_chn_clamp;
                vlSelfRef.__VdlySet__milan_datapath__DOT__tctx_chans_r__v6 = 1U;
            }
            if ((7U == (7U & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r) 
                              >> 4U)))) {
                __Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c 
                    = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_data_r 
                                      >> 1U));
                vlSelfRef.milan_datapath__DOT____VlemCall_14__aaf_chn_clamp 
                    = ((2U > (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                        ? 2U : ((8U <= (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                 ? 8U : (0x0000000fU 
                                         & ((1U & (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                             ? ((IData)(1U) 
                                                + (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c))
                                             : (IData)(__Vfunc_milan_datapath__DOT__aaf_chn_clamp__16__c)))));
                vlSelfRef.__VdlyVal__milan_datapath__DOT__tctx_chans_r__v7 
                    = vlSelfRef.milan_datapath__DOT____VlemCall_14__aaf_chn_clamp;
                vlSelfRef.__VdlySet__milan_datapath__DOT__tctx_chans_r__v7 = 1U;
            }
        }
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
        vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psfault_sync_r 
            = ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psfault_sync_r) 
                      << 1U)) | (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_fault_ps_r));
        vlSelfRef.__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psbusy_sync_r 
            = ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psbusy_sync_r) 
                      << 1U)) | (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_busy_ps_r));
        if (vlSelfRef.milan_datapath__DOT__rsp_tvalid_w) {
            if ((8U > (IData)(vlSelfRef.milan_datapath__DOT__rsp_tuser_w))) {
                if ((8U > (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__chpos_r))) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0 
                        = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp0_w;
                    vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0 
                        = (7U & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__chpos_r));
                    vlSelfRef.__VdlyDim1__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0 
                        = (7U & (IData)(vlSelfRef.milan_datapath__DOT__rsp_tuser_w));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0 = 1U;
                }
                if ((8U > (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__ch1_w))) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1 
                        = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp1_w;
                    vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1 
                        = (7U & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__ch1_w));
                    vlSelfRef.__VdlyDim1__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1 
                        = (7U & (IData)(vlSelfRef.milan_datapath__DOT__rsp_tuser_w));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1 = 1U;
                }
            }
        }
        if (vlSelfRef.milan_datapath__DOT__aafcap_pv_w) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r__v0 
                = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aafcap_l_w)) 
                    << 0x00000018U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aafcap_r_w)));
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r__v0 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__wing_route_we_r) 
             & (8U > (IData)(vlSelfRef.milan_datapath__DOT__wing_idx_r)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__pcm_route__DOT__route_r__v0 
                = (2U & (IData)(vlSelfRef.milan_datapath__DOT__wing_route_r));
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__pcm_route__DOT__route_r__v0 
                = (7U & (IData)(vlSelfRef.milan_datapath__DOT__wing_idx_r));
            vlSelfRef.__VdlySet__milan_datapath__DOT__pcm_route__DOT__route_r__v0 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__wing_tbl_we_r) 
             & (8U > (IData)(vlSelfRef.milan_datapath__DOT__wing_idx_r)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0 
                = vlSelfRef.milan_datapath__DOT__wing_en_r;
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0 
                = (7U & (IData)(vlSelfRef.milan_datapath__DOT__wing_idx_r));
            vlSelfRef.__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0 = 1U;
            vlSelfRef.__VdlyVal__milan_datapath__DOT__stream_table__DOT__ovr_sid_r__v0 
                = vlSelfRef.milan_datapath__DOT__wing_sid_r;
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__stream_table__DOT__ovr_sid_r__v0 
                = (7U & (IData)(vlSelfRef.milan_datapath__DOT__wing_idx_r));
            vlSelfRef.__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_sid_r__v0 = 1U;
            vlSelfRef.__VdlyVal__milan_datapath__DOT__stream_table__DOT__ovr_armed_r__v0 
                = (1U & (~ ((~ (IData)(vlSelfRef.milan_datapath__DOT__wing_en_r)) 
                            & (0ULL == vlSelfRef.milan_datapath__DOT__wing_sid_r))));
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__stream_table__DOT__ovr_armed_r__v0 
                = (7U & (IData)(vlSelfRef.milan_datapath__DOT__wing_idx_r));
            vlSelfRef.__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_armed_r__v0 = 1U;
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
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_take_w) 
             & (4U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v16 
                = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[4U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v16 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_dry_w) 
             & (4U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v20 = 1U;
        }
        if ((((0x0001869fU == vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ms_div_r) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[4U]))) 
             & vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[4U])) {
            if ((0x64U != vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[4U])) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v25 
                    = (0x0000007fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[4U])));
                vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v25 = 1U;
            } else {
                vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__converged_r__v25 = 1U;
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_recentre_p_w) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[4U])))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__pend_r__v18 = 1U;
        }
        if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
                    >> 4U) | ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_moved_w) 
                              & (4U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                                 [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v19 
                = (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
                    & (4U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                       [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))
                    ? (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w)
                    : vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[4U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v19 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_take_w) 
             & (5U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v20 
                = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[5U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v20 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_dry_w) 
             & (5U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v25 = 1U;
        }
        if ((((0x0001869fU == vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ms_div_r) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[5U]))) 
             & vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[5U])) {
            if ((0x64U != vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[5U])) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v31 
                    = (0x0000007fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[5U])));
                vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v31 = 1U;
            } else {
                vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__converged_r__v31 = 1U;
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_recentre_p_w) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[5U])))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__pend_r__v22 = 1U;
        }
        if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
                    >> 5U) | ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_moved_w) 
                              & (5U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                                 [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v23 
                = (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
                    & (5U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                       [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))
                    ? (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w)
                    : vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[5U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v23 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_take_w) 
             & (6U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v24 
                = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[6U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v24 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_dry_w) 
             & (6U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v30 = 1U;
        }
        if ((((0x0001869fU == vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ms_div_r) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[6U]))) 
             & vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[6U])) {
            if ((0x64U != vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[6U])) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v37 
                    = (0x0000007fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[6U])));
                vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v37 = 1U;
            } else {
                vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__converged_r__v37 = 1U;
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_recentre_p_w) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[6U])))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__pend_r__v26 = 1U;
        }
        if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
                    >> 6U) | ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_moved_w) 
                              & (6U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                                 [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v27 
                = (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
                    & (6U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                       [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))
                    ? (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w)
                    : vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[6U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v27 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_take_w) 
             & (7U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v28 
                = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[7U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v28 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_dry_w) 
             & (7U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v35 = 1U;
        }
        if ((((0x0001869fU == vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ms_div_r) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[7U]))) 
             & vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[7U])) {
            if ((0x64U != vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[7U])) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v43 
                    = (0x0000007fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[7U])));
                vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v43 = 1U;
            } else {
                vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__converged_r__v43 = 1U;
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_recentre_p_w) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[7U])))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__pend_r__v30 = 1U;
        }
        if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
                    >> 7U) | ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_moved_w) 
                              & (7U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                                 [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v31 
                = (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
                    & (7U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                       [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))
                    ? (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w)
                    : vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[7U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v31 = 1U;
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
        if (((IData)(vlSelfRef.milan_datapath__DOT__amap_edit_owr_p_r) 
             | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_wr_p) 
                & ((~ (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_owr_p_r)) 
                   & ((~ (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_txn_active_r)) 
                      & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__lk_held_r)) 
                         & (vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_sel 
                            >> 8U))))))) {
            if (vlSelfRef.milan_datapath__DOT__amap_edit_owr_p_r) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__map_r__v0 
                    = vlSelfRef.milan_datapath__DOT__amap_edit_owr_word_r;
                vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__map_r__v0 
                    = (0x0000003fU & (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_owr_slot_r));
            } else {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__map_r__v0 
                    = vlSelfRef.milan_datapath__DOT__cfg_cmap_entry_w;
                vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__map_r__v0 
                    = (0x0000003fU & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_sel);
            }
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__map_r__v0 = 1U;
        }
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r 
            = ((1U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__xs_r))
                ? ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r) 
                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r))
                : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_pcp_r 
            = (0x000001ffU & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_pcp_r) 
                               & (~ ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_code_w))
                                      ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_disp_w)
                                      : 0U))) | (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_domain_change_w)))));
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
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__en_q_r = 0x01ffU;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_v_w = 0U;
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_v_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_v_w = 1U;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_v_w = 0U;
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_v_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_v_w = 1U;
        }
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
             & (9U > (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w)))) {
            if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w))) {
                vlSelfRef.milan_datapath__DOT__talker_diag__DOT__mr_q_r 
                    = (((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w))) 
                        & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__mr_q_r)) 
                       | (0x01ffU & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_mr_i) 
                                     << (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w))));
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
        if ((8U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__aidx_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgrant_r = 0U;
            VL_ASSIGN_W(288, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r, Vmilan_datapath__ConstPool__CONST_h9a2fc1c8_0);
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
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[5U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[5U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[6U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[6U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[7U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[7U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[8U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[8U];
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
                __Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__306__n 
                    = ((IData)(3U) + (0x0000003fU & 
                                      ((IData)(2U) 
                                       + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off))));
                __Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__306__Vfuncout 
                    = ((0x01bfU >= (0x000001ffU & (
                                                   ((IData)(0x01bfU) 
                                                    - 
                                                    (__Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__306__n 
                                                     << 3U)) 
                                                   - (IData)(7U))))
                        ? (0x000000ffU & (((0U == (0x0000001fU 
                                                   & (((IData)(0x01bfU) 
                                                       - 
                                                       (__Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__306__n 
                                                        << 3U)) 
                                                      - (IData)(7U))))
                                            ? 0U : 
                                           (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                            [(((IData)(7U) 
                                               + (0x000001ffU 
                                                  & (((IData)(0x01bfU) 
                                                      - 
                                                      (__Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__306__n 
                                                       << 3U)) 
                                                     - (IData)(7U)))) 
                                              >> 5U)] 
                                            << ((IData)(0x00000020U) 
                                                - (0x0000001fU 
                                                   & (((IData)(0x01bfU) 
                                                       - 
                                                       (__Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__306__n 
                                                        << 3U)) 
                                                      - (IData)(7U)))))) 
                                          | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                             [(0x0000000fU 
                                               & ((((IData)(0x01bfU) 
                                                    - 
                                                    (__Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__306__n 
                                                     << 3U)) 
                                                   - (IData)(7U)) 
                                                  >> 5U))] 
                                             >> (0x0000001fU 
                                                 & (((IData)(0x01bfU) 
                                                     - 
                                                     (__Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__306__n 
                                                      << 3U)) 
                                                    - (IData)(7U))))))
                        : 0U);
                vlSelfRef.milan_datapath__DOT__avtprx_b3 
                    = __Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__306__Vfuncout;
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
                            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w))) {
                                vlSelfRef.milan_datapath__DOT__avtprx_unlocked_c 
                                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w;
                            }
                            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w)))) {
                                vlSelfRef.milan_datapath__DOT__avtprx_locked_c 
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
                        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w))) {
                            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w)))) {
                                vlSelfRef.milan_datapath__DOT__avtprx_last_tsd 
                                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w;
                            }
                        }
                        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w) 
                                      >> 1U)))) {
                            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w))) {
                                vlSelfRef.milan_datapath__DOT__avtprx_last_ts 
                                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w;
                            }
                        }
                    }
                }
            }
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_q_r 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_cnt_r 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w = 0U;
        if (((3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w) 
             != (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                = ((0x0003fffcU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r) 
                   | (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w));
        }
        if (((3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w 
                    >> 2U)) != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                                      >> 2U)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                = ((0x0003fff3U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r) 
                   | (0x0000000cU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w));
        }
        if (((3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w 
                    >> 4U)) != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                                      >> 4U)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                = ((0x0003ffcfU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r) 
                   | (0x00000030U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w));
        }
        if (((3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w 
                    >> 6U)) != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                                      >> 6U)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                = ((0x0003ff3fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r) 
                   | (0x000000c0U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w));
        }
        if (((3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w 
                    >> 8U)) != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                                      >> 8U)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                = ((0x0003fcffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r) 
                   | (0x00000300U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w 
                = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w));
        }
        if (((3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w 
                    >> 0x0aU)) != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                                         >> 0x0aU)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                = ((0x0003f3ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r) 
                   | (0x00000c00U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w 
                = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w));
        }
        if (((3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w 
                    >> 0x0cU)) != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                                         >> 0x0cU)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                = ((0x0003cfffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r) 
                   | (0x00003000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w 
                = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w));
        }
        if (((3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w 
                    >> 0x0eU)) != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                                         >> 0x0eU)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                = ((0x00033fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r) 
                   | (0x0000c000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w 
                = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w));
        }
        if (((3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w 
                    >> 0x10U)) != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                                         >> 0x10U)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                = ((0x0000ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r) 
                   | (0x00030000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w 
                = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_notify__ev_amap_i) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__amap_type_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__amap_index_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w;
        if (vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_go_w) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_armed_r = 1U;
            vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_unsup_r = 0U;
        }
        vlSelfRef.milan_datapath__DOT__lb_dup_cnt_w 
            = ((0x00010000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__dup_sum_w)
                ? 0x0000ffffU : (0x0000ffffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__dup_sum_w));
        vlSelfRef.milan_datapath__DOT__lb_skip_cnt_w 
            = ((0x00010000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skip_sum_w)
                ? 0x0000ffffU : (0x0000ffffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skip_sum_w));
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
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w = 0U;
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ind_reg_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w 
                    = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w));
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
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 4U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ind_reg_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w 
                    = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w));
            }
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 5U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ind_reg_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w 
                    = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w));
            }
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 6U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ind_reg_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w 
                    = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w));
            }
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 7U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ind_reg_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w 
                    = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w));
            }
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 8U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ind_reg_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w 
                    = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w));
            }
        }
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
                                    if ((8U >= (0x0000000fU 
                                                & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i)))) {
                                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r 
                                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r) 
                                               | (0x01ffU 
                                                  & ((IData)(1U) 
                                                     << 
                                                     (0x0000000fU 
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
        vlSelfRef.milan_datapath__DOT__mon_wire_chans_w 
            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r
            [(7U & (IData)(vlSelfRef.milan_datapath__DOT__route_render_sel_w))];
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reload_ok_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_acc_r = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reload_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rl_ref_r 
                = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reload_ok_w)));
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_valid_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_send_valid_w = 0U;
        if (vlSelfRef.milan_datapath__DOT__lb_tap_tvalid_w) {
            if (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__stash_open_w) {
                vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__stash_strm_r 
                    = vlSelfRef.milan_datapath__DOT__lb_tap_tuser_w;
            }
        }
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
        if ((vlSelfRef.milan_datapath__DOT__crft_count_w 
             != vlSelfRef.milan_datapath__DOT__tkd_crfq_r)) {
            vlSelfRef.milan_datapath__DOT__tkd_crf_pend_r = 1U;
        } else if (vlSelfRef.milan_datapath__DOT__tkd_crf_p_w) {
            vlSelfRef.milan_datapath__DOT__tkd_crf_pend_r = 0U;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__arm_q_slot_r 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w;
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
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_next__68__s 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__sel_r;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_next__68__Vfuncout 
                = ((0x1fU == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_next__68__s))
                    ? 0U : (0x0000001fU & ((IData)(1U) 
                                           + (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_next__68__s))));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__ptr_r 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_next__68__Vfuncout;
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
                            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__owner_r__v0 
                                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__owner_r;
                            vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__owner_r__v0 
                                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__free_ix_w;
                            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__owner_r__v0 = 1U;
                            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_r__v0 
                                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r
                                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__owner_r];
                            vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_r__v0 
                                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__free_ix_w;
                            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_r__v0 = 1U;
                            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r__v0 
                                = (0x0000ffffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r
                                                            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__owner_r])));
                            vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r__v0 
                                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__owner_r;
                            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r__v0[0U] 
                                = (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__ctlr_mac_r);
                            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r__v0[1U] 
                                = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__ctlr_eid_r) 
                                    << 0x00000010U) 
                                   | (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__ctlr_mac_r 
                                              >> 0x00000020U)));
                            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r__v0[2U] 
                                = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__ctlr_eid_r) 
                                    >> 0x00000010U) 
                                   | ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__ctlr_eid_r 
                                               >> 0x00000020U)) 
                                      << 0x00000010U));
                            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r__v0[3U] 
                                = ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__ctlr_eid_r 
                                            >> 0x00000020U)) 
                                   >> 0x00000010U);
                            vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r__v0 
                                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__free_ix_w;
                            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r__v0 = 1U;
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
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__exp_fire_w) 
             & ((0x20U <= (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__sweep_rdata_r 
                                                  >> 0x00000020U)))) 
                & (0x29U > (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__sweep_rdata_r 
                                                   >> 0x00000020U))))))) {
            if ((8U >= (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__sweep_rdata_r 
                                               >> 0x00000020U))))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pendexp_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pendexp_r) 
                       | (0x01ffU & ((IData)(1U) << 
                                     (0x0000000fU & (IData)(
                                                            (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__sweep_rdata_r 
                                                             >> 0x00000020U))))));
            }
        }
        if (((8U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__xs_r)) 
             & ((0x0aU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__cur_act_w)) 
                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__apend_r 
                   >> 0x0000000aU)))) {
            if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pendexp_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pendexp_r));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pend_any_w) 
             & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_279))) {
            if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pend_sink_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pendexp_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pend_sink_w))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pendexp_r));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_pend2) 
             | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_done_w))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__r_valid = 1U;
        } else if (vlSelfRef.s_axi_rready) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__r_valid = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__alloc_gnt_o) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__writing_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__writing_r) 
                   | (0x0fU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_slot_w))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_active_r = 1U;
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
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r) {
                if ((8U >= (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r 
                        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r) 
                           | (0x01ffU & ((IData)(1U) 
                                         << (0x0000000fU 
                                             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))));
                }
            } else if ((8U >= (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r 
                    = ((~ ((IData)(1U) << (0x0000000fU 
                                           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r));
            }
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
        if ((0x00000020U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w) 
                            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r 
                = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r));
        }
        if ((0x00000040U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w) 
                            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r 
                = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r));
        }
        if ((0x00000080U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w) 
                            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r 
                = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r));
        }
        if ((0x00000100U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w) 
                            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r 
                = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r));
        }
        if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_port_w)) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w))) {
            if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_sink_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_sink_w))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r));
            }
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
                = (0x0000007fU & ((IData)(0x47U) + Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
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
                 & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_18))) {
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
                       - (IData)(0x00000047U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__need_draw_r 
                    = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__need_draw_r));
            } else if ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                              - (IData)(0x00000047U)))) {
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
            if ((0x00000020U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_f_r) 
                                | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__ftx_r__v5 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ftx_r[5U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__ftx_r__v5 = 1U;
            }
            if ((0x00000020U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
                                | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v5 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__tuiv_r[5U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v5 = 1U;
            }
            if ((0x00000020U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_mr_r) 
                                | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__mreset_r__v5 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__mreset_r[5U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v5 = 1U;
            }
            if ((0x00000020U & ((((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_f_r) 
                                  | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)) 
                                 | ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
                                    | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w))) 
                                | ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_mr_r) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w))))) {
                vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                    = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
            }
            if ((0x00000040U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_f_r) 
                                | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__ftx_r__v6 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ftx_r[6U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__ftx_r__v6 = 1U;
            }
            if ((0x00000040U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
                                | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v6 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__tuiv_r[6U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v6 = 1U;
            }
            if ((0x00000040U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_mr_r) 
                                | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__mreset_r__v6 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__mreset_r[6U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v6 = 1U;
            }
            if ((0x00000040U & ((((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_f_r) 
                                  | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)) 
                                 | ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
                                    | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w))) 
                                | ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_mr_r) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w))))) {
                vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                    = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
            }
            if ((0x00000080U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_f_r) 
                                | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__ftx_r__v7 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ftx_r[7U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__ftx_r__v7 = 1U;
            }
            if ((0x00000080U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
                                | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v7 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__tuiv_r[7U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v7 = 1U;
            }
            if ((0x00000080U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_mr_r) 
                                | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__mreset_r__v7 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__mreset_r[7U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v7 = 1U;
            }
            if ((0x00000080U & ((((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_f_r) 
                                  | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)) 
                                 | ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
                                    | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w))) 
                                | ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_mr_r) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w))))) {
                vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                    = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
            }
            if ((0x00000100U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_f_r) 
                                | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__ftx_r__v8 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ftx_r[8U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__ftx_r__v8 = 1U;
            }
            if ((0x00000100U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
                                | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v8 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__tuiv_r[8U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v8 = 1U;
            }
            if ((0x00000100U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_mr_r) 
                                | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__mreset_r__v8 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__mreset_r[8U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v8 = 1U;
            }
            if ((0x00000100U & ((((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_f_r) 
                                  | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)) 
                                 | ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
                                    | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w))) 
                                | ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_mr_r) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w))))) {
                vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                    = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
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
                = ((0x01feU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r)) 
                   | (1U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r 
                = ((0x01feU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r)) 
                   | (1U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r 
                = ((0x01feU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r)) 
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
                = ((0x01fdU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r)) 
                   | (2U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r 
                = ((0x01fdU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r)) 
                   | (2U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r 
                = ((0x01fdU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r)) 
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
                = ((0x01fbU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r)) 
                   | (4U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r 
                = ((0x01fbU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r)) 
                   | (4U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r 
                = ((0x01fbU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r)) 
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
                = ((0x01f7U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r)) 
                   | (8U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r 
                = ((0x01f7U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r)) 
                   | (8U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r 
                = ((0x01f7U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r)) 
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
        if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                    >> 4U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r) 
                                 >> 4U))))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__start_r__v4 
                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__start_r[4U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v4 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r 
                = ((0x01efU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r)) 
                   | (0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r 
                = ((0x01efU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r)) 
                   | (0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r 
                = ((0x01efU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r)) 
                   | (0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w)));
            vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
        } else if ((1U & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                              >> 4U)) & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r) 
                                         >> 4U)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__stop_r__v4 
                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__stop_r[4U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v4 = 1U;
            vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
        }
        if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                    >> 5U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r) 
                                 >> 5U))))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__start_r__v5 
                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__start_r[5U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v5 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r 
                = ((0x01dfU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r)) 
                   | (0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r 
                = ((0x01dfU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r)) 
                   | (0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r 
                = ((0x01dfU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r)) 
                   | (0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w)));
            vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
        } else if ((1U & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                              >> 5U)) & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r) 
                                         >> 5U)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__stop_r__v5 
                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__stop_r[5U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v5 = 1U;
            vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
        }
        if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                    >> 6U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r) 
                                 >> 6U))))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__start_r__v6 
                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__start_r[6U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v6 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r 
                = ((0x01bfU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r)) 
                   | (0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r 
                = ((0x01bfU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r)) 
                   | (0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r 
                = ((0x01bfU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r)) 
                   | (0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w)));
            vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
        } else if ((1U & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                              >> 6U)) & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r) 
                                         >> 6U)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__stop_r__v6 
                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__stop_r[6U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v6 = 1U;
            vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
        }
        if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                    >> 7U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r) 
                                 >> 7U))))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__start_r__v7 
                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__start_r[7U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v7 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r 
                = ((0x017fU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r)) 
                   | (0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r 
                = ((0x017fU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r)) 
                   | (0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r 
                = ((0x017fU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r)) 
                   | (0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w)));
            vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
        } else if ((1U & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                              >> 7U)) & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r) 
                                         >> 7U)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__stop_r__v7 
                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__stop_r[7U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v7 = 1U;
            vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                      >> 8U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r) 
                                   >> 8U))))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__start_r__v8 
                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__start_r[8U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v8 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r 
                = ((0x00ffU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r)) 
                   | (0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r 
                = ((0x00ffU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r)) 
                   | (0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r 
                = ((0x00ffU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r)) 
                   | (0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w)));
            vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
        } else if ((IData)(((~ ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                >> 8U)) & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r) 
                                           >> 8U)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__stop_r__v8 
                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__stop_r[8U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v8 = 1U;
            vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
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
            if ((0x5fU >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r))) {
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
            if ((0x5fU >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w))) {
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
             & ((8U >= (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                       - (IData)(1U)))) 
                && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r) 
                          >> (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                             - (IData)(1U)))))))) {
            if ((8U >= (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                       - (IData)(1U))))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_evt_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_evt_r) 
                       | (0x01ffU & ((IData)(1U) << 
                                     (0x0000000fU & 
                                      ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                       - (IData)(1U))))));
            }
        }
        if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_evt_w)))) {
            if ((5U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w) {
                    if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_sink_w))) {
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
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w))) 
             & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w)) 
                | (0x0aU != (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (0x01feU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w) 
                    >> 1U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 1U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                              >> 4U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (0x01fdU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w) 
                    >> 2U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 2U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                              >> 8U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (0x01fbU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w) 
                    >> 3U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 3U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                              >> 0x0cU))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (0x01f7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w) 
                    >> 4U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 4U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                              >> 0x10U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (0x01efU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w) 
                    >> 5U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 5U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                              >> 0x14U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (0x01dfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w) 
                    >> 6U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 6U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                              >> 0x18U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (0x01bfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w) 
                    >> 7U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 7U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                              >> 0x1cU))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        } else if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (0x017fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w) 
                    >> 8U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 8U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                              >> 0x20U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        } else if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (0x00ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        }
    } else {
        vlSelfRef.__Vdly__milan_datapath__DOT__i2spb_overruns = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_rec_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_wr_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v30 = 1U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r__v1 = 1U;
        vlSelfRef.milan_datapath__DOT__pcmrx_drops = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v34 = 1U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__stat_snap__v18 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__run_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_valid_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_last_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__fetch_idx_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__ptp_clock_validity__DOT__hold_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_st_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_idx_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_assem_r = 0ULL;
        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v8 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_valid_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__tmo_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid__v1 = 1U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v33 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_valid_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r__v2 = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_adp_r = 0U;
        vlSelfRef.milan_datapath__DOT__tdm_dup_cnt_w = 0U;
        vlSelfRef.milan_datapath__DOT__tdm_skip_cnt_w = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__media_clock_restart__DOT__tgt_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__mcr_mr_v_w = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v19 = 1U;
        vlSelfRef.milan_datapath__DOT__txarb_abort_sticky_r = 0U;
        vlSelfRef.milan_datapath__DOT__txarb_stall_sticky_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v8 = 1U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v7 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__held_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__release_pend_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v8 = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_wp_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r = 0ULL;
        vlSelfRef.__VdlySet__milan_datapath__DOT__tctx_chans_r__v8 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_st_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_idx_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_eid_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psfault_sync_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psbusy_sync_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__cur_r__v2 = 1U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r__v1 = 1U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pcm_route__DOT__route_r__v1 = 1U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v1 = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v32 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_alloc_wait_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_sid_r__v1 = 1U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__map_r__v1 = 1U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_armed_r__v1 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_pcp_r = 0U;
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
        VL_ASSIGN_W(288, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r, Vmilan_datapath__ConstPool__CONST_h9a2fc1c8_0);
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
        vlSelfRef.milan_datapath__DOT__avtprx_late_c = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_early_c = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_mreset_c = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_q_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_cnt_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_id_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_id_r = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__b_valid = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__amap_type_r = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_tu_bit = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_fsh2 = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_armed_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_unsup_r = 0U;
        vlSelfRef.milan_datapath__DOT__lb_dup_cnt_w = 0U;
        vlSelfRef.milan_datapath__DOT__lb_skip_cnt_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vpushed_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__pending_r = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_fsh = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_busy_r = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_ts = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__arm_ref_r = 0U;
        vlSelfRef.milan_datapath__DOT__crf_delta_w = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_last_tsd = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_last_ts = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rd_data_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__avtprx_tu_c = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_unsupp_c = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_frx_c = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_seqmm_c = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_intr_c = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_unlocked_c = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_locked_c = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__cfg_v_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ifg = 0x0000000cU;
        vlSelfRef.milan_datapath__DOT__csr__DOT__lpf_ctrl = 1U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__irq_mask = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__amap_index_r = 0U;
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
        vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_vid = 2U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__adp_midhi = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__adp_idx0 = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__adp_midlo = 0U;
        vlSelfRef.milan_datapath__DOT__mon_wire_chans_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_acc_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__crf_ctrl = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rl_ref_r = 0U;
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
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__stash_strm_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_owner_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_slot_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_deadline_w = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__parsed = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ahi = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__mac_alo = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_r = 1ULL;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__seeded_r = 0U;
        vlSelfRef.milan_datapath__DOT__crf_rx__DOT__prev_mr_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__tx_dead_r = 0U;
        vlSelfRef.milan_datapath__DOT__link_guard__DOT__tx_alive_r = 1U;
        vlSelfRef.milan_datapath__DOT__tkd_crf_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__arm_q_slot_r = 0U;
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
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pendexp_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__r_valid = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_prefer_aecp_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_active_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_release_slot_w = 0U;
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
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__seq_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__verdict_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_active_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__exp_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aprb__DOT__aprb_sid_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aprb__DOT__aprb_hit_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aprb__DOT__aprb_idx_r = 0U;
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
        vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v9 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r = 0U;
        vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v19 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__retried_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__await_tx_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__armed_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__armed_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__armed_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_evt_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_waddr_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_pend_r = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r = 0U;
    }
    if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_w) 
         & ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r)) 
            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_ix_r)))) {
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r__v0[0U] 
            = (IData)(vlSelfRef.i_desc_mem_rsp_data);
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r__v0[1U] 
            = (IData)((vlSelfRef.i_desc_mem_rsp_data 
                       >> 0x00000020U));
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r__v0[2U] 
            = (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_b0_r);
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r__v0[3U] 
            = (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_b0_r 
                       >> 0x00000020U));
        vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r__v0 
            = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_ix_r) 
                              >> 1U));
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r__v0 = 1U;
    }
    if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__accept_w) 
         & ((0x0bU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__state_r)) 
            & (0x0400U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_wptr_r))))) {
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_ram__v0 
            = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__out_ent_r));
        vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_ram__v0 
            = (0x000003ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_wptr_r));
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_ram__v0 = 1U;
    }
    if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__stg_we_w) {
        vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__stg_r__v0 
            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__cmap_l_w)) 
                << 0x00000018U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__cmap_r_w)));
        vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__stg_r__v0 
            = (((((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w) 
                  << 1U) | vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__wbank_r
                 [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w]) 
                << 5U) | (((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r
                                   [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w]) 
                           << 2U) | (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w)));
        vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__stg_r__v0 = 1U;
    }
    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__stg_q_r 
        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__stg_r
        [(((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r) 
           << 6U) | (((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ebank_r) 
                      << 5U) | ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__esmp_r) 
                                  << 2U) | (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eo_r)) 
                                & (- (IData)((2U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)))))))];
    if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_valid_w) 
         & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_cancel_w)))) {
        if ((0x5fU >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__slot_ram_r__v0 
                = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_owner_w)) 
                    << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_deadline_w)));
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__slot_ram_r__v0 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w;
            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__slot_ram_r__v0 = 1U;
        }
    }
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__deliver_w) {
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r__v0[0U] = 0U;
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r__v0[1U] = 0U;
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r__v0[2U] 
            = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__sel_r) 
                << 0x00000018U) | ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__valid_r) 
                                     & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                                        >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__sel_r))) 
                                    << 0x00000010U) 
                                   | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r
                                   [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__sel_r]));
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r__v0[3U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r;
        vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r__v0 
            = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__wr_count_r));
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r__v0 = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_sel_w) 
          & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_we_r)) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w) 
            >> 5U))) {
        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))) {
            if ((8U > (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r__v0 
                    = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_wdata_r);
                vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r__v0 
                    = (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w));
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r__v0 = 1U;
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r__v0 
                    = (vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_wdata_r 
                       >> 0x10U);
                vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r__v0 
                    = (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w));
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r__v0 = 1U;
            }
        }
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w) 
                      >> 4U)))) {
            if ((8U > (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_pref_r__v0 
                    = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_wdata_r);
                vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_pref_r__v0 
                    = (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w));
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_pref_r__v0 = 1U;
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_len_r__v0 
                    = (vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_wdata_r 
                       >> 0x10U);
                vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_len_r__v0 
                    = (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w));
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_len_r__v0 = 1U;
            }
        }
    }
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
        if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_raddr_w))) {
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
    if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_q_r 
            = ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r))
                ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_r
               [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r]
                : 0ULL);
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__enable_q_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__pp_shadow__enable_i));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__out_valid_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__rd_fire_w));
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__en_q 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__crf_rx__en_i));
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
}
