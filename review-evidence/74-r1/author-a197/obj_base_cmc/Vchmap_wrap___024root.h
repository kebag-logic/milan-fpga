// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vchmap_wrap.h for the primary calling header

#ifndef VERILATED_VCHMAP_WRAP___024ROOT_H_
#define VERILATED_VCHMAP_WRAP___024ROOT_H_  // guard

#include "verilated.h"
class Vchmap_wrap_KL_chan_map_capture;


class Vchmap_wrap__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vchmap_wrap___024root final {
  public:
    // CELLS
    Vchmap_wrap_KL_chan_map_capture* __PVT__chmap_wrap__DOT__u_chmap_a;
    Vchmap_wrap_KL_chan_map_capture* __PVT__chmap_wrap__DOT__u_chmap_b;

    // DESIGN SPECIFIC STATE
    // Anonymous structures to workaround compiler member-count bugs
    struct {
        VL_IN8(clk,0,0);
        VL_IN8(clk_audio,0,0);
        VL_IN8(rst_n,0,0);
        VL_IN8(tg_en_i,0,0);
        VL_IN8(tg_tick_i,0,0);
        VL_IN8(i2s_pair_valid_i,0,0);
        VL_IN8(tdm_pair_valid_i,0,0);
        VL_IN8(tdm_pair_slot_i,3,0);
        VL_IN8(lb_tvalid_i,0,0);
        VL_IN8(lb_tlast_i,0,0);
        VL_IN8(lb_tuser_i,3,0);
        VL_IN8(a_lb_flush_i,7,0);
        VL_IN8(b_lb_flush_i,7,0);
        VL_IN8(a_map_wr_en_i,0,0);
        VL_IN8(a_map_wr_addr_i,5,0);
        VL_IN8(a_map_rd_en_i,0,0);
        VL_IN8(a_map_rd_addr_i,5,0);
        VL_OUT8(a_map_rd_valid_o,0,0);
        VL_IN8(a_tick_i,0,0);
        VL_OUT8(a_pv_o,0,0);
        VL_IN8(a_en_i,1,0);
        VL_IN8(a_tctx_wr_en_i,0,0);
        VL_IN8(a_tctx_wr_addr_i,6,0);
        VL_OUT8(a_tctx_wr_rdy_o,0,0);
        VL_IN8(a_tctx_rd_en_i,0,0);
        VL_IN8(a_tctx_rd_addr_i,6,0);
        VL_OUT8(a_tctx_rd_valid_o,0,0);
        VL_OUT8(a_tkeep_o,7,0);
        VL_OUT8(a_tvalid_o,0,0);
        VL_OUT8(a_tlast_o,0,0);
        VL_IN8(a_tready_i,0,0);
        VL_IN8(b_map_wr_en_i,0,0);
        VL_IN8(b_map_wr_addr_i,5,0);
        VL_IN8(b_map_rd_en_i,0,0);
        VL_IN8(b_map_rd_addr_i,5,0);
        VL_OUT8(b_map_rd_valid_o,0,0);
        VL_IN8(b_tick_i,0,0);
        VL_IN8(b_en_i,7,0);
        VL_IN8(b_tctx_wr_en_i,0,0);
        VL_IN8(b_tctx_wr_addr_i,6,0);
        VL_OUT8(b_tctx_wr_rdy_o,0,0);
        VL_IN8(b_tctx_rd_en_i,0,0);
        VL_IN8(b_tctx_rd_addr_i,6,0);
        VL_OUT8(b_tctx_rd_valid_o,0,0);
        VL_OUT8(b_tkeep_o,7,0);
        VL_OUT8(b_tvalid_o,0,0);
        VL_OUT8(b_tlast_o,0,0);
        VL_IN8(b_tready_i,0,0);
        CData/*3:0*/ chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_1__chn_clamp;
        CData/*6:0*/ chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_0__taddr;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_b__DOT__tram_we_w;
        CData/*6:0*/ chmap_wrap__DOT__u_pkt_b__DOT__tram_waddr_w;
        CData/*6:0*/ chmap_wrap__DOT__u_pkt_b__DOT__tram_raddr_w;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_b__DOT__stg_we_w;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_b__DOT__pown_v_w;
        CData/*2:0*/ chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w;
        CData/*1:0*/ chmap_wrap__DOT__u_pkt_b__DOT__pown_o_w;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_b__DOT__own_last_w;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r;
        CData/*2:0*/ chmap_wrap__DOT__u_pkt_b__DOT__tsw_t_r;
        CData/*2:0*/ chmap_wrap__DOT__u_pkt_b__DOT__est_r;
        CData/*2:0*/ chmap_wrap__DOT__u_pkt_b__DOT__et_r;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_b__DOT__ebank_r;
        CData/*3:0*/ chmap_wrap__DOT__u_pkt_b__DOT__fph_r;
    };
    struct {
        CData/*4:0*/ chmap_wrap__DOT__u_pkt_b__DOT__beat_r;
        CData/*2:0*/ chmap_wrap__DOT__u_pkt_b__DOT__rr_r;
        CData/*4:0*/ chmap_wrap__DOT__u_pkt_b__DOT__eiss_r;
        CData/*4:0*/ chmap_wrap__DOT__u_pkt_b__DOT__ecap_r;
        CData/*2:0*/ chmap_wrap__DOT__u_pkt_b__DOT__esmp_r;
        CData/*1:0*/ chmap_wrap__DOT__u_pkt_b__DOT__eo_r;
        CData/*7:0*/ chmap_wrap__DOT__u_pkt_b__DOT__eseq_r;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_b__DOT__etu_r;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_b__DOT__emr_r;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_b__DOT__grant_v_w;
        CData/*2:0*/ chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_go_w;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_q_r;
        CData/*3:0*/ chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_1__chn_clamp;
        CData/*4:0*/ chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_0__taddr;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_a__DOT__tram_we_w;
        CData/*4:0*/ chmap_wrap__DOT__u_pkt_a__DOT__tram_waddr_w;
        CData/*4:0*/ chmap_wrap__DOT__u_pkt_a__DOT__tram_raddr_w;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_a__DOT__stg_we_w;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_a__DOT__pown_v_w;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w;
        CData/*1:0*/ chmap_wrap__DOT__u_pkt_a__DOT__pown_o_w;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_a__DOT__own_last_w;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_a__DOT__tsw_t_r;
        CData/*2:0*/ chmap_wrap__DOT__u_pkt_a__DOT__est_r;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_a__DOT__et_r;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_a__DOT__ebank_r;
        CData/*3:0*/ chmap_wrap__DOT__u_pkt_a__DOT__fph_r;
        CData/*4:0*/ chmap_wrap__DOT__u_pkt_a__DOT__beat_r;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_a__DOT__rr_r;
        CData/*4:0*/ chmap_wrap__DOT__u_pkt_a__DOT__eiss_r;
        CData/*4:0*/ chmap_wrap__DOT__u_pkt_a__DOT__ecap_r;
        CData/*2:0*/ chmap_wrap__DOT__u_pkt_a__DOT__esmp_r;
        CData/*1:0*/ chmap_wrap__DOT__u_pkt_a__DOT__eo_r;
        CData/*7:0*/ chmap_wrap__DOT__u_pkt_a__DOT__eseq_r;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_a__DOT__etu_r;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_a__DOT__emr_r;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_a__DOT__grant_v_w;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_a__DOT__grant_t_w;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_go_w;
        CData/*0:0*/ chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_q_r;
        CData/*5:0*/ chmap_wrap__DOT__u_tone_media__DOT__idx_r;
        CData/*5:0*/ chmap_wrap__DOT__u_tone_legacy__DOT__idx_r;
        CData/*6:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__0__Vfuncout;
        CData/*2:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__0__t;
        CData/*6:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__1__Vfuncout;
        CData/*2:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__1__t;
        CData/*6:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__2__Vfuncout;
        CData/*2:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__2__t;
        CData/*2:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__4__t;
        CData/*3:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__4__w;
        CData/*6:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__5__Vfuncout;
        CData/*2:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__5__t;
        CData/*6:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__6__Vfuncout;
        CData/*2:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__6__t;
        CData/*2:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__7__t;
        CData/*3:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__7__w;
        CData/*6:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__8__Vfuncout;
        CData/*2:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__8__t;
        CData/*3:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__8__w;
        CData/*6:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__9__Vfuncout;
        CData/*2:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__9__t;
        CData/*3:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__9__w;
    };
    struct {
        CData/*2:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__10__t;
        CData/*3:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__10__w;
        CData/*4:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__12__Vfuncout;
        CData/*0:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__12__t;
        CData/*4:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__13__Vfuncout;
        CData/*0:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__13__t;
        CData/*4:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__14__Vfuncout;
        CData/*0:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__14__t;
        CData/*0:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__16__t;
        CData/*3:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__16__w;
        CData/*4:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__17__Vfuncout;
        CData/*0:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__17__t;
        CData/*4:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__18__Vfuncout;
        CData/*0:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__18__t;
        CData/*0:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__19__t;
        CData/*3:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__19__w;
        CData/*4:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__20__Vfuncout;
        CData/*0:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__20__t;
        CData/*3:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__20__w;
        CData/*4:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__21__Vfuncout;
        CData/*0:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__21__t;
        CData/*3:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__21__w;
        CData/*0:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__22__t;
        CData/*3:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__22__w;
        CData/*2:0*/ __VdfgRegularize_h6e95ff9d_0_11;
        CData/*2:0*/ __VdfgRegularize_h6e95ff9d_0_20;
        CData/*0:0*/ __VstlFirstIteration;
        CData/*0:0*/ __VstlPhaseResult;
        CData/*0:0*/ __Vtrigprevexpr___TOP__clk__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__rst_n__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__clk_audio__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__tg_en_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__tg_tick_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__i2s_pair_valid_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__tdm_pair_valid_i__0;
        CData/*3:0*/ __Vtrigprevexpr___TOP__tdm_pair_slot_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__lb_tvalid_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__lb_tlast_i__0;
        CData/*3:0*/ __Vtrigprevexpr___TOP__lb_tuser_i__0;
        CData/*7:0*/ __Vtrigprevexpr___TOP__a_lb_flush_i__0;
        CData/*7:0*/ __Vtrigprevexpr___TOP__b_lb_flush_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__a_map_wr_en_i__0;
        CData/*5:0*/ __Vtrigprevexpr___TOP__a_map_wr_addr_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__a_map_rd_en_i__0;
        CData/*5:0*/ __Vtrigprevexpr___TOP__a_map_rd_addr_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__a_tick_i__0;
        CData/*1:0*/ __Vtrigprevexpr___TOP__a_en_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__a_tctx_wr_en_i__0;
        CData/*6:0*/ __Vtrigprevexpr___TOP__a_tctx_wr_addr_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__a_tctx_rd_en_i__0;
        CData/*6:0*/ __Vtrigprevexpr___TOP__a_tctx_rd_addr_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__a_tready_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__b_map_wr_en_i__0;
        CData/*5:0*/ __Vtrigprevexpr___TOP__b_map_wr_addr_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__b_map_rd_en_i__0;
        CData/*5:0*/ __Vtrigprevexpr___TOP__b_map_rd_addr_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__b_tick_i__0;
        CData/*7:0*/ __Vtrigprevexpr___TOP__b_en_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__b_tctx_wr_en_i__0;
        CData/*6:0*/ __Vtrigprevexpr___TOP__b_tctx_wr_addr_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__b_tctx_rd_en_i__0;
        CData/*6:0*/ __Vtrigprevexpr___TOP__b_tctx_rd_addr_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__b_tready_i__0;
        CData/*0:0*/ __VicoDidInit;
    };
    struct {
        CData/*0:0*/ __VicoPhaseResult;
        CData/*0:0*/ __Vtrigprevexpr___TOP__clk__1;
        CData/*0:0*/ __Vtrigprevexpr___TOP__clk_audio__1;
        CData/*0:0*/ __VactPhaseResult;
        CData/*0:0*/ __VnbaPhaseResult;
        VL_IN16(vlan_vid_i,11,0);
        VL_OUT16(a_dup_cnt_o,15,0);
        VL_OUT16(a_skip_cnt_o,15,0);
        VL_OUT16(a_tdm_dup_cnt_o,15,0);
        VL_OUT16(a_tdm_skip_cnt_o,15,0);
        VL_OUT16(b_dup_cnt_o,15,0);
        VL_OUT16(b_skip_cnt_o,15,0);
        VL_IN16(a_map_wr_data_i,12,0);
        VL_OUT16(a_map_rd_data_o,14,0);
        VL_IN16(b_map_wr_data_i,12,0);
        VL_OUT16(b_map_rd_data_o,14,0);
        SData/*15:0*/ chmap_wrap__DOT__u_pkt_b__DOT__euid_r;
        SData/*11:0*/ chmap_wrap__DOT__u_pkt_b__DOT__evid_r;
        SData/*11:0*/ chmap_wrap__DOT__u_pkt_b__DOT__eff_vid_w;
        SData/*15:0*/ chmap_wrap__DOT__u_pkt_a__DOT__euid_r;
        SData/*11:0*/ chmap_wrap__DOT__u_pkt_a__DOT__evid_r;
        SData/*11:0*/ chmap_wrap__DOT__u_pkt_a__DOT__eff_vid_w;
        SData/*8:0*/ chmap_wrap__DOT__u_tone_legacy__DOT__cnt_r;
        SData/*11:0*/ __Vtrigprevexpr___TOP__vlan_vid_i__0;
        SData/*12:0*/ __Vtrigprevexpr___TOP__a_map_wr_data_i__0;
        SData/*12:0*/ __Vtrigprevexpr___TOP__b_map_wr_data_i__0;
        VL_OUT(tone_legacy_o,23,0);
        VL_OUT(tone_media_o,23,0);
        VL_IN(transit_ns_i,31,0);
        VL_IN(i2s_l_i,23,0);
        VL_IN(i2s_r_i,23,0);
        VL_IN(tdm_l_i,23,0);
        VL_IN(tdm_r_i,23,0);
        VL_IN(tone_smp_i,23,0);
        VL_IN(lb_wire_chans_i,31,0);
        VL_IN(a_tctx_wr_data_i,31,0);
        VL_OUT(a_tctx_rd_data_o,31,0);
        VL_IN(b_tctx_wr_data_i,31,0);
        VL_OUT(b_tctx_rd_data_o,31,0);
        IData/*31:0*/ chmap_wrap__DOT__u_pkt_b__DOT__tram_wdata_w;
        IData/*31:0*/ chmap_wrap__DOT__u_pkt_b__DOT__tram_q_r;
        IData/*31:0*/ chmap_wrap__DOT__u_pkt_b__DOT__tsw_val_r;
        IData/*31:0*/ chmap_wrap__DOT__u_pkt_b__DOT__ets_r;
        IData/*31:0*/ chmap_wrap__DOT__u_pkt_a__DOT__tram_wdata_w;
        IData/*31:0*/ chmap_wrap__DOT__u_pkt_a__DOT__tram_q_r;
        IData/*31:0*/ chmap_wrap__DOT__u_pkt_a__DOT__tsw_val_r;
        IData/*31:0*/ chmap_wrap__DOT__u_pkt_a__DOT__ets_r;
        IData/*31:0*/ __Vtrigprevexpr___TOP__transit_ns_i__0;
        IData/*23:0*/ __Vtrigprevexpr___TOP__i2s_l_i__0;
        IData/*23:0*/ __Vtrigprevexpr___TOP__i2s_r_i__0;
        IData/*23:0*/ __Vtrigprevexpr___TOP__tdm_l_i__0;
        IData/*23:0*/ __Vtrigprevexpr___TOP__tdm_r_i__0;
        IData/*23:0*/ __Vtrigprevexpr___TOP__tone_smp_i__0;
        IData/*31:0*/ __Vtrigprevexpr___TOP__lb_wire_chans_i__0;
        IData/*31:0*/ __Vtrigprevexpr___TOP__a_tctx_wr_data_i__0;
        IData/*31:0*/ __Vtrigprevexpr___TOP__b_tctx_wr_data_i__0;
        IData/*31:0*/ __VactIterCount;
        VL_IN64(dest_mac_i,47,0);
        VL_IN64(station_mac_i,47,0);
        VL_IN64(ptp_ns_i,63,0);
        VL_IN64(lb_tdata_i,63,0);
        VL_OUT64(a_tdata_o,63,0);
        VL_OUT64(b_tdata_o,63,0);
        QData/*47:0*/ chmap_wrap__DOT__u_pkt_b__DOT__stg_q_r;
    };
    struct {
        QData/*47:0*/ chmap_wrap__DOT__u_pkt_b__DOT__edmac_r;
        QData/*47:0*/ chmap_wrap__DOT__u_pkt_b__DOT__eff_dmac_w;
        QData/*63:0*/ chmap_wrap__DOT__u_pkt_b__DOT__stream_id_w;
        QData/*47:0*/ chmap_wrap__DOT__u_pkt_a__DOT__stg_q_r;
        QData/*47:0*/ chmap_wrap__DOT__u_pkt_a__DOT__edmac_r;
        QData/*47:0*/ chmap_wrap__DOT__u_pkt_a__DOT__eff_dmac_w;
        QData/*63:0*/ chmap_wrap__DOT__u_pkt_a__DOT__stream_id_w;
        QData/*47:0*/ __Vtrigprevexpr___TOP__dest_mac_i__0;
        QData/*47:0*/ __Vtrigprevexpr___TOP__station_mac_i__0;
        QData/*63:0*/ __Vtrigprevexpr___TOP__ptp_ns_i__0;
        QData/*63:0*/ __Vtrigprevexpr___TOP__lb_tdata_i__0;
        VlUnpacked<IData/*31:0*/, 128> chmap_wrap__DOT__u_pkt_b__DOT__tctx_r;
        VlUnpacked<QData/*47:0*/, 512> chmap_wrap__DOT__u_pkt_b__DOT__stg_r;
        VlUnpacked<CData/*2:0*/, 8> chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r;
        VlUnpacked<CData/*0:0*/, 8> chmap_wrap__DOT__u_pkt_b__DOT__wbank_r;
        VlUnpacked<CData/*0:0*/, 8> chmap_wrap__DOT__u_pkt_b__DOT__pend_r;
        VlUnpacked<CData/*3:0*/, 8> chmap_wrap__DOT__u_pkt_b__DOT__chans_r;
        VlUnpacked<CData/*5:0*/, 9> chmap_wrap__DOT__u_pkt_b__DOT__pbase_w;
        VlUnpacked<IData/*23:0*/, 24> chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r;
        VlUnpacked<IData/*23:0*/, 24> chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r;
        VlUnpacked<CData/*7:0*/, 240> chmap_wrap__DOT__u_pkt_b__DOT__fb;
        VlUnpacked<IData/*31:0*/, 32> chmap_wrap__DOT__u_pkt_a__DOT__tctx_r;
        VlUnpacked<QData/*47:0*/, 128> chmap_wrap__DOT__u_pkt_a__DOT__stg_r;
        VlUnpacked<CData/*2:0*/, 2> chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r;
        VlUnpacked<CData/*0:0*/, 2> chmap_wrap__DOT__u_pkt_a__DOT__wbank_r;
        VlUnpacked<CData/*0:0*/, 2> chmap_wrap__DOT__u_pkt_a__DOT__pend_r;
        VlUnpacked<CData/*3:0*/, 2> chmap_wrap__DOT__u_pkt_a__DOT__chans_r;
        VlUnpacked<CData/*5:0*/, 3> chmap_wrap__DOT__u_pkt_a__DOT__pbase_w;
        VlUnpacked<IData/*23:0*/, 24> chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r;
        VlUnpacked<IData/*23:0*/, 24> chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r;
        VlUnpacked<CData/*7:0*/, 240> chmap_wrap__DOT__u_pkt_a__DOT__fb;
        VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;
        VlUnpacked<QData/*63:0*/, 2> __VicoTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;
    };

