/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : cosim_top.sv
//  Project     : Milan FPGA -- saved state and fast connect
//                (docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md, the whole
//                 snapshot-ownership contract)
//
//  Description : The RTL half of the co-simulation. It instantiates the REAL
//                donor producer path at the pinned revision --
//                KL_acmp_nvm_shadow (the binding record manager, the only
//                record writer the donor has) driving KL_pp_nvm_port (the
//                device-face initiator) -- the REAL donor KL_aecp_dyn_state
//                (the AECP dynamic-state store whose sticky dirty level the
//                parent consumes), and the SHIPPING hdl/milan/KL_nvm_backend.
//
//                NVM_CONTRACT_3 selects which control face the backend under
//                test carries. It is defined for the shipping module; a build
//                WITHOUT it compiles a backend from before the contract, and
//                that is how the suite's non-vacuity control runs the three
//                historical defects (A2, B1, E1) red on the source they were
//                reproduced against.
//
//                The parent glue between them is TRANSCRIBED from
//                hdl/milan/KL_pp_shadow.sv and says so where it is: the
//                level-and-alarm wiring the contract specifies, and the dyn
//                rising-edge detector the tracked parent derived before it.
//                The processor's millisecond tick is a divider here, as
//                tick_ms_w is a divider in the processor.
//
//                Two harness faces stand in for things that are not in scope:
//                the listener's record-write port (cap_*) and the uCPU's
//                state-port write (dyn_*) are driven by bus-functional
//                models, and a device-face BFM (bfm_*) can take the
//                backend's device face over while the port is idle, to
//                produce operations the donor manager does not produce on
//                demand (an ERASE with no WRITE behind it, an abandoned
//                stream, a partial WRITE). Every case says which it uses.
//---------------------------------------------------------------------------//
`default_nettype none

module cosim_top
  import pp_acmp_pkg::*;
#(
    parameter int unsigned CLK_HZ_P       = 1_000_000,
    parameter int unsigned N_STREAM_IN_P  = 2,
    parameter int unsigned N_STREAM_OUT_P = 2,
    parameter int unsigned N_SPORT_IN_P   = 1,
    parameter int unsigned N_SPORT_OUT_P  = 1,
    parameter int unsigned N_AUDIO_UNIT_P = 1,
    parameter int unsigned N_CLK_DOM_P    = 1,
    parameter int unsigned N_NAME_P       = 38,
    parameter int unsigned T_HOLD_MS_P    = 50,
    parameter int unsigned CAP_ID_W_P     = 16
) (
    input  wire         clk_i,
    input  wire         rst_n,

    //! ---- listener record-write BFM -> the real binding manager ----------
    input  wire         cap_wr_i,
    input  wire  [7:0]  cap_sink_i,
    input  wire         cap_bound_i,
    input  wire         cap_started_i,
    input  wire         cap_sw_i,
    input  wire  [15:0] cap_uid_i,
    input  wire  [63:0] cap_teid_i,
    input  wire  [63:0] cap_ceid_i,

    //! ---- uCPU state-port write BFM -> the real dynamic-state store ------
    input  wire         dyn_wr_i,
    input  wire  [12:0] dyn_sel_i,
    input  wire  [15:0] dyn_idx_i,
    input  wire  [63:0] dyn_val_i,

    //! ---- PP_CTRL[1], the restore go the firmware sets --------------------
    input  wire         restore_go_i,

    //! ---- device-face BFM takeover ---------------------------------------
    input  wire         bfm_sel_i,
    input  wire         bfm_req_i,
    input  wire  [1:0]  bfm_op_i,
    input  wire  [7:0]  bfm_region_i,
    input  wire  [15:0] bfm_offset_i,
    input  wire  [15:0] bfm_len_i,
    input  wire         bfm_wvalid_i,
    input  wire  [7:0]  bfm_wdata_i,
    input  wire         bfm_rready_i,

    //! ---- the backend's memory face, to the C++ memory model -------------
    output logic        mem_req_valid_o,
    input  wire         mem_req_ready_i,
    output logic [31:0] mem_req_addr_o,
    output logic [8:0]  mem_req_beats_o,
    input  wire         mem_rsp_valid_i,
    output logic        mem_rsp_ready_o,
    input  wire  [63:0] mem_rsp_data_i,
    input  wire         mem_rsp_last_i,
    input  wire         mem_rsp_err_i,
    output logic        mem_wr_valid_o,
    input  wire         mem_wr_ready_i,
    output logic [31:0] mem_wr_addr_o,
    output logic [63:0] mem_wr_data_o,
    output logic [7:0]  mem_wr_strb_o,
    input  wire         mem_wr_done_i,
    input  wire         mem_wr_err_i,

    //! ---- the backend's control face (PP_NVM_SEL/DATA/STAT) --------------
    input  wire         csr_sel_i,
    input  wire         csr_we_i,
    input  wire  [5:0]  csr_addr_i,
    input  wire  [31:0] csr_wdata_i,
    output logic [31:0] csr_rdata_o,

    //! ---- observation -----------------------------------------------------
    output logic        nvm_backed_o,
    output logic        nvm_dirty_o,
    output logic        nvm_stale_o,
    output logic [3:0]  nvm_verdict_o,
    output logic        nvm_img_valid_o,
    output logic        nvm_pend_o,
    output logic        nvm_unres_o,
    output logic        restore_busy_o,
    output logic        restore_done_o,
    output logic        restore_fail_o,
    output logic        restore_blank_o,
    output logic        alarm_o,
    output logic [N_STREAM_IN_P-1:0] mgr_dirty_o,
    output logic        port_busy_o,
    output logic        dyn_dirty_o,
    output logic [63:0] dyn_fmt_in0_o,
    output logic        dyn_fmt_in0_v_o,
    output logic        pre_valid_o,
    output logic [15:0] pre_sink_o,
    output logic [63:0] pre_talker_eid_o,
    output logic [15:0] pre_talker_uid_o,
    output logic [63:0] pre_ctlr_eid_o,
    output logic        pre_sw_o,
    output logic        pre_started_o,
    output logic        dev_req_o,
    output logic        dev_gnt_o,
    output logic [1:0]  dev_op_o,
    output logic [7:0]  dev_region_o,
    output logic        dev_wready_o,
    output logic        dev_rvalid_o,
    output logic [7:0]  dev_rdata_o,
    output logic        dev_busy_o,
    output logic        dev_done_o,
    output logic        dev_err_o,
    output logic        tick_ms_o
);

  // ---- the processor's millisecond tick (tick_ms_w), a divider -----------
  localparam int unsigned MS_DIV_C = CLK_HZ_P / 1000;
  logic [31:0] ms_cnt_r;
  logic        tick_ms_w;
  assign tick_ms_w = (ms_cnt_r == 32'd0);
  always_ff @(posedge clk_i) begin
    if (!rst_n) ms_cnt_r <= 32'(MS_DIV_C - 1);
    else        ms_cnt_r <= tick_ms_w ? 32'(MS_DIV_C - 1) : ms_cnt_r - 32'd1;
  end
  assign tick_ms_o = tick_ms_w;

  // ---- the real dynamic-state store --------------------------------------
  localparam int unsigned SIW_C = (N_STREAM_IN_P > 1) ? $clog2(N_STREAM_IN_P) : 1;
  logic [N_STREAM_OUT_P*32-1:0] pt_nc_w;
  logic [N_STREAM_OUT_P-1:0]    ptv_nc_w, fov_nc_w;
  logic [N_STREAM_IN_P*64-1:0]  fin_w;
  logic [N_STREAM_IN_P-1:0]     finv_w;
  logic [N_STREAM_OUT_P*64-1:0] fo_nc_w;
  logic [15:0] cfg_nc_w, cs_nc_w, wr_nc_w, oob_nc_w;
  logic [7:0]  id_nc_w;
  logic        st_ready_nc_w, st_rvalid_nc_w;
  logic [63:0] st_rdata_nc_w;
  logic        aecp_dyn_dirty_w;

  KL_aecp_dyn_state #(
      .N_STREAM_IN_P  (N_STREAM_IN_P),
      .N_STREAM_OUT_P (N_STREAM_OUT_P),
      .N_AUDIO_UNIT_P (N_AUDIO_UNIT_P),
      .N_CLK_DOMAIN_P (N_CLK_DOM_P),
      .N_CONTROL_P    (1)
  ) u_dyn (
      .clk_i           (clk_i),
      .rst_n           (rst_n),
      .st_req_i        (dyn_wr_i),
      .st_we_i         (1'b1),
      //! region 0x1 is the value (KL_aecp_dyn_state RGN_DYN_C), [15:3] the
      //! field selector
      .st_addr_i       ({4'h1, dyn_sel_i, 3'b000}),
      .st_wdata_i      (dyn_val_i),
      .st_ready_o      (st_ready_nc_w),
      .st_rvalid_o     (st_rvalid_nc_w),
      .st_rdata_o      (st_rdata_nc_w),
      .desc_index_i    (dyn_idx_i),
      .cur_config_o    (cfg_nc_w),
      .identify_o      (id_nc_w),
      .clk_src_index_o (cs_nc_w),
      .pt_offset_o     (pt_nc_w),
      .pt_offset_v_o   (ptv_nc_w),
      .fmt_in_o        (fin_w),
      .fmt_in_v_o      (finv_w),
      .fmt_out_o       (fo_nc_w),
      .fmt_out_v_o     (fov_nc_w),
      .dirty_o         (aecp_dyn_dirty_w),
      .dbg_writes_o    (wr_nc_w),
      .dbg_oob_o       (oob_nc_w)
  );
  assign dyn_dirty_o     = aecp_dyn_dirty_w;
  assign dyn_fmt_in0_o   = fin_w[63:0];
  assign dyn_fmt_in0_v_o = finv_w[0];

  // ---- the real binding manager ------------------------------------------
  acmp_rec_t cap_rec_w;
  always_comb begin
    cap_rec_w               = '0;
    cap_rec_w.f_bound       = cap_bound_i;
    cap_rec_w.f_started     = cap_started_i;
    cap_rec_w.f_sw          = cap_sw_i;
    cap_rec_w.talker_uid    = cap_uid_i;
    cap_rec_w.talker_eid    = cap_teid_i;
    cap_rec_w.bind_ctlr_eid = cap_ceid_i;
  end

  logic        nvm_req_w, nvm_we_w, nvm_wvalid_w, nvm_wready_w;
  logic [7:0]  nvm_record_id_w, nvm_wdata_w, nvm_rdata_w;
  logic        nvm_rvalid_w, nvm_rready_w, nvm_busy_w, nvm_done_w, nvm_err_w;
  logic [N_STREAM_IN_P-1:0] mgr_dirty_w, mgr_valid_nc_w, mgr_touched_nc_w;
  logic        mgr_alarm_w, pp_restore_done_w, pp_restore_fail_w, pp_restore_blank_w;

  KL_acmp_nvm_shadow #(
      .N_SINKS_P (N_STREAM_IN_P)
  ) u_nvm_shadow (
      .clk_i            (clk_i),
      .rst_n            (rst_n),
      .tick_i           (tick_ms_w),
      .restore_go_i     (restore_go_i),
      .restore_busy_o   (restore_busy_o),
      .restore_done_o   (pp_restore_done_w),
      .restore_fail_o   (pp_restore_fail_w),
      .restore_blank_o  (pp_restore_blank_w),
      .alarm_o          (mgr_alarm_w),
      .cap_wr_i         (cap_wr_i),
      .cap_sink_i       (SIW_C'(cap_sink_i)),
      .cap_rec_i        (cap_rec_w),
      .pre_valid_o      (pre_valid_o),
      .pre_sink_o       (pre_sink_o),
      .pre_talker_eid_o (pre_talker_eid_o),
      .pre_talker_uid_o (pre_talker_uid_o),
      .pre_ctlr_eid_o   (pre_ctlr_eid_o),
      .pre_sw_o         (pre_sw_o),
      .pre_started_o    (pre_started_o),
      .pre_ready_i      (1'b1),
      .nvm_req_o        (nvm_req_w),
      .nvm_we_o         (nvm_we_w),
      .nvm_record_id_o  (nvm_record_id_w),
      .nvm_wvalid_o     (nvm_wvalid_w),
      .nvm_wready_i     (nvm_wready_w),
      .nvm_wdata_o      (nvm_wdata_w),
      .nvm_rvalid_i     (nvm_rvalid_w),
      .nvm_rready_o     (nvm_rready_w),
      .nvm_rdata_i      (nvm_rdata_w),
      .nvm_busy_i       (nvm_busy_w),
      .nvm_done_i       (nvm_done_w),
      .nvm_err_i        (nvm_err_w),
      .dbg_dirty_o      (mgr_dirty_w),
      .dbg_valid_o      (mgr_valid_nc_w),
      .dbg_touched_o    (mgr_touched_nc_w)
  );
  assign mgr_dirty_o = mgr_dirty_w;
  assign alarm_o     = mgr_alarm_w;
  assign port_busy_o = nvm_busy_w;

  // ---- the real port --------------------------------------------------------
  logic        p_dev_req_w, p_dev_wvalid_w, p_dev_rready_w;
  logic [1:0]  p_dev_op_w;
  logic [7:0]  p_dev_region_w, p_dev_wdata_w;
  logic [15:0] p_dev_offset_w, p_dev_len_w;
  logic        b_gnt_w, b_wready_w, b_rvalid_w, b_busy_w, b_done_w, b_err_w;
  logic [7:0]  b_rdata_w;

  KL_pp_nvm_port u_nvm_port (
      .clk_i           (clk_i),
      .rst_n           (rst_n),
      .nvm_req_i       (nvm_req_w),
      .nvm_we_i        (nvm_we_w),
      .nvm_record_id_i (nvm_record_id_w),
      .nvm_wvalid_i    (nvm_wvalid_w),
      .nvm_wready_o    (nvm_wready_w),
      .nvm_wdata_i     (nvm_wdata_w),
      .nvm_rvalid_o    (nvm_rvalid_w),
      .nvm_rready_i    (nvm_rready_w),
      .nvm_rdata_o     (nvm_rdata_w),
      .nvm_busy_o      (nvm_busy_w),
      .nvm_done_o      (nvm_done_w),
      .nvm_err_o       (nvm_err_w),
      .dev_req_o       (p_dev_req_w),
      //! the port sees nothing of the backend while the BFM owns the face
      .dev_gnt_i       (b_gnt_w    & ~bfm_sel_i),
      .dev_op_o        (p_dev_op_w),
      .dev_region_o    (p_dev_region_w),
      .dev_offset_o    (p_dev_offset_w),
      .dev_len_o       (p_dev_len_w),
      .dev_wvalid_o    (p_dev_wvalid_w),
      .dev_wready_i    (b_wready_w & ~bfm_sel_i),
      .dev_wdata_o     (p_dev_wdata_w),
      .dev_rvalid_i    (b_rvalid_w & ~bfm_sel_i),
      .dev_rdata_i     (b_rdata_w),
      .dev_rready_o    (p_dev_rready_w),
      .dev_busy_i      (b_busy_w),
      .dev_done_i      (b_done_w   & ~bfm_sel_i),
      .dev_err_i       (b_err_w    & ~bfm_sel_i)
  );

  // ---- the device-face mux -------------------------------------------------
  logic        d_req_w, d_wvalid_w, d_rready_w;
  logic [1:0]  d_op_w;
  logic [7:0]  d_region_w, d_wdata_w;
  logic [15:0] d_offset_w, d_len_w;
  assign d_req_w    = bfm_sel_i ? bfm_req_i    : p_dev_req_w;
  assign d_op_w     = bfm_sel_i ? bfm_op_i     : p_dev_op_w;
  assign d_region_w = bfm_sel_i ? bfm_region_i : p_dev_region_w;
  assign d_offset_w = bfm_sel_i ? bfm_offset_i : p_dev_offset_w;
  assign d_len_w    = bfm_sel_i ? bfm_len_i    : p_dev_len_w;
  assign d_wvalid_w = bfm_sel_i ? bfm_wvalid_i : p_dev_wvalid_w;
  assign d_wdata_w  = bfm_sel_i ? bfm_wdata_i  : p_dev_wdata_w;
  assign d_rready_w = bfm_sel_i ? bfm_rready_i : p_dev_rready_w;

  assign dev_req_o    = d_req_w;
  assign dev_op_o     = d_op_w;
  assign dev_region_o = d_region_w;
  assign dev_gnt_o    = b_gnt_w;
  assign dev_wready_o = b_wready_w;
  assign dev_rvalid_o = b_rvalid_w;
  assign dev_rdata_o  = b_rdata_w;
  assign dev_busy_o   = b_busy_w;
  assign dev_done_o   = b_done_w;
  assign dev_err_o    = b_err_w;

  // ---- the parent glue ------------------------------------------------------
`ifdef NVM_CONTRACT_3
  //! The sticky level IS the ownership of an unmaterialised change, so it is
  //! passed as a level (snapshot-ownership section 6.1); the manager's
  //! unflushed sinks are the second term, and at the pinned processor they
  //! are a real output port (donor scope D1, nvm_unflushed_o) rather than
  //! something this harness models — the same dbg_dirty_o the shadow above
  //! drives. The alarm the processor already exports reaches the backend.
  //!
  //! The glue's THIRD term, the sticky bit an AECP commit mark of class 6 or
  //! 7 sets (donor scope D2), has no producer here: this harness elaborates
  //! the dynamic-state store and the binding manager, not the AECP engine, so
  //! no mark can be raised and the term would be a constant. It is graded
  //! where its producer is, in the processor's own pp_top suite.
  logic pend_w;
  assign pend_w = aecp_dyn_dirty_w | (|mgr_dirty_w);
