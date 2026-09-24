// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See VKL_mmcm_drp_servo.h for the primary calling header

#ifndef VERILATED_VKL_MMCM_DRP_SERVO___024ROOT_H_
#define VERILATED_VKL_MMCM_DRP_SERVO___024ROOT_H_  // guard

#include "verilated.h"


class VKL_mmcm_drp_servo__Syms;

class alignas(VL_CACHE_LINE_BYTES) VKL_mmcm_drp_servo___024root final {
  public:

    // DESIGN SPECIFIC STATE
    // Anonymous structures to workaround compiler member-count bugs
    struct {
        VL_IN8(clk_i,0,0);
        VL_IN8(clk_audio_i,0,0);
        VL_IN8(ps_clk_i,0,0);
        VL_IN8(rst_n,0,0);
        VL_IN8(crf_locked_i,0,0);
        VL_IN8(auto_repair_i,0,0);
        VL_IN8(ps_invert_i,0,0);
        VL_OUT8(drp_addr_o,6,0);
        VL_OUT8(drp_en_o,0,0);
        VL_OUT8(drp_we_o,0,0);
        VL_IN8(drp_rdy_i,0,0);
        VL_OUT8(mmcm_rst_o,0,0);
        VL_IN8(mmcm_locked_i,0,0);
        VL_OUT8(ps_en_o,0,0);
        VL_OUT8(ps_incdec_o,0,0);
        VL_IN8(ps_done_i,0,0);
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__clk_i;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__rst_n;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__clk_audio_i;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__ps_clk_i;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__crf_locked_i;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__auto_repair_i;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__ps_invert_i;
        CData/*6:0*/ KL_mmcm_drp_servo__DOT__drp_addr_o;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__drp_en_o;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__drp_we_o;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__drp_rdy_i;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__mmcm_rst_o;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__mmcm_locked_i;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__ps_en_o;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__ps_incdec_o;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__ps_done_i;
        CData/*1:0*/ KL_mmcm_drp_servo__DOT__arst_sync_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__arst_n_w;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__tick_a_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__tick_p_w;
        CData/*1:0*/ KL_mmcm_drp_servo__DOT__locked_sync_r;
        CData/*1:0*/ KL_mmcm_drp_servo__DOT__psbusy_sync_r;
        CData/*1:0*/ KL_mmcm_drp_servo__DOT__psfault_sync_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__ps_busy_ps_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__ps_fault_ps_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__mmcm_locked_s_w;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__ps_busy_s_w;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__ps_fault_s_w;
        CData/*2:0*/ KL_mmcm_drp_servo__DOT__state_r;
        CData/*3:0*/ KL_mmcm_drp_servo__DOT__dstate_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__servo_sel_w;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__win_valid_r;
        CData/*1:0*/ KL_mmcm_drp_servo__DOT__win_skip_r;
        CData/*1:0*/ KL_mmcm_drp_servo__DOT__disc_run_r;
        CData/*5:0*/ KL_mmcm_drp_servo__DOT__disc_cnt_r;
        CData/*2:0*/ KL_mmcm_drp_servo__DOT__lock_cnt_r;
        CData/*2:0*/ KL_mmcm_drp_servo__DOT__pp_seq_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__pp_run_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__pp_thr_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__hs_send_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__hs_rcv_w;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__ps_hold_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__drp_pass_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__rd_second_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__repairing_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__verified_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__mismatch_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__drp_fault_r;
    };
    struct {
        CData/*3:0*/ KL_mmcm_drp_servo__DOT__rst_settle_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__ptp_jump_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__guard_hit_w;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__step_hit_w;
        CData/*1:0*/ KL_mmcm_drp_servo__DOT__psrst_sync_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__psrst_n_w;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__ps_req_w;
        CData/*1:0*/ KL_mmcm_drp_servo__DOT__pstate_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__ps_dir_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__pend_v_r;
        CData/*7:0*/ KL_mmcm_drp_servo__DOT__ps_wd_r;
        CData/*6:0*/ KL_mmcm_drp_servo__DOT__servo_engine__DOT__disc_tally__DOT__n_v;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_clk;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_rst_n;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_send;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_rcv;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_clk;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_rst_n;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_req;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_send_d;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_tog;
        CData/*2:0*/ KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__ack_sync;
        CData/*2:0*/ KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_sync;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_req_r;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__ack_tog;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_edge;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_clk;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_rst_n;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_pulse;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_clk;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_rst_n;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_pulse;
        CData/*0:0*/ KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_level;
        CData/*2:0*/ KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__sync;
        CData/*0:0*/ __Vdly__KL_mmcm_drp_servo__DOT__pend_v_r;
        CData/*0:0*/ __Vdly__KL_mmcm_drp_servo__DOT__ps_dir_r;
        CData/*1:0*/ __Vdly__KL_mmcm_drp_servo__DOT__pstate_r;
        CData/*7:0*/ __Vdly__KL_mmcm_drp_servo__DOT__ps_wd_r;
        CData/*0:0*/ __Vdly__KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__ack_tog;
        CData/*0:0*/ __Vdly__KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_level;
        CData/*0:0*/ __VstlFirstIteration;
        CData/*0:0*/ __VstlPhaseResult;
        CData/*0:0*/ __Vtrigprevexpr___TOP__clk_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__rst_n__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__clk_audio_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__ps_clk_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__crf_locked_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__auto_repair_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__ps_invert_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__drp_rdy_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__mmcm_locked_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__ps_done_i__0;
        CData/*0:0*/ __VicoDidInit;
        CData/*0:0*/ __VicoFirstIteration;
        CData/*0:0*/ __VicoPhaseResult;
        CData/*0:0*/ __Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__clk_audio_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__clk_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__ps_clk_i__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_clk__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_clk__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_clk__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_clk__0;
        CData/*0:0*/ __VactPhaseResult;
        CData/*0:0*/ __VnbaPhaseResult;
    };
    struct {
        VL_IN16(clk_src_i,15,0);
        VL_IN16(crf_src_idx_i,15,0);
        VL_OUT16(drp_di_o,15,0);
        VL_IN16(drp_do_i,15,0);
        SData/*15:0*/ KL_mmcm_drp_servo__DOT__clk_src_i;
        SData/*15:0*/ KL_mmcm_drp_servo__DOT__crf_src_idx_i;
        SData/*15:0*/ KL_mmcm_drp_servo__DOT__drp_di_o;
        SData/*15:0*/ KL_mmcm_drp_servo__DOT__drp_do_i;
        SData/*14:0*/ KL_mmcm_drp_servo__DOT__tick_div_r;
        SData/*9:0*/ KL_mmcm_drp_servo__DOT__tick_cnt_r;
        SData/*14:0*/ KL_mmcm_drp_servo__DOT__hs_data_r;
        SData/*15:0*/ KL_mmcm_drp_servo__DOT__rd_val_r;
        SData/*15:0*/ KL_mmcm_drp_servo__DOT__exp_val_w;
        SData/*15:0*/ KL_mmcm_drp_servo__DOT__exp_mask_w;
        SData/*14:0*/ KL_mmcm_drp_servo__DOT__ps_cmd_w;
        SData/*13:0*/ KL_mmcm_drp_servo__DOT__ps_cnt_r;
        SData/*14:0*/ KL_mmcm_drp_servo__DOT__pend_r;
        SData/*15:0*/ KL_mmcm_drp_servo__DOT__trim_w;
        SData/*14:0*/ KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_in;
        SData/*14:0*/ KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_out;
        SData/*14:0*/ KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__data_hold;
        SData/*14:0*/ KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_out_r;
        SData/*13:0*/ __Vdly__KL_mmcm_drp_servo__DOT__ps_cnt_r;
        SData/*15:0*/ __Vtrigprevexpr___TOP__clk_src_i__0;
        SData/*15:0*/ __Vtrigprevexpr___TOP__crf_src_idx_i__0;
        SData/*15:0*/ __Vtrigprevexpr___TOP__drp_do_i__0;
        VL_IN(crf_rate_i,31,0);
        VL_OUT(status_o,31,0);
        IData/*23:0*/ KL_mmcm_drp_servo__DOT____VlemCall_1__clamp_u;
        IData/*23:0*/ KL_mmcm_drp_servo__DOT____VlemCall_0__clamp_u;
        IData/*31:0*/ KL_mmcm_drp_servo__DOT__crf_rate_i;
        IData/*31:0*/ KL_mmcm_drp_servo__DOT__status_o;
        IData/*31:0*/ KL_mmcm_drp_servo__DOT__ew_r;
        IData/*23:0*/ KL_mmcm_drp_servo__DOT__integ_r;
        IData/*23:0*/ KL_mmcm_drp_servo__DOT__u_cmd_r;
        IData/*31:0*/ KL_mmcm_drp_servo__DOT__pp_locerr_r;
        IData/*31:0*/ KL_mmcm_drp_servo__DOT__pp_rate_r;
        IData/*31:0*/ KL_mmcm_drp_servo__DOT__pp_isum_r;
        IData/*23:0*/ KL_mmcm_drp_servo__DOT__pp_ig_r;
        IData/*31:0*/ KL_mmcm_drp_servo__DOT__pp_un_r;
        IData/*23:0*/ KL_mmcm_drp_servo__DOT__pp_ut_r;
        IData/*31:0*/ KL_mmcm_drp_servo__DOT__pp_du_r;
        IData/*31:0*/ KL_mmcm_drp_servo__DOT__u_gain_r;
        IData/*31:0*/ KL_mmcm_drp_servo__DOT__acc_r;
        IData/*17:0*/ KL_mmcm_drp_servo__DOT__relock_r;
        IData/*31:0*/ KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__a_v;
        IData/*31:0*/ KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__b_v;
        IData/*31:0*/ __Vtrigprevexpr___TOP__crf_rate_i__0;
        IData/*31:0*/ __VactIterCount;
        VL_IN64(ptp_now_i,63,0);
        QData/*63:0*/ KL_mmcm_drp_servo__DOT__ptp_now_i;
        QData/*63:0*/ KL_mmcm_drp_servo__DOT__win_start_r;
        QData/*63:0*/ KL_mmcm_drp_servo__DOT__pp_d_r;
        QData/*63:0*/ KL_mmcm_drp_servo__DOT__pp_spann_r;
        QData/*63:0*/ KL_mmcm_drp_servo__DOT__ptp_q_r;
        QData/*63:0*/ __Vtrigprevexpr___TOP__ptp_now_i__0;
        VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;
        VlUnpacked<QData/*63:0*/, 2> __VicoTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;
    };

