/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : d3_top.sv   (design evidence, milan-fpga #500, scope D3)
//
//  Description : The RTL half of the D3 co-simulation. REAL, at the pinned
//                processor revision 424c688f: KL_aecp_dyn_state (the
//                dynamic-state store), KL_aecp_desc_store (the descriptor
//                store and its writable name table, walking a real AEMI
//                image the firmware copies into the model's DDR),
//                KL_acmp_nvm_shadow (the binding manager) and KL_pp_nvm_port.
//                SHIPPING: hdl/milan/KL_nvm_backend.sv at dev 07294a76.
//                PROTOTYPE: KL_aecp_nvm_writer (the D3 record writer) and
//                KL_pp_nvm_mgr_arb (two managers, one port).
//
//                The uCPU is a bus-functional model on the state bus
//                (ub_*), with the dispatch hold-off the page specifies: it
//                starts no program while the writer owns the bus (own_o),
//                and the writer takes the bus only while no program runs
//                (prog_busy_i). The channel-map store, the GET_AUDIO_MAP
//                read face, the map edit face and the format judge are a
//                C++ model of the parent's map plane (d3_bridge.cpp).
//
//                The parent glue is TRANSCRIBED from hdl/milan/KL_pp_shadow.sv
//                with the change the page specifies: the D3 writer's
//                unflushed level REPLACES aecp_dyn_dirty_o and the sticky
//                class-6/7 mark bit in pend_i, and the processor's restore
//                done is the AND of the two walks.
//
//                D3_TRACKED (a build define) is the glue AS IT SHIPS at dev
//                07294a76: no D3 writer, pend_i = aecp_dyn_dirty_o OR the
//                binding manager's unflushed sinks OR the sticky class-6/7
//                mark bit, and the restore is the binding walk alone. It is
//                what "what reproduces today" runs against.
//---------------------------------------------------------------------------//
`default_nettype none

module d3_top
  import pp_acmp_pkg::*;
#(
    parameter int unsigned CLK_HZ_P       = 1_000_000,
    parameter int unsigned N_STREAM_IN_P  = 2,
    parameter int unsigned N_STREAM_OUT_P = 2,
    parameter int unsigned N_SPORT_IN_P   = 1,
    parameter int unsigned N_SPORT_OUT_P  = 1,
    parameter int unsigned N_AUDIO_UNIT_P = 1,
    parameter int unsigned N_CLK_DOM_P    = 1,
    parameter int unsigned N_NAME_P       = 30,
    parameter logic [8*N_SPORT_IN_P-1:0]  MAPI_CLS_P = '0,
    parameter logic [8*N_SPORT_OUT_P-1:0] MAPO_CLS_P = '0,
    parameter int unsigned MAP_ENT_MAX_P  = 17,
    parameter int unsigned IDX_ENTRIES_P  = 32,
    parameter int unsigned D3_DEB_TICKS_P = 500,
    parameter int unsigned T_HOLD_MS_P    = 50
) (
    input  wire         clk_i,
    input  wire         rst_n,

    //! ---- listener record-write BFM -> the real binding manager ---------
    input  wire         cap_wr_i,
    input  wire  [7:0]  cap_sink_i,
    input  wire         cap_bound_i,
    input  wire         cap_started_i,
    input  wire         cap_sw_i,
    input  wire  [15:0] cap_uid_i,
    input  wire  [63:0] cap_teid_i,
    input  wire  [63:0] cap_ceid_i,

    //! ---- the uCPU BFM on the state bus ------------------------------------
    input  wire         prog_busy_i,
    input  wire         ub_req_i,
    input  wire         ub_we_i,
    input  wire         ub_name_i,
    input  wire  [19:0] ub_addr_i,
    input  wire  [63:0] ub_wdata_i,
    input  wire  [15:0] ub_didx_i,
    output logic        ub_ready_o,
    output logic        ub_rvalid_o,
    output logic [63:0] ub_rdata_o,
    output logic        ub_err_o,
    output logic        own_o,
    //! the commit mark a program raises (class and command descriptor), and
    //! the map edit face's commit-one-record beat the map model applies
    input  wire         mk_stb_i,
    input  wire  [7:0]  mk_mark_i,
    input  wire  [15:0] mk_type_i,
    input  wire  [15:0] mk_idx_i,
    input  wire         me_stb_i,
    input  wire  [15:0] me_type_i,
    input  wire  [15:0] me_idx_i,

    //! ---- PP_CTRL[1] ----------------------------------------------------------
    input  wire         restore_go_i,
    //! harness knob: hold the writer's change snoop off (stale-store control)
    input  wire         snoop_off_i,

    //! ---- the descriptor store's memory face, to the C++ DDR model --------
    output logic        dm_req_valid_o,
    input  wire         dm_req_ready_i,
    output logic [31:0] dm_req_addr_o,
    output logic [8:0]  dm_req_beats_o,
    input  wire         dm_rsp_valid_i,
    input  wire  [63:0] dm_rsp_data_i,
    input  wire         dm_rsp_last_i,
    input  wire         dm_rsp_err_i,

    //! ---- the map plane faces, to the C++ map model -------------------------
    output logic        am_req_o,
    output logic [15:0] am_type_o,
    output logic [15:0] am_idx_o,
    output logic [15:0] am_map_o,
    output logic [1:0]  am_sel_o,
    output logic [7:0]  am_rec_o,
    input  wire  [63:0] am_data_i,
    input  wire         am_wait_i,
    output logic        mr_req_o,
    output logic        mr_add_o,
    output logic [15:0] mr_type_o,
    output logic [15:0] mr_idx_o,
    output logic [7:0]  mr_cnt_o,
    output logic        mr_ent_v_o,
    output logic [63:0] mr_ent_o,
    input  wire         mr_ent_rdy_i,
    input  wire         mr_done_i,
    input  wire         mr_ok_i,
    output logic        fj_req_o,
    output logic        fj_out_o,
    output logic [15:0] fj_idx_o,
    output logic [63:0] fj_fmt_o,
    input  wire         fj_wait_i,
    input  wire  [1:0]  fj_data_i,

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

    //! ---- the backend's control face ----------------------------------------
    input  wire         csr_sel_i,
    input  wire         csr_we_i,
    input  wire  [5:0]  csr_addr_i,
    input  wire  [31:0] csr_wdata_i,
    output logic [31:0] csr_rdata_o,

    //! ---- observation -----------------------------------------------------------
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
    output logic        d3_alarm_o,
    output logic        d3_unflushed_o,
    output logic        d3_restore_done_o,
    output logic        d3_restore_fail_o,
    output logic [7:0]  d3_rs_applied_o,
    output logic [7:0]  d3_rs_refused_o,
    output logic [7:0]  d3_rs_blank_o,
    output logic [7:0]  d3_rs_reverted_o,
    output logic [15:0] d3_writes_o,
    output logic [15:0] d3_slot_o,
    output logic        d3_taint_o,
    output logic [N_AUDIO_UNIT_P + N_CLK_DOM_P + N_STREAM_IN_P + 2*N_STREAM_OUT_P
                  + N_SPORT_IN_P + N_SPORT_OUT_P + N_NAME_P:0] d3_dirty_o,
    output logic [N_STREAM_IN_P-1:0] mgr_dirty_o,
    output logic        mgr_restore_done_o,
    output logic        port_busy_o,
    output logic        desc_img_valid_o,
    output logic [N_STREAM_IN_P*64-1:0]  dyn_fmt_in_o,
    output logic [N_STREAM_IN_P-1:0]     dyn_fmt_in_v_o,
    output logic [N_STREAM_OUT_P*64-1:0] dyn_fmt_out_o,
    output logic [N_STREAM_OUT_P-1:0]    dyn_fmt_out_v_o,
    output logic        dev_req_o,
    output logic        dev_gnt_o,
    output logic [1:0]  dev_op_o,
    output logic [7:0]  dev_region_o,
    output logic        dev_wvalid_o,
    output logic        dev_wready_o,
    output logic [7:0]  dev_wdata_o,
    output logic        dev_busy_o,
    output logic        dev_done_o,
    output logic        dev_err_o,
    output logic        d3_mdone_o,
    output logic        tick_ms_o,
    //! the binding manager's state (KL_acmp_nvm_shadow hs_r, read through
    //! the hierarchy) and the arbiter's grant to the D3 writer: case K15's
    //! premise is a cycle with both H_FL_REQ and that grant
    output logic [3:0]  m0_state_o,
    output logic        arb_m1_gnt_o
);

  // ---- the processor's millisecond tick, a divider ------------------------
  localparam int unsigned MS_DIV_C = CLK_HZ_P / 1000;
  logic [31:0] ms_cnt_r;
  logic        tick_ms_w;
  assign tick_ms_w = (ms_cnt_r == 32'd0);
  always_ff @(posedge clk_i) begin
    if (!rst_n) ms_cnt_r <= 32'(MS_DIV_C - 1);
    else        ms_cnt_r <= tick_ms_w ? 32'(MS_DIV_C - 1) : ms_cnt_r - 32'd1;
  end
  assign tick_ms_o = tick_ms_w;

  // ---- the state bus: the uCPU BFM, or the D3 writer while it owns it ----
  logic        d3_own_w;
  logic        sb_req_w, sb_we_w, sb_name_w;
  logic [19:0] sb_addr_w;
  logic [63:0] sb_wdata_w;
  logic [7:0]  sb_wstrb_w;
  logic [15:0] sb_didx_w;
  logic        st_req_w, st_we_w, st_name_w;
  logic [19:0] st_addr_w;
  logic [63:0] st_wdata_w;
  logic [7:0]  st_wstrb_w;
  logic [15:0] st_didx_w;
  logic        dyn_sel_w;
  logic        dyn_ready_w, dyn_rvalid_w, store_ready_w, store_rvalid_w, store_err_w;
  logic [63:0] dyn_rdata_w, store_rdata_w;
  logic        st_ready_w, st_rvalid_w, st_err_w;
  logic [63:0] st_rdata_w;

  assign st_req_w   = d3_own_w ? sb_req_w   : ub_req_i;
  assign st_we_w    = d3_own_w ? sb_we_w    : ub_we_i;
  assign st_name_w  = d3_own_w ? sb_name_w  : ub_name_i;
  assign st_addr_w  = d3_own_w ? sb_addr_w  : ub_addr_i;
  assign st_wdata_w = d3_own_w ? sb_wdata_w : ub_wdata_i;
  assign st_wstrb_w = d3_own_w ? sb_wstrb_w : 8'hFF;
  assign st_didx_w  = d3_own_w ? sb_didx_w  : ub_didx_i;
  //! KL_aecp_engine's region routing (dyn_sel_w there)
  assign dyn_sel_w  = !st_name_w && ((st_addr_w[19:16] == 4'h1) || (st_addr_w[19:16] == 4'h2));
  assign st_ready_w  = dyn_sel_w ? dyn_ready_w : store_ready_w;
  assign st_rvalid_w = dyn_rvalid_w || store_rvalid_w;
  assign st_rdata_w  = dyn_rvalid_w ? dyn_rdata_w : store_rdata_w;
  assign st_err_w    = store_rvalid_w && store_err_w;
  assign ub_ready_o  = !d3_own_w && st_ready_w;
  assign ub_rvalid_o = !d3_own_w && st_rvalid_w;
  assign ub_rdata_o  = st_rdata_w;
  assign ub_err_o    = st_err_w;
  assign own_o       = d3_own_w;

  // ---- the real dynamic-state store ----------------------------------------
  logic [N_STREAM_OUT_P*32-1:0] pt_nc_w;
  logic [N_STREAM_OUT_P-1:0]    ptv_nc_w;
  logic [15:0] cfg_nc_w, cs_nc_w, wr_nc_w, oob_nc_w;
  logic [7:0]  id_nc_w;
  logic        aecp_dyn_dirty_nc_w;

  KL_aecp_dyn_state #(
      .N_STREAM_IN_P  (N_STREAM_IN_P),
      .N_STREAM_OUT_P (N_STREAM_OUT_P),
      .N_AUDIO_UNIT_P (N_AUDIO_UNIT_P),
      .N_CLK_DOMAIN_P (N_CLK_DOM_P),
      .N_CONTROL_P    (1)
  ) u_dyn (
      .clk_i           (clk_i),
      .rst_n           (rst_n),
      .st_req_i        (st_req_w && dyn_sel_w),
      .st_we_i         (st_we_w),
      .st_addr_i       (st_addr_w),
      .st_wdata_i      (st_wdata_w),
      .st_ready_o      (dyn_ready_w),
      .st_rvalid_o     (dyn_rvalid_w),
      .st_rdata_o      (dyn_rdata_w),
      .desc_index_i    (st_didx_w),
      .cur_config_o    (cfg_nc_w),
      .identify_o      (id_nc_w),
      .clk_src_index_o (cs_nc_w),
      .pt_offset_o     (pt_nc_w),
      .pt_offset_v_o   (ptv_nc_w),
      .fmt_in_o        (dyn_fmt_in_o),
      .fmt_in_v_o      (dyn_fmt_in_v_o),
      .fmt_out_o       (dyn_fmt_out_o),
      .fmt_out_v_o     (dyn_fmt_out_v_o),
      .dirty_o         (aecp_dyn_dirty_nc_w),
      .dbg_writes_o    (wr_nc_w),
      .dbg_oob_o       (oob_nc_w)
  );

  // ---- the real descriptor store -------------------------------------------
  logic [3:0]  img_fault_nc_w;
  logic [15:0] miss_nc_w, fetch_nc_w, rowr_nc_w, dlen_nc_w;
  logic        dm_rsp_ready_nc_w;

  KL_aecp_desc_store #(
      .DESC_BASE_P       (32'h2000_0000),
      .LINE_BYTES_P      (576),
      .IDX_ENTRIES_P     (IDX_ENTRIES_P),
      .NAME_ENTRIES_P    (N_NAME_P),
      .MEM_TIMEOUT_CYC_P (4096)
  ) u_store (
      .clk_i             (clk_i),
      .rst_n             (rst_n),
      .st_req_i          (st_req_w && !dyn_sel_w),
      .st_we_i           (st_we_w),
      .st_name_i         (st_name_w),
      .st_addr_i         (st_addr_w),
      .st_wdata_i        (st_wdata_w),
      .st_wstrb_i        (st_wstrb_w),
      .st_ready_o        (store_ready_w),
      .st_rvalid_o       (store_rvalid_w),
      .st_rdata_o        (store_rdata_w),
      .st_err_o          (store_err_w),
      .mem_req_valid_o   (dm_req_valid_o),
      .mem_req_ready_i   (dm_req_ready_i),
      .mem_req_addr_o    (dm_req_addr_o),
      .mem_req_beats_o   (dm_req_beats_o),
      .mem_rsp_valid_i   (dm_rsp_valid_i),
      .mem_rsp_ready_o   (dm_rsp_ready_nc_w),
      .mem_rsp_data_i    (dm_rsp_data_i),
      .mem_rsp_last_i    (dm_rsp_last_i),
      .mem_rsp_err_i     (dm_rsp_err_i),
      .dbg_img_valid_o   (desc_img_valid_o),
      .dbg_fault_o       (img_fault_nc_w),
      .dbg_locate_miss_o (miss_nc_w),
      .dbg_fetch_cnt_o   (fetch_nc_w),
      .dbg_ro_write_o    (rowr_nc_w),
      .dbg_desc_len_o    (dlen_nc_w)
  );

  // ---- the real binding manager ----------------------------------------------
  localparam int unsigned SIW_C = (N_STREAM_IN_P > 1) ? $clog2(N_STREAM_IN_P) : 1;
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

  logic        m0_req_w, m0_we_w, m0_wvalid_w, m0_wready_w, m0_rvalid_w, m0_rready_w;
  logic        m0_busy_w, m0_done_w, m0_err_w;
  logic [7:0]  m0_rid_w, m0_wdata_w, m0_rdata_w;
  logic [N_STREAM_IN_P-1:0] mgr_dirty_w, mgr_valid_nc_w, mgr_touched_nc_w;
  logic        mgr_alarm_w, mgr_busy_w, mgr_done_w, mgr_fail_w, mgr_blank_w;
  logic        pre_valid_nc_w, pre_sw_nc_w, pre_started_nc_w;
  logic [15:0] pre_sink_nc_w, pre_uid_nc_w;
  logic [63:0] pre_teid_nc_w, pre_ceid_nc_w;

  KL_acmp_nvm_shadow #(
      .N_SINKS_P (N_STREAM_IN_P)
  ) u_nvm_shadow (
      .clk_i            (clk_i),
      .rst_n            (rst_n),
      .tick_i           (tick_ms_w),
      .restore_go_i     (restore_go_i),
      .restore_busy_o   (mgr_busy_w),
      .restore_done_o   (mgr_done_w),
      .restore_fail_o   (mgr_fail_w),
      .restore_blank_o  (mgr_blank_w),
      .alarm_o          (mgr_alarm_w),
      .cap_wr_i         (cap_wr_i),
      .cap_sink_i       (SIW_C'(cap_sink_i)),
      .cap_rec_i        (cap_rec_w),
      .pre_valid_o      (pre_valid_nc_w),
      .pre_sink_o       (pre_sink_nc_w),
      .pre_talker_eid_o (pre_teid_nc_w),
      .pre_talker_uid_o (pre_uid_nc_w),
      .pre_ctlr_eid_o   (pre_ceid_nc_w),
      .pre_sw_o         (pre_sw_nc_w),
      .pre_started_o    (pre_started_nc_w),
      .pre_ready_i      (1'b1),
      .nvm_req_o        (m0_req_w),
      .nvm_we_o         (m0_we_w),
      .nvm_record_id_o  (m0_rid_w),
      .nvm_wvalid_o     (m0_wvalid_w),
      .nvm_wready_i     (m0_wready_w),
      .nvm_wdata_o      (m0_wdata_w),
      .nvm_rvalid_i     (m0_rvalid_w),
      .nvm_rready_o     (m0_rready_w),
      .nvm_rdata_i      (m0_rdata_w),
      .nvm_busy_i       (m0_busy_w),
      .nvm_done_i       (m0_done_w),
      .nvm_err_i        (m0_err_w),
      .dbg_dirty_o      (mgr_dirty_w),
      .dbg_valid_o      (mgr_valid_nc_w),
      .dbg_touched_o    (mgr_touched_nc_w)
  );
  assign mgr_dirty_o        = mgr_dirty_w;
  assign mgr_restore_done_o = mgr_done_w;
  assign m0_state_o         = 4'(u_nvm_shadow.hs_r);

  // ---- the prototype D3 record writer ------------------------------------------
  logic        m1_req_w, m1_we_w, m1_gnt_w, m1_wvalid_w, m1_wready_w;
  logic        m1_rvalid_w, m1_rready_w, m1_done_w, m1_err_w;
  logic [7:0]  m1_rid_w, m1_wdata_w, m1_rdata_w;
  logic        d3_busy_w, d3_done_w, d3_fail_w, d3_alarm_w, d3_unfl_w, d3_blank_w;
  logic        u_dyn_ack_w, u_name_ack_w;
  assign arb_m1_gnt_o = m1_gnt_w;

`ifdef D3_TRACKED
  //! the tracked glue has no D3 writer: nothing owns the state bus but the
  //! uCPU, nothing answers the map faces, and nothing requests the port but
  //! the binding manager
  assign d3_own_w = 1'b0;
  assign {sb_req_w, sb_we_w, sb_name_w} = 3'b000;
  assign sb_addr_w = '0; assign sb_wdata_w = '0; assign sb_wstrb_w = '0; assign sb_didx_w = '0;
  assign {am_req_o, mr_req_o, mr_add_o, mr_ent_v_o, fj_req_o, fj_out_o} = 6'b000000;
  assign am_type_o = '0; assign am_idx_o = '0; assign am_map_o = '0; assign am_sel_o = '0;
  assign am_rec_o = '0; assign mr_type_o = '0; assign mr_idx_o = '0; assign mr_cnt_o = '0;
  assign mr_ent_o = '0; assign fj_idx_o = '0; assign fj_fmt_o = '0;
  assign {m1_req_w, m1_we_w, m1_wvalid_w, m1_rready_w} = 4'b0000;
  assign m1_rid_w = '0; assign m1_wdata_w = '0;
  assign d3_busy_w = 1'b0; assign d3_done_w = mgr_done_w; assign d3_fail_w = 1'b0;
  assign d3_blank_w = 1'b1;
  assign d3_alarm_w = 1'b0; assign d3_unfl_w = 1'b0;
  assign {u_dyn_ack_w, u_name_ack_w} = 2'b00;
  assign d3_rs_applied_o = '0; assign d3_rs_refused_o = '0; assign d3_rs_blank_o = '0;
  assign d3_rs_reverted_o = '0; assign d3_writes_o = '0; assign d3_slot_o = '0;
  assign d3_taint_o = 1'b0; assign d3_dirty_o = '0;
`else
  //! the change sources are the uCPU's own accesses: the writer's restore
  //! writes never reach them, so a restore write is not a change
  assign u_dyn_ack_w  = !snoop_off_i && !d3_own_w && ub_req_i && ub_we_i && dyn_sel_w && dyn_ready_w;
  assign u_name_ack_w = !snoop_off_i && !d3_own_w && ub_req_i && ub_we_i && ub_name_i && store_ready_w;

  KL_aecp_nvm_writer #(
      .N_STREAM_IN_P  (N_STREAM_IN_P),
      .N_STREAM_OUT_P (N_STREAM_OUT_P),
      .N_SPORT_IN_P   (N_SPORT_IN_P),
      .N_SPORT_OUT_P  (N_SPORT_OUT_P),
      .N_AUDIO_UNIT_P (N_AUDIO_UNIT_P),
      .N_CLK_DOM_P    (N_CLK_DOM_P),
      .N_NAME_P       (N_NAME_P),
      .MAPI_CLS_P     (MAPI_CLS_P),
      .MAPO_CLS_P     (MAPO_CLS_P),
      .MAP_ENT_MAX_P  (MAP_ENT_MAX_P),
      .LAYOUT_VER_P   (8'h02),
      .DEB_TICKS_P    (D3_DEB_TICKS_P),
      .RETRY_MAX_P    (2)
  ) u_d3 (
      .clk_i            (clk_i),
      .rst_n            (rst_n),
      .tick_i           (tick_ms_w),
      .u_dyn_ack_i      (u_dyn_ack_w),
      .u_name_ack_i     (u_name_ack_w),
      .u_addr_i         (ub_addr_i),
      .u_didx_i         (ub_didx_i),
      .me_stb_i         (me_stb_i),
      .me_type_i        (me_type_i),
      .me_idx_i         (me_idx_i),
      .prog_busy_i      (prog_busy_i),
      .own_o            (d3_own_w),
      .sb_req_o         (sb_req_w),
      .sb_we_o          (sb_we_w),
      .sb_name_o        (sb_name_w),
      .sb_addr_o        (sb_addr_w),
      .sb_wdata_o       (sb_wdata_w),
      .sb_wstrb_o       (sb_wstrb_w),
      .sb_didx_o        (sb_didx_w),
      .sb_ready_i       (st_ready_w),
      .sb_rvalid_i      (st_rvalid_w),
      .sb_rdata_i       (st_rdata_w),
      .sb_err_i         (st_err_w),
      .desc_img_valid_i (desc_img_valid_o),
      .am_req_o         (am_req_o),
      .am_type_o        (am_type_o),
      .am_idx_o         (am_idx_o),
      .am_map_o         (am_map_o),
      .am_sel_o         (am_sel_o),
      .am_rec_o         (am_rec_o),
      .am_data_i        (am_data_i),
      .am_wait_i        (am_wait_i),
      .mr_req_o         (mr_req_o),
      .mr_add_o         (mr_add_o),
      .mr_type_o        (mr_type_o),
      .mr_idx_o         (mr_idx_o),
      .mr_cnt_o         (mr_cnt_o),
      .mr_ent_v_o       (mr_ent_v_o),
      .mr_ent_o         (mr_ent_o),
      .mr_ent_rdy_i     (mr_ent_rdy_i),
      .mr_done_i        (mr_done_i),
      .mr_ok_i          (mr_ok_i),
      .fj_req_o         (fj_req_o),
      .fj_out_o         (fj_out_o),
      .fj_idx_o         (fj_idx_o),
      .fj_fmt_o         (fj_fmt_o),
      .fj_wait_i        (fj_wait_i),
      .fj_data_i        (fj_data_i),
      .m_req_o          (m1_req_w),
      .m_we_o           (m1_we_w),
      .m_rid_o          (m1_rid_w),
      .m_gnt_i          (m1_gnt_w),
      .m_wvalid_o       (m1_wvalid_w),
      .m_wdata_o        (m1_wdata_w),
      .m_wready_i       (m1_wready_w),
      .m_rvalid_i       (m1_rvalid_w),
      .m_rdata_i        (m1_rdata_w),
      .m_rready_o       (m1_rready_w),
      .m_done_i         (m1_done_w),
      .m_err_i          (m1_err_w),
      .restore_go_i     (mgr_done_w),
      .restore_busy_o   (d3_busy_w),
      .restore_done_o   (d3_done_w),
      .restore_fail_o   (d3_fail_w),
      .restore_blank_o  (d3_blank_w),
      .rs_applied_o     (d3_rs_applied_o),
      .rs_refused_o     (d3_rs_refused_o),
      .rs_blank_o       (d3_rs_blank_o),
      .rs_reverted_o    (d3_rs_reverted_o),
      .unflushed_o      (d3_unfl_w),
      .alarm_o          (d3_alarm_w),
      .writes_o         (d3_writes_o),
      .dbg_slot_o       (d3_slot_o),
      .dbg_taint_o      (d3_taint_o),
      .dbg_dirty_o      (d3_dirty_o)
  );
`endif
  assign d3_alarm_o        = d3_alarm_w;
  assign d3_mdone_o        = m1_done_w;
  assign d3_unflushed_o    = d3_unfl_w;
  assign d3_restore_done_o = d3_done_w;
  assign d3_restore_fail_o = d3_fail_w;

  // ---- two managers, one port ------------------------------------------------------
  logic        p_req_w, p_we_w, p_wvalid_w, p_rready_w, p_wready_w, p_rvalid_w;
  logic        p_busy_w, p_done_w, p_err_w;
  logic [7:0]  p_rid_w, p_wdata_w, p_rdata_w;

  KL_pp_nvm_mgr_arb u_arb (
      .clk_i       (clk_i),
      .rst_n       (rst_n),
      .m0_req_i    (m0_req_w),
      .m0_we_i     (m0_we_w),
      .m0_rid_i    (m0_rid_w),
      .m0_wvalid_i (m0_wvalid_w),
      .m0_wdata_i  (m0_wdata_w),
      .m0_rready_i (m0_rready_w),
      .m0_wready_o (m0_wready_w),
      .m0_rvalid_o (m0_rvalid_w),
      .m0_rdata_o  (m0_rdata_w),
      .m0_busy_o   (m0_busy_w),
      .m0_done_o   (m0_done_w),
      .m0_err_o    (m0_err_w),
      .m1_req_i    (m1_req_w),
      .m1_we_i     (m1_we_w),
      .m1_rid_i    (m1_rid_w),
      .m1_wvalid_i (m1_wvalid_w),
      .m1_wdata_i  (m1_wdata_w),
      .m1_rready_i (m1_rready_w),
      .m1_gnt_o    (m1_gnt_w),
      .m1_wready_o (m1_wready_w),
      .m1_rvalid_o (m1_rvalid_w),
      .m1_rdata_o  (m1_rdata_w),
      .m1_done_o   (m1_done_w),
      .m1_err_o    (m1_err_w),
      .p_req_o     (p_req_w),
      .p_we_o      (p_we_w),
      .p_rid_o     (p_rid_w),
      .p_wvalid_o  (p_wvalid_w),
      .p_wdata_o   (p_wdata_w),
      .p_rready_o  (p_rready_w),
      .p_wready_i  (p_wready_w),
      .p_rvalid_i  (p_rvalid_w),
      .p_rdata_i   (p_rdata_w),
      .p_busy_i    (p_busy_w),
      .p_done_i    (p_done_w),
      .p_err_i     (p_err_w)
  );

  // ---- the real port: the ONE device-face initiator ------------------------------
  logic        d_req_w, d_wvalid_w, d_rready_w;
  logic [1:0]  d_op_w;
  logic [7:0]  d_region_w, d_wdata_w;
  logic [15:0] d_offset_w, d_len_w;
  logic        b_gnt_w, b_wready_w, b_rvalid_w, b_busy_w, b_done_w, b_err_w;
  logic [7:0]  b_rdata_w;

  KL_pp_nvm_port u_nvm_port (
      .clk_i           (clk_i),
      .rst_n           (rst_n),
      .nvm_req_i       (p_req_w),
      .nvm_we_i        (p_we_w),
      .nvm_record_id_i (p_rid_w),
      .nvm_wvalid_i    (p_wvalid_w),
      .nvm_wready_o    (p_wready_w),
      .nvm_wdata_i     (p_wdata_w),
      .nvm_rvalid_o    (p_rvalid_w),
      .nvm_rready_i    (p_rready_w),
      .nvm_rdata_o     (p_rdata_w),
      .nvm_busy_o      (p_busy_w),
      .nvm_done_o      (p_done_w),
      .nvm_err_o       (p_err_w),
      .dev_req_o       (d_req_w),
      .dev_gnt_i       (b_gnt_w),
      .dev_op_o        (d_op_w),
      .dev_region_o    (d_region_w),
      .dev_offset_o    (d_offset_w),
      .dev_len_o       (d_len_w),
      .dev_wvalid_o    (d_wvalid_w),
      .dev_wready_i    (b_wready_w),
      .dev_wdata_o     (d_wdata_w),
      .dev_rvalid_i    (b_rvalid_w),
      .dev_rdata_i     (b_rdata_w),
      .dev_rready_o    (d_rready_w),
      .dev_busy_i      (b_busy_w),
      .dev_done_i      (b_done_w),
      .dev_err_i       (b_err_w)
  );
  assign port_busy_o  = p_busy_w;
  assign dev_req_o    = d_req_w;
  assign dev_op_o     = d_op_w;
  assign dev_region_o = d_region_w;
  assign dev_gnt_o    = b_gnt_w;
  assign dev_wvalid_o = d_wvalid_w;
  assign dev_wready_o = b_wready_w;
  assign dev_wdata_o  = d_wdata_w;
  assign dev_busy_o   = b_busy_w;
  assign dev_done_o   = b_done_w;
  assign dev_err_o    = b_err_w;

  // ---- the parent glue (KL_pp_shadow, with the D3 change) --------------------------
  //! pend_i: the binding manager's unflushed sinks OR the D3 writer's
  //! unflushed records. The dyn store's sticky level and the sticky class-6/7
  //! mark bit are REPLACED: a writer exists for every group they reported.
  logic pend_w, alarm_w;
`ifdef D3_TRACKED
  //! KL_pp_shadow at dev 07294a76, transcribed: the class-6/7 mark sets a
  //! bit only reset clears, and the dyn store's level is passed straight in
  logic aecp_mark_pend_r;
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      aecp_mark_pend_r <= 1'b0;
    end else if (mk_stb_i && ((mk_mark_i == 8'd6) || (mk_mark_i == 8'd7))) begin
      aecp_mark_pend_r <= 1'b1;
    end
  end
  assign pend_w  = aecp_dyn_dirty_nc_w | (|mgr_dirty_w) | aecp_mark_pend_r;
`else
  assign pend_w  = (|mgr_dirty_w) | d3_unfl_w;
`endif
  assign alarm_w = mgr_alarm_w | d3_alarm_w;
  assign alarm_o = alarm_w;

  //! the processor's restore is BOTH walks: the binding walk, then D3
  logic rs_busy_w, rs_done_w;
  assign rs_busy_w = mgr_busy_w | d3_busy_w;
  assign rs_done_w = mgr_done_w & d3_done_w;

  logic restore_busy_q, walk_blind_r, img_valid_w;
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      restore_busy_q <= 1'b0;
      walk_blind_r   <= 1'b1;
    end else begin
      restore_busy_q <= rs_busy_w;
      if (rs_busy_w && !restore_busy_q)   walk_blind_r <= ~img_valid_w;
      else if (rs_busy_w && !img_valid_w) walk_blind_r <= 1'b1;
    end
  end
  assign restore_busy_o  = rs_busy_w;
  assign restore_done_o  = rs_done_w;
  //! blank: NEITHER walk validated a record, so a restore that put names
  //! back and no binding does not read "nothing restored"
  assign restore_blank_o = mgr_blank_w & d3_blank_w;
  assign restore_fail_o  = mgr_fail_w || d3_fail_w || (rs_done_w && walk_blind_r);

  // ---- the shipping backend ----------------------------------------------------------
  KL_nvm_backend #(
      .CLK_HZ_P       (CLK_HZ_P),
      .N_STREAM_IN_P  (N_STREAM_IN_P),
      .N_STREAM_OUT_P (N_STREAM_OUT_P),
      .N_SPORT_IN_P   (N_SPORT_IN_P),
      .N_SPORT_OUT_P  (N_SPORT_OUT_P),
      .N_AUDIO_UNIT_P (N_AUDIO_UNIT_P),
      .N_CLK_DOM_P    (N_CLK_DOM_P),
      .N_NAME_P       (N_NAME_P),
      .T_HOLD_MS_P    (T_HOLD_MS_P),
      .CAP_ID_W_P     (16)
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
      .pend_i          (pend_w),
      .alarm_i         (alarm_w),
      .nvm_backed_o    (nvm_backed_o),
      .nvm_dirty_o     (nvm_dirty_o),
      .nvm_stale_o     (nvm_stale_o),
      .nvm_verdict_o   (nvm_verdict_o),
      .img_valid_o     (img_valid_w),
      .nvm_pend_o      (nvm_pend_o),
      .nvm_unres_o     (nvm_unres_o)
  );
  assign nvm_img_valid_o = img_valid_w;

endmodule

`default_nettype wire