    // INTERNAL VARIABLES
    Vchmap_wrap__Syms* vlSymsp;
    const char* vlNamep;

    // PARAMETERS
    static constexpr VlUnpacked<IData/*23:0*/, 48> chmap_wrap__DOT__u_tone_media__DOT__TONE_TAB_C = {{
        0U, 0x0010b515U, 0x002120fbU, 0x0030fbc5U,
        0x003fffffU, 0x004debe4U, 0x005a8279U, 0x00658c99U,
        0x006ed9ebU, 0x007641aeU, 0x007ba374U, 0x007ee7a9U,
        0x007fffffU, 0x007ee7a9U, 0x007ba374U, 0x007641aeU,
        0x006ed9ebU, 0x00658c99U, 0x005a8279U, 0x004debe4U,
        0x003fffffU, 0x0030fbc5U, 0x002120fbU, 0x0010b515U,
        0U, 0x00ef4aebU, 0x00dedf05U, 0x00cf043bU,
        0x00c00001U, 0x00b2141cU, 0x00a57d87U, 0x009a7367U,
        0x00912615U, 0x0089be52U, 0x00845c8cU, 0x00811857U,
        0x00800001U, 0x00811857U, 0x00845c8cU, 0x0089be52U,
        0x00912615U, 0x009a7367U, 0x00a57d87U, 0x00b2141cU,
        0x00c00000U, 0x00cf043bU, 0x00dedf05U, 0x00ef4aebU
    }};
    static constexpr VlUnpacked<IData/*23:0*/, 48> chmap_wrap__DOT__u_tone_legacy__DOT__TONE_TAB_C = {{
        0U, 0x0010b515U, 0x002120fbU, 0x0030fbc5U,
        0x003fffffU, 0x004debe4U, 0x005a8279U, 0x00658c99U,
        0x006ed9ebU, 0x007641aeU, 0x007ba374U, 0x007ee7a9U,
        0x007fffffU, 0x007ee7a9U, 0x007ba374U, 0x007641aeU,
        0x006ed9ebU, 0x00658c99U, 0x005a8279U, 0x004debe4U,
        0x003fffffU, 0x0030fbc5U, 0x002120fbU, 0x0010b515U,
        0U, 0x00ef4aebU, 0x00dedf05U, 0x00cf043bU,
        0x00c00001U, 0x00b2141cU, 0x00a57d87U, 0x009a7367U,
        0x00912615U, 0x0089be52U, 0x00845c8cU, 0x00811857U,
        0x00800001U, 0x00811857U, 0x00845c8cU, 0x0089be52U,
        0x00912615U, 0x009a7367U, 0x00a57d87U, 0x00b2141cU,
        0x00c00000U, 0x00cf043bU, 0x00dedf05U, 0x00ef4aebU
    }};

    // CONSTRUCTORS
    Vchmap_wrap___024root(Vchmap_wrap__Syms* symsp, const char* namep);
    ~Vchmap_wrap___024root();
    VL_UNCOPYABLE(Vchmap_wrap___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