    // INTERNAL VARIABLES
    VKL_mmcm_drp_servo__Syms* vlSymsp;
    const char* vlNamep;

    // PARAMETERS
    static constexpr CData/*6:0*/ KL_mmcm_drp_servo__DOT__DADDR_C0R1_C = 8U;
    static constexpr CData/*6:0*/ KL_mmcm_drp_servo__DOT__DADDR_C0R2_C = 9U;
    static constexpr CData/*6:0*/ KL_mmcm_drp_servo__DOT__DADDR_POWER_C = 0x28U;
    static constexpr SData/*15:0*/ KL_mmcm_drp_servo__DOT__CFG_C0R1_P = 0x0595U;
    static constexpr SData/*15:0*/ KL_mmcm_drp_servo__DOT__CFG_C0R1_MASK_P = 0xefffU;
    static constexpr SData/*15:0*/ KL_mmcm_drp_servo__DOT__CFG_C0R2_P = 0x0080U;
    static constexpr SData/*15:0*/ KL_mmcm_drp_servo__DOT__CFG_C0R2_MASK_P = 0x7fffU;
    static constexpr SData/*15:0*/ KL_mmcm_drp_servo__DOT__POWER_ALL_C = 0xffffU;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__CLK_FREQ_HZ_P = 0x02faf080U;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__TICK_CYC_P = 0x00006000U;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__WIN_LOG2_P = 9U;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__NORM_SHIFT_P = 0U;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__KI_SHIFT_P = 1U;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__KP_SHIFT_P = 2U;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__U_MAX_P = 0x00019000U;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__SLEW_MAX_P = 0x0000c800U;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__LOCK_THR_P = 0x00000400U;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__LOCK_WIN_P = 4U;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__GAIN_NUM_P = 0x0000003bU;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__PS_TOUT_CYC_P = 0x000000ffU;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__RELOCK_TOUT_P = 0x00020000U;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__WIN_TICKS_C = 0x00000200U;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__ECLAMP_C = 0x00100000U;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__GUARD_THR_C = 0x00004000U;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__DISC_MAX_C = 4U;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__STEP_DET_NS_C = 0x00001000U;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__WIDTH = 0x0000000fU;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__DEST_SYNC_FF = 2U;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__SRC_SYNC_FF = 2U;
    static constexpr IData/*31:0*/ KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__DEST_SYNC_FF = 2U;
    static constexpr QData/*63:0*/ KL_mmcm_drp_servo__DOT__NOM_WIN_NS_P = 0x000000001e848000ULL;

    // CONSTRUCTORS
    VKL_mmcm_drp_servo___024root(VKL_mmcm_drp_servo__Syms* symsp, const char* namep);
    ~VKL_mmcm_drp_servo___024root();
    VL_UNCOPYABLE(VKL_mmcm_drp_servo___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