`else
  //! TRANSCRIBED from the parent glue BEFORE the contract: the rising edge
  //! of the sticky dyn level was the backend's change_i, which is the issue
  //! #420 defect the pending bit replaces.
  logic dyn_dirty_q;
  logic nvm_change_w;
  assign nvm_change_w = aecp_dyn_dirty_w & ~dyn_dirty_q;
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) dyn_dirty_q <= 1'b0;
    else        dyn_dirty_q <= aecp_dyn_dirty_w;
  end
`endif

  //! TRANSCRIBED from hdl/milan/KL_pp_shadow.sv:890-907 and :1391-1392: a
  //! walk that ran with no validated image behind the face is a failed one
  logic restore_busy_q, walk_blind_r, img_valid_w;
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      restore_busy_q <= 1'b0;
      walk_blind_r   <= 1'b1;
    end else begin
      restore_busy_q <= restore_busy_o;
      if (restore_busy_o && !restore_busy_q)   walk_blind_r <= ~img_valid_w;
      else if (restore_busy_o && !img_valid_w) walk_blind_r <= 1'b1;
    end
  end
  assign restore_done_o  = pp_restore_done_w;
  assign restore_blank_o = pp_restore_blank_w;
  assign restore_fail_o  = pp_restore_fail_w || (pp_restore_done_w && walk_blind_r);

  // ---- the backend -----------------------------------------------------------
  KL_nvm_backend #(
      .CLK_HZ_P       (CLK_HZ_P),
      .N_STREAM_IN_P  (N_STREAM_IN_P),
      .N_STREAM_OUT_P (N_STREAM_OUT_P),
      .N_SPORT_IN_P   (N_SPORT_IN_P),
      .N_SPORT_OUT_P  (N_SPORT_OUT_P),
      .N_AUDIO_UNIT_P (N_AUDIO_UNIT_P),
      .N_CLK_DOM_P    (N_CLK_DOM_P),
      .N_NAME_P       (N_NAME_P)
