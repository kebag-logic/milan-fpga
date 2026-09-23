// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vchmap_wrap.h for the primary calling header

#ifndef VERILATED_VCHMAP_WRAP_KL_CHAN_MAP_CAPTURE_H_
#define VERILATED_VCHMAP_WRAP_KL_CHAN_MAP_CAPTURE_H_  // guard

#include "verilated.h"


class Vchmap_wrap__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vchmap_wrap_KL_chan_map_capture final {
  public:

    // DESIGN SPECIFIC STATE
    // Anonymous structures to workaround compiler member-count bugs
    struct {
        CData/*0:0*/ clk_i;
        CData/*0:0*/ rst_n;
        CData/*0:0*/ map_wr_en_i;
        CData/*5:0*/ map_wr_addr_i;
        CData/*0:0*/ map_rd_en_i;
        CData/*5:0*/ map_rd_addr_i;
        CData/*0:0*/ map_rd_valid_o;
        CData/*0:0*/ i2s_pair_valid_i;
        CData/*0:0*/ tdm_pair_valid_i;
        CData/*3:0*/ tdm_pair_slot_i;
        CData/*0:0*/ lb_tvalid_i;
        CData/*0:0*/ lb_tlast_i;
        CData/*3:0*/ lb_tuser_i;
        CData/*7:0*/ lb_flush_i;
        CData/*0:0*/ tick_i;
        CData/*0:0*/ pair_valid_o;
        CData/*4:0*/ pair_slot_o;
        CData/*0:0*/ __PVT__loop_mapped_w;
        CData/*0:0*/ __PVT__loop_fed_r;
        CData/*0:0*/ __PVT__tdm_frame_ev_w;
        CData/*0:0*/ tdm_fed_r;
        CData/*0:0*/ tdm_frame_pend_r;
        CData/*3:0*/ __PVT__lb_chpos_r;
        CData/*3:0*/ __PVT__lb_chans_w;
        CData/*3:0*/ __PVT__lb_ch1_w;
        CData/*0:0*/ __PVT__lb_ok_w;
        CData/*0:0*/ __PVT__lb_w0_w;
        CData/*4:0*/ __PVT__lb_a0_w;
        CData/*0:0*/ __PVT__stash_vld_r;
        CData/*3:0*/ __PVT__stash_strm_r;
        CData/*0:0*/ __PVT__cm0_v_w;
        CData/*0:0*/ __PVT__lb_pair01_w;
        CData/*4:0*/ __PVT__cm1_addr_w;
        CData/*0:0*/ __PVT__stash_open_w;
        CData/*0:0*/ __PVT__stash_flush_w;
        CData/*0:0*/ __PVT__beat_flush_w;
        CData/*3:0*/ __PVT__skid_v_r;
        CData/*1:0*/ __PVT__skid_wp_r;
        CData/*1:0*/ __PVT__skid_rp_r;
        CData/*2:0*/ __PVT__skid_cnt_r;
        CData/*0:0*/ __PVT__push_ram_w;
        CData/*2:0*/ __PVT__skid_free_w;
        CData/*0:0*/ __PVT__skid_acc0_w;
        CData/*0:0*/ __PVT__enq0_v_w;
        CData/*0:0*/ __PVT__enq1_v_w;
        CData/*1:0*/ __PVT__skid_enq_n_w;
        CData/*3:0*/ __PVT__skid_kill_w;
        CData/*1:0*/ __PVT__st_r;
        CData/*5:0*/ __PVT__pop_idx_r;
        CData/*0:0*/ __PVT__pop_act_w;
        CData/*0:0*/ __PVT__push_same_w;
        CData/*3:0*/ __PVT__push_cnt1_w;
        CData/*0:0*/ __PVT__push_drop_w;
        CData/*0:0*/ __PVT__pop_ret_v_r;
        CData/*4:0*/ __PVT__pop_ret_pair_r;
        CData/*4:0*/ __PVT__slot_r;
        CData/*0:0*/ __PVT__tick_pend_r;
        CData/*4:0*/ __PVT__gap_r;
        CData/*2:0*/ __VdfgRegularize_h6e95ff9d_0_7;
        CData/*2:0*/ __VdfgRegularize_h6e95ff9d_0_8;
        CData/*2:0*/ __VdfgRegularize_h6e95ff9d_0_9;
        CData/*2:0*/ __VdfgRegularize_h6e95ff9d_0_10;
        CData/*3:0*/ __VdfgRegularize_h6e95ff9d_0_37;
        CData/*3:0*/ __VdfgRegularize_h6e95ff9d_0_38;
    };
    struct {
        CData/*3:0*/ __VdfgRegularize_h6e95ff9d_0_39;
        CData/*3:0*/ __VdfgRegularize_h6e95ff9d_0_40;
        CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_51;
        CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_52;
        CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_53;
        CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_54;
        CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_58;
        CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_59;
        CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_60;
        CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_61;
        SData/*12:0*/ map_wr_data_i;
        SData/*14:0*/ map_rd_data_o;
        SData/*15:0*/ lb_dup_cnt_o;
        SData/*15:0*/ lb_skip_cnt_o;
        SData/*15:0*/ tdm_dup_cnt_o;
        SData/*15:0*/ tdm_skip_cnt_o;
        VlWide<26>/*831:0*/ __PVT__map_flat_o;
        IData/*23:0*/ i2s_l_i;
        IData/*23:0*/ i2s_r_i;
        IData/*23:0*/ tdm_l_i;
        IData/*23:0*/ tdm_r_i;
        IData/*23:0*/ tone_smp_i;
        IData/*31:0*/ lb_wire_chans_i;
        IData/*23:0*/ pair_l_o;
        IData/*23:0*/ pair_r_o;
        IData/*23:0*/ __PVT__lb_smp0_w;
        IData/*23:0*/ __PVT__lb_smp1_w;
        IData/*23:0*/ __PVT__stash_val_r;
        IData/*31:0*/ __PVT__q_fed_r;
        IData/*31:0*/ __PVT__q_primed_r;
        IData/*31:0*/ __PVT__prime_set_w;
        IData/*31:0*/ __PVT__flush_clr_w;
        IData/*16:0*/ __PVT__skip_sum_w;
        IData/*16:0*/ __PVT__dup_sum_w;
        QData/*63:0*/ lb_tdata_i;
        QData/*47:0*/ __PVT__i2s_hold_r;
        QData/*47:0*/ __PVT__cm1_data_w;
        QData/*47:0*/ __PVT__q_rdata_r;
        QData/*47:0*/ __VdfgRegularize_h6e95ff9d_0_30;
        QData/*47:0*/ __VdfgRegularize_h6e95ff9d_0_32;
        QData/*47:0*/ __VdfgRegularize_h6e95ff9d_0_34;
        QData/*47:0*/ __VdfgRegularize_h6e95ff9d_0_36;
        VlUnpacked<SData/*12:0*/, 64> __PVT__map_r;
        VlUnpacked<QData/*47:0*/, 4> tdm_hold_r;
        VlUnpacked<QData/*47:0*/, 256> __PVT__lb_q_r;
        VlUnpacked<CData/*2:0*/, 32> __PVT__q_wr_r;
        VlUnpacked<CData/*2:0*/, 32> __PVT__q_rd_r;
        VlUnpacked<CData/*3:0*/, 32> __PVT__q_cnt_r;
        VlUnpacked<QData/*47:0*/, 32> __PVT__lb_hold_r;
        VlUnpacked<QData/*47:0*/, 4> __PVT__skid_data_r;
        VlUnpacked<CData/*4:0*/, 4> __PVT__skid_addr_r;
        VlUnpacked<CData/*3:0*/, 4> __PVT__skid_strm_r;
    };

    // INTERNAL VARIABLES
    Vchmap_wrap__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vchmap_wrap_KL_chan_map_capture();
    ~Vchmap_wrap_KL_chan_map_capture();
    void ctor(Vchmap_wrap__Syms* symsp, const char* namep);
    void dtor();
    VL_UNCOPYABLE(Vchmap_wrap_KL_chan_map_capture);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
