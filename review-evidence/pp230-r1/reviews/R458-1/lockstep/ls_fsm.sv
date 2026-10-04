// SPDX-License-Identifier: CERN-OHL-W-2.0
// R458-1 review probe (milan-fpga #230): module-level random lockstep of the
// base (_ref) and head (_new) KL_srp_talker_fsm, KL_srp_listener_fsm and
// KL_srp_admission at N contexts. Every input is drawn from the random words
// r0..r7 through small value pools, so gate opens re-declare, events match
// stored records and walks push. Every output of each pair is compared every
// cycle after the first reset; the counters say what the run reached.
`default_nettype none
module ls_fsm
  import srp_pkg::*;
#(
    parameter int unsigned N  = 3,
    parameter int unsigned AW = 7
) (
    input  wire         clk_i,
    input  wire         rst_n,
    input  wire  [63:0] r0, r1, r2, r3, r4, r5, r6,
    input  wire  [31:0] now_ms_i,
    output logic [63:0] mis_tk_o, mis_ls_o, mis_ad_o,
    output logic [63:0] cov_tk_push_o, cov_ls_push_o, cov_redecl_o, cov_resettle_o,
    output logic [63:0] cov_round_o, cov_walk_ram_o, cov_tk_reg_o, cov_ls_reg_o
);
  localparam int unsigned SW = (N > 1) ? $clog2(N) : 1;

  function automatic logic [63:0] sidp(input logic [2:0] i);
    return {48'h0011_2233_4455, 13'd0, i};
  endfunction
  function automatic logic [47:0] dap(input logic i);
    return i ? 48'h91E0_F000_FE01 : 48'h91E0_F000_FE00;
  endfunction
  function automatic logic [11:0] vidp(input logic i);
    return i ? 12'd3 : 12'd2;
  endfunction
  function automatic logic [7:0] attrp(input logic [2:0] i);
    case (i)
      3'd0, 3'd1: return SRP_MSRP_ATTR_TALKER_ADV_C;
      3'd2:       return SRP_MSRP_ATTR_TALKER_FAILED_C;
      3'd3, 3'd4: return SRP_MSRP_ATTR_LISTENER_C;
      3'd5:       return SRP_MSRP_ATTR_DOMAIN_C;
      default:    return 8'(i);
    endcase
  endfunction

  // ---------------------------------------------------------------- inputs
  logic p2p_r;
  logic [N-1:0] adm_r;
  always_ff @(posedge clk_i) begin
    if (r6[7:4] == 4'd0) p2p_r <= r6[0];
    if (r1[63:60] == 4'd0) adm_r <= r1[32 +: N];
  end

  wire          gate_valid = (r0[2:0] == 3'd0);
  wire          gate_open  = r0[3] | r0[4];
  wire [SW-1:0] gate_src   = SW'(32'(r0[15:8]) % N);
  wire [63:0]   g_sid      = sidp(r0[18:16]);
  wire [47:0]   g_da       = dap(r0[19]);
  wire [11:0]   g_vid      = vidp(r0[20]);
  wire [15:0]   g_mfs      = r0[39:24];
  wire [15:0]   g_mif      = {8'd0, r0[47:40]};
  wire [2:0]    g_prio     = r0[50:48];
  wire          g_rank     = r0[51];
  wire [31:0]   g_lat      = r1[31:0];

  wire          evt_valid  = (r2[1:0] == 2'd0);
  wire          evt_msrp   = r2[2] | r2[3];
  wire [7:0]    evt_attr   = attrp(r2[6:4]);
  wire [63:0]   evt_sid    = sidp(r2[9:7]);
  wire [47:0]   evt_da     = dap(r2[10]);
  wire [15:0]   evt_vid    = {r2[11] & r2[59], 3'd0, vidp(r2[12])};
  wire [2:0]    evt_ev     = r2[15:13];
  wire [1:0]    evt_fp     = r2[17:16];
  wire [31:0]   evt_lat    = {30'd0, r2[19:18]};
  wire [63:0]   evt_fsys   = {62'd0, r2[61:60]};
  wire [7:0]    evt_fcode  = {6'd0, r2[21:20]};
  wire          join_tick  = (r2[31:28] == 4'd0);
  wire          per_tick   = (r2[39:32] == 8'd0);
  wire [3:0]    la_rx      = (r2[43:40] == 4'd0) ? r2[47:44] : 4'd0;
  wire          la_own     = (r2[55:48] == 8'd0);
  wire          ev_ready   = r2[56] | r2[57];
  wire          user_ready = r2[58];
  wire [3:0]    vid_sent   = (r3[7:4] == 4'd0) ? r3[3:0] : 4'd0;
  wire [3:0][11:0] vid_val = {12'd5, 12'd4, 12'd3, 12'd2};
  wire          exp_valid  = (r3[11:8] == 4'd0);
  wire [AW-1:0] exp_slot   = AW'(16 + 32'(r3[19:12]) % 20);
  wire          ctl_valid  = (r4[2:0] == 3'd0);
  wire          ctl_settle = r4[3] | r4[4];
  wire [SW-1:0] ctl_sink   = SW'(32'(r4[15:8]) % N);
  wire [63:0]   c_sid      = sidp(r4[18:16]);
  wire [47:0]   c_da       = dap(r4[19]);
  wire [11:0]   c_vid      = vidp(r4[20]);

  // admission: request and TSpec per source, held, with the invalidate strobe
  logic [N-1:0]        req_r;
  logic [N-1:0][15:0]  amfs_r, amif_r;
  logic [N-1:0]        inv_w;
  logic [31:0]         rate_r;
  always_comb begin
    for (int unsigned s = 0; s < N; s++) inv_w[s] = (r5[4*s +: 4] == 4'd0) && r6[8 + s];
  end
  always_ff @(posedge clk_i) begin
    for (int unsigned s = 0; s < N; s++) begin
      if (inv_w[s]) begin
        req_r[s]  <= r5[40 + (s % 20)];
        amfs_r[s] <= {4'd0, r6[31:20]} + 16'(s);
        amif_r[s] <= {13'd0, r6[34:32]} + 16'd1;
      end
    end
    if (r6[47:40] == 8'd0) rate_r <= r6[48] ? 32'd100_000_000 : 32'd1_000_000_000;
  end

  // ------------------------------------------------------------- talker x2
  `define TK_PORTS(sfx) \
      .clk_i(clk_i), .rst_n(rst_n), .own_mac_i(48'h0201_0203_0405), .p2p_i(p2p_r), \
      .gate_valid_i(gate_valid), .gate_ready_o(tk_gr``sfx), .gate_open_i(gate_open), \
      .gate_src_i(gate_src), .gate_stream_id_i(g_sid), .gate_da_i(g_da), .gate_vid_i(g_vid), \
      .gate_max_frame_i(g_mfs), .gate_max_interval_i(g_mif), .gate_prio_i(g_prio), \
      .gate_rank_i(g_rank), .gate_acc_lat_i(g_lat), .sr_admitted_i(adm_r), \
      .evt_valid_i(evt_valid), .evt_msrp_i(evt_msrp), .evt_attr_type_i(evt_attr), \
      .evt_stream_id_i(evt_sid), .evt_da_i(evt_da), .evt_vid_i(evt_vid), \
      .evt_mrp_event_i(evt_ev), .evt_fourpacked_i(evt_fp), .join_tick_i(join_tick), \
      .periodic_tick_i(per_tick), .leaveall_rx_i(la_rx), .leaveall_own_i(la_own), \
      .txop_done_o(tk_done``sfx), .ev_valid_o(tk_evv``sfx), .ev_ready_i(ev_ready), \
      .ev_app_o(tk_eva``sfx), .ev_attr_type_o(tk_evt``sfx), .ev_event_o(tk_eve``sfx), \
      .ev_fourpack_o(tk_evf``sfx), .ev_value_o(tk_evx``sfx), .user_valid_o(tk_uv``sfx), \
      .user_join_o(tk_uj``sfx), .user_vid_o(tk_uvid``sfx), .user_ready_i(user_ready), \
      .vid_sent_i(vid_sent), .vid_val_i(vid_val), .now_ms_i(now_ms_i), \
      .arm_valid_o(tk_av``sfx), .arm_cancel_o(tk_ac``sfx), .arm_slot_o(tk_as``sfx), \
      .arm_owner_o(tk_ao``sfx), .arm_deadline_ms_o(tk_ad``sfx), .exp_valid_i(exp_valid), \
      .exp_slot_i(exp_slot), .lstn_reg_change_o(tk_lrc``sfx), .tk_decl_state_o(tk_ds``sfx), \
      .lstn_reg_state_o(tk_lrs``sfx), .active_o(tk_act``sfx), .msrp_fail_code_o(tk_fc``sfx), \
      .msrp_fail_bridge_o(tk_fb``sfx), .dbg_app_state_o(tk_das``sfx), .dbg_reg_state_o(tk_drs``sfx)

  logic tk_gr_r, tk_gr_n, tk_done_r, tk_done_n, tk_evv_r, tk_evv_n, tk_eva_r, tk_eva_n;
  logic [7:0] tk_evt_r, tk_evt_n; logic [2:0] tk_eve_r, tk_eve_n; logic [1:0] tk_evf_r, tk_evf_n;
  logic [271:0] tk_evx_r, tk_evx_n; logic tk_uv_r, tk_uv_n, tk_uj_r, tk_uj_n;
  logic [11:0] tk_uvid_r, tk_uvid_n; logic tk_av_r, tk_av_n, tk_ac_r, tk_ac_n;
  logic [AW-1:0] tk_as_r, tk_as_n; logic [7:0] tk_ao_r, tk_ao_n; logic [31:0] tk_ad_r, tk_ad_n;
  logic [N-1:0] tk_lrc_r, tk_lrc_n, tk_act_r, tk_act_n;
  logic [N-1:0][1:0] tk_ds_r, tk_ds_n, tk_lrs_r, tk_lrs_n, tk_drs_r, tk_drs_n;
  logic [N-1:0][7:0] tk_fc_r, tk_fc_n; logic [N-1:0][63:0] tk_fb_r, tk_fb_n;
  logic [N-1:0][3:0] tk_das_r, tk_das_n;

  KL_srp_talker_fsm_ref #(.N_SOURCES_P(N), .SLOT_BASE_P(16), .SLOT_AW_P(AW), .LEAVE_MS_P(50))
    u_tk_ref (`TK_PORTS(_r));
  KL_srp_talker_fsm_new #(.N_SOURCES_P(N), .SLOT_BASE_P(16), .SLOT_AW_P(AW), .LEAVE_MS_P(50))
    u_tk_new (`TK_PORTS(_n));

  wire tk_diff = (tk_gr_r != tk_gr_n) || (tk_done_r != tk_done_n) || (tk_evv_r != tk_evv_n)
              || (tk_eva_r != tk_eva_n) || (tk_evt_r != tk_evt_n) || (tk_eve_r != tk_eve_n)
              || (tk_evf_r != tk_evf_n) || (tk_evx_r != tk_evx_n) || (tk_uv_r != tk_uv_n)
              || (tk_uj_r != tk_uj_n) || (tk_uvid_r != tk_uvid_n) || (tk_av_r != tk_av_n)
              || (tk_ac_r != tk_ac_n) || (tk_as_r != tk_as_n) || (tk_ao_r != tk_ao_n)
              || (tk_ad_r != tk_ad_n) || (tk_lrc_r != tk_lrc_n) || (tk_ds_r != tk_ds_n)
              || (tk_lrs_r != tk_lrs_n) || (tk_act_r != tk_act_n) || (tk_fc_r != tk_fc_n)
              || (tk_fb_r != tk_fb_n) || (tk_das_r != tk_das_n) || (tk_drs_r != tk_drs_n);

  // ----------------------------------------------------------- listener x2
  `define LS_PORTS(sfx) \
      .clk_i(clk_i), .rst_n(rst_n), .p2p_i(p2p_r), .ctl_valid_i(ctl_valid), \
      .ctl_ready_o(ls_cr``sfx), .ctl_settle_i(ctl_settle), .ctl_sink_i(ctl_sink), \
      .ctl_stream_id_i(c_sid), .ctl_da_i(c_da), .ctl_vid_i(c_vid), \
      .evt_valid_i(evt_valid), .evt_msrp_i(evt_msrp), .evt_attr_type_i(evt_attr), \
      .evt_stream_id_i(evt_sid), .evt_da_i(evt_da), .evt_vid_i(evt_vid), \
      .evt_mrp_event_i(evt_ev), .evt_acc_latency_i(evt_lat), \
      .evt_failure_system_id_i(evt_fsys), .evt_failure_code_i(evt_fcode), \
      .join_tick_i(join_tick), .periodic_tick_i(per_tick), .leaveall_rx_i(la_rx), \
      .leaveall_own_i(la_own), .txop_done_o(ls_done``sfx), .ev_valid_o(ls_evv``sfx), \
      .ev_ready_i(ev_ready), .ev_app_o(ls_eva``sfx), .ev_attr_type_o(ls_evt``sfx), \
      .ev_event_o(ls_eve``sfx), .ev_fourpack_o(ls_evf``sfx), .ev_value_o(ls_evx``sfx), \
      .user_valid_o(ls_uv``sfx), .user_join_o(ls_uj``sfx), .user_vid_o(ls_uvid``sfx), \
      .user_ready_i(user_ready), .now_ms_i(now_ms_i), .arm_valid_o(ls_av``sfx), \
      .arm_cancel_o(ls_ac``sfx), .arm_slot_o(ls_as``sfx), .arm_owner_o(ls_ao``sfx), \
      .arm_deadline_ms_o(ls_ad``sfx), .exp_valid_i(exp_valid), .exp_slot_i(exp_slot), \
      .evt_tk_registered_o(ls_r``sfx), .evt_tk_unregistered_o(ls_u``sfx), \
      .evt_tk_fail_chg_o(ls_f``sfx), .evt_tk_latency_chg_o(ls_l``sfx), \
      .tk_reg_state_o(ls_trs``sfx), .lstn_decl_state_o(ls_lds``sfx), \
      .acc_latency_o(ls_al``sfx), .msrp_fail_code_o(ls_fc``sfx), \
      .msrp_fail_bridge_o(ls_fb``sfx), .dbg_app_state_o(ls_das``sfx), .dbg_reg_state_o(ls_drs``sfx)

  logic ls_cr_r, ls_cr_n, ls_done_r, ls_done_n, ls_evv_r, ls_evv_n, ls_eva_r, ls_eva_n;
  logic [7:0] ls_evt_r, ls_evt_n; logic [2:0] ls_eve_r, ls_eve_n; logic [1:0] ls_evf_r, ls_evf_n;
  logic [271:0] ls_evx_r, ls_evx_n; logic ls_uv_r, ls_uv_n, ls_uj_r, ls_uj_n;
  logic [11:0] ls_uvid_r, ls_uvid_n; logic ls_av_r, ls_av_n, ls_ac_r, ls_ac_n;
  logic [AW-1:0] ls_as_r, ls_as_n; logic [7:0] ls_ao_r, ls_ao_n; logic [31:0] ls_ad_r, ls_ad_n;
  logic [N-1:0] ls_r_r, ls_r_n, ls_u_r, ls_u_n, ls_f_r, ls_f_n, ls_l_r, ls_l_n;
  logic [N-1:0][1:0] ls_trs_r, ls_trs_n, ls_lds_r, ls_lds_n, ls_drs_r, ls_drs_n;
  logic [N-1:0][31:0] ls_al_r, ls_al_n; logic [N-1:0][7:0] ls_fc_r, ls_fc_n;
  logic [N-1:0][63:0] ls_fb_r, ls_fb_n; logic [N-1:0][3:0] ls_das_r, ls_das_n;

  KL_srp_listener_fsm_ref #(.N_SINKS_P(N), .SLOT_BASE_P(24), .SLOT_AW_P(AW), .LEAVE_MS_P(50))
    u_ls_ref (`LS_PORTS(_r));
  KL_srp_listener_fsm_new #(.N_SINKS_P(N), .SLOT_BASE_P(24), .SLOT_AW_P(AW), .LEAVE_MS_P(50))
    u_ls_new (`LS_PORTS(_n));

  wire ls_diff = (ls_cr_r != ls_cr_n) || (ls_done_r != ls_done_n) || (ls_evv_r != ls_evv_n)
              || (ls_eva_r != ls_eva_n) || (ls_evt_r != ls_evt_n) || (ls_eve_r != ls_eve_n)
              || (ls_evf_r != ls_evf_n) || (ls_evx_r != ls_evx_n) || (ls_uv_r != ls_uv_n)
              || (ls_uj_r != ls_uj_n) || (ls_uvid_r != ls_uvid_n) || (ls_av_r != ls_av_n)
              || (ls_ac_r != ls_ac_n) || (ls_as_r != ls_as_n) || (ls_ao_r != ls_ao_n)
              || (ls_ad_r != ls_ad_n) || (ls_r_r != ls_r_n) || (ls_u_r != ls_u_n)
              || (ls_f_r != ls_f_n) || (ls_l_r != ls_l_n) || (ls_trs_r != ls_trs_n)
              || (ls_lds_r != ls_lds_n) || (ls_al_r != ls_al_n) || (ls_fc_r != ls_fc_n)
              || (ls_fb_r != ls_fb_n) || (ls_das_r != ls_das_n) || (ls_drs_r != ls_drs_n);

  // ---------------------------------------------------------- admission x2
  logic [N-1:0] ad_adm_r, ad_adm_n; logic [N-1:0][31:0] ad_gs_r, ad_gs_n;
  logic [31:0] ad_sum_r, ad_sum_n; logic ad_ov_r, ad_ov_n, ad_rd_r, ad_rd_n;
  KL_srp_admission_ref #(.N_SOURCES_P(N)) u_ad_ref (
      .clk_i(clk_i), .rst_n(rst_n), .req_i(req_r), .invalidate_i(inv_w),
      .max_frame_i(amfs_r), .interval_frames_i(amif_r), .port_rate_bps_i(rate_r),
      .sr_admitted_o(ad_adm_r), .granted_slope_bps_o(ad_gs_r), .sum_slope_bps_o(ad_sum_r),
      .over_limit_o(ad_ov_r), .round_done_o(ad_rd_r));
  KL_srp_admission_new #(.N_SOURCES_P(N)) u_ad_new (
      .clk_i(clk_i), .rst_n(rst_n), .req_i(req_r), .invalidate_i(inv_w),
      .max_frame_i(amfs_r), .interval_frames_i(amif_r), .port_rate_bps_i(rate_r),
      .sr_admitted_o(ad_adm_n), .granted_slope_bps_o(ad_gs_n), .sum_slope_bps_o(ad_sum_n),
      .over_limit_o(ad_ov_n), .round_done_o(ad_rd_n));
  wire ad_diff = (ad_adm_r != ad_adm_n) || (ad_gs_r != ad_gs_n) || (ad_sum_r != ad_sum_n)
              || (ad_ov_r != ad_ov_n) || (ad_rd_r != ad_rd_n);

  // ------------------------------------------------- compare and coverage
  logic seen_rst_r;
  initial seen_rst_r = 1'b0;
  always_ff @(posedge clk_i) begin : cmp
    if (!rst_n) seen_rst_r <= 1'b1;
    if (seen_rst_r) begin
      if (tk_diff) mis_tk_o <= mis_tk_o + 1;
      if (ls_diff) mis_ls_o <= mis_ls_o + 1;
      if (ad_diff) mis_ad_o <= mis_ad_o + 1;
      if (rst_n) begin
        if (tk_evv_n && ev_ready) cov_tk_push_o <= cov_tk_push_o + 1;
        if (ls_evv_n && ev_ready) cov_ls_push_o <= cov_ls_push_o + 1;
        if (gate_valid && tk_gr_n && gate_open && u_tk_new.rec_valid_r[gate_src])
          cov_redecl_o <= cov_redecl_o + 1;
        if (ctl_valid && ls_cr_n && ctl_settle && u_ls_new.rec_valid_r[ctl_sink])
          cov_resettle_o <= cov_resettle_o + 1;
        if (ad_rd_n) cov_round_o <= cov_round_o + 1;
        if (tk_evv_n && ev_ready && (N > 2)) cov_walk_ram_o <= cov_walk_ram_o + 1;
        if (|tk_lrc_n) cov_tk_reg_o <= cov_tk_reg_o + 1;
        if (|ls_r_n) cov_ls_reg_o <= cov_ls_reg_o + 1;
      end
    end
  end
  initial begin
    mis_tk_o = 0; mis_ls_o = 0; mis_ad_o = 0; cov_tk_push_o = 0; cov_ls_push_o = 0;
    cov_redecl_o = 0; cov_resettle_o = 0; cov_round_o = 0; cov_walk_ram_o = 0;
    cov_tk_reg_o = 0; cov_ls_reg_o = 0;
  end
endmodule
`default_nettype wire