`ifdef NVM_CONTRACT_3
     ,.T_HOLD_MS_P    (T_HOLD_MS_P)
     ,.CAP_ID_W_P     (CAP_ID_W_P)
`endif
  ) u_nvm (
      .clk_i           (clk_i),
      .rst_n           (rst_n),
      .dev_req_i       (d_req_w),
      .dev_gnt_o       (b_gnt_w),
      .dev_op_i        (d_op_w),
      .dev_region_i    (d_region_w),
      .dev_offset_i    (d_offset_w),
      .dev_len_i       (d_len_w),
      .dev_wvalid_i    (d_wvalid_w),
      .dev_wready_o    (b_wready_w),
      .dev_wdata_i     (d_wdata_w),
      .dev_rvalid_o    (b_rvalid_w),
      .dev_rdata_o     (b_rdata_w),
      .dev_rready_i    (d_rready_w),
      .dev_busy_o      (b_busy_w),
      .dev_done_o      (b_done_w),
      .dev_err_o       (b_err_w),
      .mem_req_valid_o (mem_req_valid_o),
      .mem_req_ready_i (mem_req_ready_i),
      .mem_req_addr_o  (mem_req_addr_o),
      .mem_req_beats_o (mem_req_beats_o),
      .mem_rsp_valid_i (mem_rsp_valid_i),
      .mem_rsp_ready_o (mem_rsp_ready_o),
      .mem_rsp_data_i  (mem_rsp_data_i),
      .mem_rsp_last_i  (mem_rsp_last_i),
      .mem_rsp_err_i   (mem_rsp_err_i),
      .mem_wr_valid_o  (mem_wr_valid_o),
      .mem_wr_ready_i  (mem_wr_ready_i),
      .mem_wr_addr_o   (mem_wr_addr_o),
      .mem_wr_data_o   (mem_wr_data_o),
      .mem_wr_strb_o   (mem_wr_strb_o),
      .mem_wr_done_i   (mem_wr_done_i),
      .mem_wr_err_i    (mem_wr_err_i),
      .csr_sel_i       (csr_sel_i),
      .csr_we_i        (csr_we_i),
      .csr_addr_i      (csr_addr_i),
      .csr_wdata_i     (csr_wdata_i),
      .csr_rdata_o     (csr_rdata_o),
`ifdef NVM_CONTRACT_3
      .pend_i          (pend_w),
      .alarm_i         (mgr_alarm_w),
      .nvm_pend_o      (nvm_pend_o),
      .nvm_unres_o     (nvm_unres_o),
`else
      .change_i        (nvm_change_w),
`endif
      .nvm_backed_o    (nvm_backed_o),
      .nvm_dirty_o     (nvm_dirty_o),
      .nvm_stale_o     (nvm_stale_o),
      .nvm_verdict_o   (nvm_verdict_o),
      .img_valid_o     (img_valid_w)
  );
  assign nvm_img_valid_o = img_valid_w;
`ifndef NVM_CONTRACT_3
  assign nvm_pend_o  = 1'b0;
  assign nvm_unres_o = 1'b0;
`endif

endmodule

`default_nettype wire
