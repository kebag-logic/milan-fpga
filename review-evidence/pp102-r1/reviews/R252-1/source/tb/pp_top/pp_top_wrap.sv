/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : pp_top_wrap.sv
//  Project     : IEEE 1722.1 protocol processor — pp_top suite
//
//  Description : End-to-end harness around the REAL protocol_processor_top:
//                nothing but the top's own external contract is exposed —
//                the MAC trunk byte streams, the side-port host face, the
//                SRP service face, the NVM device face, the AECP pop face
//                and the level controls. Time is compressed: 1 ms = 100 clk
//                (DIV_US 2 x DIV_MS 50), which keeps the 89-slot deadline
//                sweep (91 cycles) inside the ms tick while T-ADP-DELAY(-
//                START), T-ADP-ADV, T-ACMP-DELAY, T-MRP-JOIN and the NVM
//                debounce all run for real.
//
//                The one decision that matters: the talker source shape is
//                tied HERE (all 8 sources enabled, stream_id k =
//                {own_mac, k}) because the suite drives SRP declarations
//                through the svc face with its own stream_ids — the tied
//                lanes only feed talker-command flows this suite does not
//                byte-check.
//
//                The one parameter the suite builds twice: SRP_DOM_DEF_VID_P
//                is overridden ONLY when the second build defines
//                PP_TOP_SRP_DOM_DEF_VID (Makefile), so the first build grades
//                the top's own default and never a copy of it.
//---------------------------------------------------------------------------//
`default_nettype none

module pp_top_wrap (
    input  wire         clk_i,
    input  wire         rst_n,

    // identity + model
    input  wire  [63:0] entity_id_i,
    input  wire  [63:0] entity_model_id_i,
    input  wire  [47:0] own_mac_i,
    input  wire  [15:0] talker_sources_i,
    input  wire  [15:0] talker_caps_i,
    input  wire  [15:0] listener_sinks_i,
    input  wire  [15:0] listener_caps_i,
    input  wire  [15:0] current_cfg_i,
    input  wire  [15:0] identify_index_i,

    // level controls + class-D in
    input  wire         entity_enable_i,
    input  wire         link_up_i,
    input  wire         gm_change_i,
    input  wire  [63:0] gm_id_i,
    input  wire  [7:0]  gptp_domain_i,

    // SRP quasi-static
    input  wire         p2p_i,
    input  wire         cfg_rank_i,
    input  wire  [31:0] cfg_acc_lat_ns_i,
    input  wire  [31:0] port_rate_bps_i,
    input  wire  [15:0] cfg_tspec_max_frame_i,

    // MAC trunk RX
    input  wire         rx_valid_i,
    input  wire  [7:0]  rx_data_i,
    input  wire         rx_last_i,

    // MAC TX
    output logic        tx_valid_o,
    output logic        tx_sof_o,
    output logic [7:0]  tx_data_o,
    output logic        tx_eof_o,
    input  wire         tx_ready_i,

    // AECP pop face (kept live: an integrator may still observe/drain it)
    output logic        aecp_txn_valid_o,
    input  wire         aecp_txn_ready_i,

    // GET_COUNTERS read face (06 §6.6) — the C++ harness plays the
    // integrator's counter store behind it, so the counter VALUES this suite
    // checks are the model's and never the DUT's own
    output logic        ctr_req_o,
    output logic [15:0] ctr_desc_type_o,
    output logic [15:0] ctr_desc_index_o,
    output logic  [5:0] ctr_word_o,
    input  wire  [31:0] ctr_data_i,
    input  wire         ctr_wait_i,
    input  wire         ctr_change_i,
    input  wire  [15:0] ctr_change_desc_type_i,
    input  wire  [15:0] ctr_change_desc_index_i,

    // GET_AUDIO_MAP read face (06 §6.5) - same bargain: the harness plays
    // the integrator's dynamic-mapping store, so every geometry word and
    // every record this suite checks on the wire is the model's
    output logic        amap_req_o,
    output logic [15:0] amap_desc_type_o,
    output logic [15:0] amap_desc_index_o,
    output logic [15:0] amap_map_index_o,
    output logic  [1:0] amap_sel_o,
    output logic  [7:0] amap_rec_o,
    input  wire  [63:0] amap_data_i,
    input  wire         amap_wait_i,

    // ADD/REMOVE_AUDIO_MAPPINGS transaction face
    output logic        amap_edit_req_o,
    output logic  [2:0] amap_edit_phase_o,
    output logic        amap_edit_remove_o,
    output logic [15:0] amap_edit_desc_type_o,
    output logic [15:0] amap_edit_desc_index_o,
    output logic [15:0] amap_edit_count_o,
    output logic  [7:0] amap_edit_rec_o,
    output logic [63:0] amap_edit_record_o,
    output logic [63:0] amap_edit_value_o,
    input  wire  [63:0] amap_edit_data_i,
    input  wire         amap_edit_wait_i,

    // Milan-info gather face (06 SS6.2/SS6.10) - the harness is the integrator
    output logic        gsi_req_o,
    output logic [1:0]  gsi_kind_o,
    output logic [15:0] gsi_desc_type_o,
    output logic [15:0] gsi_desc_index_o,
    output logic  [3:0] gsi_sel_o,
    output logic  [7:0] gsi_ord_o,
    //! the proposed format under a SET_STREAM_FORMAT: the harness integrator
    //! model reads it to answer the kind-0 selector-15 verdict
    output logic [63:0] gsi_prop_fmt_o,
    input  wire  [63:0] gsi_data_i,
    input  wire         gsi_wait_i,
    input  wire         gsi_avb_chg_i,
    input  wire         gsi_asp_chg_i,

    // descriptor-image memory master (07 §3.3) — the C++ harness plays a
    // latency-injecting DRAM behind it
    output logic        desc_mem_req_valid_o,
    input  wire         desc_mem_req_ready_i,
    output logic [31:0] desc_mem_req_addr_o,
    output logic  [8:0] desc_mem_req_beats_o,
    input  wire         desc_mem_rsp_valid_i,
    output logic        desc_mem_rsp_ready_o,
    input  wire  [63:0] desc_mem_rsp_data_i,
    input  wire         desc_mem_rsp_last_i,
    input  wire         desc_mem_rsp_err_i,

    // AECP response-buffer memory master (03 §7, read/write)
    output logic        resp_mem_req_valid_o,
    input  wire         resp_mem_req_ready_i,
    output logic [31:0] resp_mem_req_addr_o,
    output logic  [8:0] resp_mem_req_beats_o,
    input  wire         resp_mem_rsp_valid_i,
    output logic        resp_mem_rsp_ready_o,
    input  wire  [63:0] resp_mem_rsp_data_i,
    input  wire         resp_mem_rsp_last_i,
    input  wire         resp_mem_rsp_err_i,
    output logic        resp_mem_wr_valid_o,
    input  wire         resp_mem_wr_ready_i,
    output logic [31:0] resp_mem_wr_addr_o,
    output logic [63:0] resp_mem_wr_data_o,
    output logic  [7:0] resp_mem_wr_strb_o,
    input  wire         resp_mem_wr_done_i,
    input  wire         resp_mem_wr_err_i,

    // NVM restore + device face
    input  wire         restore_go_i,
    output logic        restore_busy_o,
    output logic        restore_done_o,
    output logic        restore_fail_o,
    output logic        restore_blank_o,
    output logic        nvm_alarm_o,
    output logic  [7:0] nvm_unflushed_o,
    output logic        nvm_dev_req_o,
    input  wire         nvm_dev_gnt_i,
    output logic [1:0]  nvm_dev_op_o,
    output logic [7:0]  nvm_dev_region_o,
    output logic [15:0] nvm_dev_offset_o,
    output logic [15:0] nvm_dev_len_o,
    output logic        nvm_dev_wvalid_o,
    input  wire         nvm_dev_wready_i,
    output logic [7:0]  nvm_dev_wdata_o,
    input  wire         nvm_dev_rvalid_i,
    input  wire  [7:0]  nvm_dev_rdata_i,
    output logic        nvm_dev_rready_o,
    input  wire         nvm_dev_busy_i,
    input  wire         nvm_dev_done_i,
    input  wire         nvm_dev_err_i,

    // side-port host face
    input  wire         host_req_valid_i,
    input  wire         host_we_i,
    input  wire  [19:0] host_addr_i,
    input  wire  [31:0] host_wdata_i,
    output logic [31:0] host_rdata_o,
    output logic        host_rvalid_o,
    output logic        host_err_o,

    // SRP service face
    input  wire         svc_valid_i,
    output logic        svc_ready_o,
    input  wire  [2:0]  svc_op_i,
    input  wire  [7:0]  svc_index_i,
    input  wire  [63:0] svc_stream_id_i,
    input  wire  [47:0] svc_da_i,
    input  wire  [11:0] svc_vid_i,
    input  wire  [15:0] svc_max_frame_i,
    input  wire  [1:0]  svc_lstn_state_i,
    output logic        svc_rsp_valid_o,
    output logic [1:0]  svc_rsp_status_o,
    output logic [31:0] svc_rsp_data_o,

    // maap face (02 §4.2): with cfg_maap_internal_i = 0 the C++ harness
    // plays the allocator, INCLUDING the "no allocator at all" wiring; with
    // 1 the internal KL_pp_maap engine answers and this group is quiesced
    output logic        maap_req_valid_o,
    input  wire         maap_req_ready_i,
    output logic        maap_req_release_o,
    output logic [2:0]  maap_req_src_o,
    input  wire         maap_rsp_valid_i,
    input  wire         maap_rsp_ok_i,
    input  wire  [47:0] maap_rsp_da_i,
    input  wire         maap_conflict_valid_i,
    input  wire  [2:0]  maap_conflict_src_i,
    output logic        maap_conflict_ack_o,

    // internal MAAP engine (11): quasi-static config + the published claim
    input  wire         cfg_maap_internal_i,
    input  wire  [7:0]  cfg_maap_count_i,
    input  wire  [15:0] cfg_maap_seed_offset_i,
    input  wire         cfg_maap_seed_valid_i,
    output logic [47:0] maap_addr_o,
    output logic        maap_addr_valid_o,
    output logic [1:0]  maap_state_o,
    output logic [7:0]  maap_conflicts_o,
    output logic [7:0]  maap_defends_o,

    // the per-source DA gate a fabric ANDs with its own stream enable
    output logic [7:0]  acmp_declaring_o,

    // the Class A Domain in force (class-D, F02.10), passed through by name:
    // these ports are where an integrator reads P-SRP-DOM-DEF-VID's effect
    output logic  [2:0] srp_class_a_prio_o,
    output logic [11:0] srp_class_a_vid_o,
    output logic        srp_domain_adopted_o,
    output logic        srp_domain_change_o,

    // observability
    output logic [31:0] dbg_now_ms_o,
    // suite taps (cross-module refs into the DUT; observe-only)
    output logic        dbg_acmp_valid_o,
    output logic [3:0]  dbg_acmp_msg_o,
    output logic        dbg_is_tkr_o,
    output logic        dbg_lstn_pop_o,
    output logic        dbg_lstn_busy_o,
    output logic        dbg_evr_valid_o,
    output logic [4:0]  dbg_evr_src_o,
    output logic        dbg_evr_ack_o,
    //! the STREAM_IS_RUNNING predicate, OBSERVED not driven: the bind and the
    //! SRP declaration are made the real way (an ACMP BIND_RX and a talker
    //! declaration), and these two only let the bench prove the cause took
    //! effect before it grades the refusal. Forcing them would test the
    //! dispatch arm against a fiction.
    output logic        dbg_bound0_o,
    output logic        dbg_streaming0_o,
    output logic        dbg_trc_wr_o,
    output logic        dbg_adp_evt_o,
    output logic        dbg_evt_tk_v_o,
    output logic        dbg_evt_tk_rdy_o,
    output logic        dbg_img_valid_o,
    output logic  [3:0] dbg_img_fault_o,
    output logic [15:0] dbg_aecp_cmd_o,
    output logic [15:0] dbg_aecp_resp_o,
    output logic [15:0] dbg_aecp_drop_o,
    output logic  [2:0] dbg_resp_fault_o,
    output logic [15:0] dbg_resp_err_o,
    output logic [15:0] dbg_resp_lane_o,
    output logic  [2:0] dbg_ca_state_o,
    output logic        dbg_ca_cancel_o,
    output logic        dbg_txc_locked_o,
    output logic  [2:0] dbg_txs_free_o,
    output logic  [3:0] dbg_org_busy_o,
    output logic  [3:0] dbg_org_queue_o,
    output logic  [3:0] dbg_org_second_owner_o,
    output logic        dbg_txs_release_valid_o,
    //! the per-sink started/stopped view the FABRIC admission gate reads
    //! (Milan 5.3.8.7). It is exposed because a START/STOP_STREAMING that
    //! answers SUCCESS without moving this bit is the exact defect the
    //! command's response shape cannot show.
    output logic  [7:0] aecp_strm_started_o,
    //! the per-row settings faces, exposed for the same reason: a
    //! SET_STREAM_FORMAT / SET_STREAM_INFO that answers SUCCESS without
    //! moving its row (or raising its valid bit) is invisible to any
    //! response-shape check
    output logic [8*32-1:0] aecp_pt_offset_o,
    output logic  [7:0] aecp_pt_offset_v_o,
    output logic [8*64-1:0] aecp_fmt_in_o,
    output logic  [7:0] aecp_fmt_in_v_o,
    output logic [8*64-1:0] aecp_fmt_out_o,
    output logic  [7:0] aecp_fmt_out_v_o,
    //! the SET_CLOCK_SOURCE refusal contract (06 section 6.4: nothing
    //! stored, marked or notified) has no wire shape: a write of the value
    //! the row already holds, an NVM mark and a notification enqueue all
    //! leave the response and GET as they were. These three observe the
    //! effects themselves: the dynamic store's accepted-write counter, the
    //! OP_NVM_MARK strobe and the OP_NOTIFY_ENQ strobe (06 section 8). The
    //! mark strobe and its code are TOP-LEVEL PORTS now (issue #90), so they
    //! are passed through by name and not peeked at inside the DUT.
    output logic [15:0] dbg_dyn_writes_o,
    output logic        aecp_nvm_stb_o,
    output logic  [7:0] aecp_nvm_mark_o,
    output logic        dbg_notify_enq_o
);

  // 1 ms = 2 x 50 = 100 clk; the 91-slot sweep (93 cycles) fits inside
  localparam int unsigned TB_DIV_US_C = 2;
  localparam int unsigned TB_DIV_MS_C = 50;

  // talker source shape (see banner)
  logic [7:0]       cfg_src_en_w;
  logic [15:0]      cfg_src_iface_w;
  logic [8*64-1:0]  cfg_stream_id_w;

  assign cfg_src_en_w    = 8'hFF;
  assign cfg_src_iface_w = 16'd0;
  for (genvar g = 0; g < 8; g++) begin : g_sid
    assign cfg_stream_id_w[g*64 +: 64] = {own_mac_i, 16'(g)};
  end

  // AECP pop face: record lane observed, payload faces DEFINED-idle
  logic [pp_pkg::PP_TXN_W_C-1:0] aecp_txn_nc_w;
  logic [7:0]                    aecp_rd_data_nc_w;
  logic [9:0]                    aecp_slot_len_nc_w;
  logic                          aecp_lock_held_nc_w;

  protocol_processor_top #(
`ifdef PP_TOP_SRP_DOM_DEF_VID
      //! the second build's verification-only fixture (see the banner)
      .SRP_DOM_DEF_VID_P (`PP_TOP_SRP_DOM_DEF_VID),
`endif
      .TIM_DIV_US_P (TB_DIV_US_C),
      .TIM_DIV_MS_P (TB_DIV_MS_C),
      //! TIM compression for the registration/lock deadlines, same reason
      //! as the DIV overrides: the suite must SEE IEEE 7.4.37.2's 300 s
      //! TIME_LIMITED expiry and 7.4.2's 60 s lock expiry, not wait 30
      //! million compressed cycles for them
      .REG_TL_TIMEOUT_MS_P (400),
      .LOCK_TIMEOUT_MS_P   (400),
      .TROM_HEX_P   ("ltn_rom.hex"),
      .UCODE_HEX_P  ("ucode.hex")
  ) u_dut (
      .clk_i                 (clk_i),
      .rst_n                 (rst_n),
      .entity_id_i           (entity_id_i),
      .entity_model_id_i     (entity_model_id_i),
      .own_mac_i             (own_mac_i),
      .talker_sources_i      (talker_sources_i),
      .talker_caps_i         (talker_caps_i),
      .listener_sinks_i      (listener_sinks_i),
      .listener_caps_i       (listener_caps_i),
      .current_cfg_i         (current_cfg_i),
      .identify_index_i      (identify_index_i),
      .entity_enable_i       (entity_enable_i),
      .link_up_i             (link_up_i),
      .gm_change_i           (gm_change_i),
      .gm_id_i               (gm_id_i),
      .gptp_domain_i         (gptp_domain_i),
      .p2p_i                 (p2p_i),
      .cfg_rank_i            (cfg_rank_i),
      .cfg_acc_lat_ns_i      (cfg_acc_lat_ns_i),
      .port_rate_bps_i       (port_rate_bps_i),
      .cfg_tspec_max_frame_i (cfg_tspec_max_frame_i),
      .cfg_src_en_i          (cfg_src_en_w),
      .cfg_src_iface_i       (cfg_src_iface_w),
      .cfg_stream_id_i       (cfg_stream_id_w),
      .rx_valid_i            (rx_valid_i),
      .rx_data_i             (rx_data_i),
      .rx_last_i             (rx_last_i),
      .tx_valid_o            (tx_valid_o),
      .tx_sof_o              (tx_sof_o),
      .tx_data_o             (tx_data_o),
      .tx_eof_o              (tx_eof_o),
      .tx_ready_i            (tx_ready_i),
      .aecp_txn_valid_o      (aecp_txn_valid_o),
      .aecp_txn_o            (aecp_txn_nc_w),
      .aecp_txn_ready_i      (aecp_txn_ready_i),
      .aecp_rxs_rd_slot_i    (2'd0),
      .aecp_rxs_rd_addr_i    (10'd0),
      .aecp_rxs_rd_en_i      (1'b0),
      .aecp_rxs_rd_data_o    (aecp_rd_data_nc_w),
      .aecp_rxs_slot_len_o   (aecp_slot_len_nc_w),
      .aecp_rxs_free_i       (1'b0),
      .aecp_rxs_free_slot_i  (2'd0),
      //! Dynamic state is verified through AECP response traffic here. Keep
      //! every unused publication explicit so newly added state cannot leave
      //! a silent harness integration gap.
      .aecp_cur_config_o     (),
      .aecp_identify_o       (),
      .aecp_clk_src_index_o  (),
      .aecp_strm_started_o   (aecp_strm_started_o),
      .aecp_pt_offset_o      (aecp_pt_offset_o),
      .aecp_pt_offset_v_o    (aecp_pt_offset_v_o),
      .aecp_fmt_in_o         (aecp_fmt_in_o),
      .aecp_fmt_in_v_o       (aecp_fmt_in_v_o),
      .aecp_fmt_out_o        (aecp_fmt_out_o),
      .aecp_fmt_out_v_o      (aecp_fmt_out_v_o),
      .aecp_dyn_dirty_o      (),
      .aecp_nvm_stb_o        (aecp_nvm_stb_o),
      .aecp_nvm_mark_o       (aecp_nvm_mark_o),
      .aecp_lock_held_o      (aecp_lock_held_nc_w),
      .ctr_req_o             (ctr_req_o),
      .ctr_desc_type_o       (ctr_desc_type_o),
      .ctr_desc_index_o      (ctr_desc_index_o),
      .ctr_word_o            (ctr_word_o),
      .ctr_data_i            (ctr_data_i),
      .ctr_wait_i            (ctr_wait_i),
      .ctr_change_i          (ctr_change_i),
      .ctr_change_desc_type_i(ctr_change_desc_type_i),
      .ctr_change_desc_index_i(ctr_change_desc_index_i),
      .amap_req_o            (amap_req_o),
      .amap_desc_type_o      (amap_desc_type_o),
      .amap_desc_index_o     (amap_desc_index_o),
      .amap_map_index_o      (amap_map_index_o),
      .amap_sel_o            (amap_sel_o),
      .amap_rec_o            (amap_rec_o),
      .amap_data_i           (amap_data_i),
      .amap_wait_i           (amap_wait_i),
      .amap_edit_req_o       (amap_edit_req_o),
      .amap_edit_phase_o     (amap_edit_phase_o),
      .amap_edit_remove_o    (amap_edit_remove_o),
      .amap_edit_desc_type_o (amap_edit_desc_type_o),
      .amap_edit_desc_index_o(amap_edit_desc_index_o),
      .amap_edit_count_o     (amap_edit_count_o),
      .amap_edit_rec_o       (amap_edit_rec_o),
      .amap_edit_record_o    (amap_edit_record_o),
      .amap_edit_value_o     (amap_edit_value_o),
      .amap_edit_data_i      (amap_edit_data_i),
      .amap_edit_wait_i      (amap_edit_wait_i),
      .gsi_req_o             (gsi_req_o),
      .gsi_kind_o            (gsi_kind_o),
      .gsi_desc_type_o       (gsi_desc_type_o),
      .gsi_desc_index_o      (gsi_desc_index_o),
      .gsi_sel_o             (gsi_sel_o),
      .gsi_ord_o             (gsi_ord_o),
      .gsi_prop_fmt_o        (gsi_prop_fmt_o),
      .gsi_data_i            (gsi_data_i),
      .gsi_wait_i            (gsi_wait_i),
      .gsi_avb_chg_i         (gsi_avb_chg_i),
      .gsi_asp_chg_i         (gsi_asp_chg_i),
      .desc_mem_req_valid_o  (desc_mem_req_valid_o),
      .desc_mem_req_ready_i  (desc_mem_req_ready_i),
      .desc_mem_req_addr_o   (desc_mem_req_addr_o),
      .desc_mem_req_beats_o  (desc_mem_req_beats_o),
      .desc_mem_rsp_valid_i  (desc_mem_rsp_valid_i),
      .desc_mem_rsp_ready_o  (desc_mem_rsp_ready_o),
      .desc_mem_rsp_data_i   (desc_mem_rsp_data_i),
      .desc_mem_rsp_last_i   (desc_mem_rsp_last_i),
      .desc_mem_rsp_err_i    (desc_mem_rsp_err_i),
      .resp_mem_req_valid_o  (resp_mem_req_valid_o),
      .resp_mem_req_ready_i  (resp_mem_req_ready_i),
      .resp_mem_req_addr_o   (resp_mem_req_addr_o),
      .resp_mem_req_beats_o  (resp_mem_req_beats_o),
      .resp_mem_rsp_valid_i  (resp_mem_rsp_valid_i),
      .resp_mem_rsp_ready_o  (resp_mem_rsp_ready_o),
      .resp_mem_rsp_data_i   (resp_mem_rsp_data_i),
      .resp_mem_rsp_last_i   (resp_mem_rsp_last_i),
      .resp_mem_rsp_err_i    (resp_mem_rsp_err_i),
      .resp_mem_wr_valid_o   (resp_mem_wr_valid_o),
      .resp_mem_wr_ready_i   (resp_mem_wr_ready_i),
      .resp_mem_wr_addr_o    (resp_mem_wr_addr_o),
      .resp_mem_wr_data_o    (resp_mem_wr_data_o),
      .resp_mem_wr_strb_o    (resp_mem_wr_strb_o),
      .resp_mem_wr_done_i    (resp_mem_wr_done_i),
      .resp_mem_wr_err_i     (resp_mem_wr_err_i),
      .restore_go_i          (restore_go_i),
      .restore_busy_o        (restore_busy_o),
      .restore_done_o        (restore_done_o),
      .restore_fail_o        (restore_fail_o),
      .restore_blank_o       (restore_blank_o),
      .nvm_alarm_o           (nvm_alarm_o),
      .nvm_unflushed_o       (nvm_unflushed_o),
      .nvm_dev_req_o         (nvm_dev_req_o),
      .nvm_dev_gnt_i         (nvm_dev_gnt_i),
      .nvm_dev_op_o          (nvm_dev_op_o),
      .nvm_dev_region_o      (nvm_dev_region_o),
      .nvm_dev_offset_o      (nvm_dev_offset_o),
      .nvm_dev_len_o         (nvm_dev_len_o),
      .nvm_dev_wvalid_o      (nvm_dev_wvalid_o),
      .nvm_dev_wready_i      (nvm_dev_wready_i),
      .nvm_dev_wdata_o       (nvm_dev_wdata_o),
      .nvm_dev_rvalid_i      (nvm_dev_rvalid_i),
      .nvm_dev_rdata_i       (nvm_dev_rdata_i),
      .nvm_dev_rready_o      (nvm_dev_rready_o),
      .nvm_dev_busy_i        (nvm_dev_busy_i),
      .nvm_dev_done_i        (nvm_dev_done_i),
      .nvm_dev_err_i         (nvm_dev_err_i),
      .host_req_valid_i      (host_req_valid_i),
      .host_we_i             (host_we_i),
      .host_addr_i           (host_addr_i),
      .host_wdata_i          (host_wdata_i),
      .host_rdata_o          (host_rdata_o),
      .host_rvalid_o         (host_rvalid_o),
      .host_err_o            (host_err_o),
      .svc_valid_i           (svc_valid_i),
      .svc_ready_o           (svc_ready_o),
      .svc_op_i              (svc_op_i),
      .svc_index_i           (svc_index_i),
      .svc_stream_id_i       (svc_stream_id_i),
      .svc_da_i              (svc_da_i),
      .svc_vid_i             (svc_vid_i),
      .svc_max_frame_i       (svc_max_frame_i),
      .svc_lstn_state_i      (svc_lstn_state_i),
      .svc_rsp_valid_o       (svc_rsp_valid_o),
      .svc_rsp_status_o      (svc_rsp_status_o),
      .svc_rsp_data_o        (svc_rsp_data_o),
      .maap_req_valid_o      (maap_req_valid_o),
      .maap_req_ready_i      (maap_req_ready_i),
      .maap_req_release_o    (maap_req_release_o),
      .maap_req_src_o        (maap_req_src_o),
      .maap_rsp_valid_i      (maap_rsp_valid_i),
      .maap_rsp_ok_i         (maap_rsp_ok_i),
      .maap_rsp_da_i         (maap_rsp_da_i),
      .maap_conflict_valid_i (maap_conflict_valid_i),
      .maap_conflict_src_i   (maap_conflict_src_i),
      .maap_conflict_ack_o   (maap_conflict_ack_o),
      .cfg_maap_internal_i   (cfg_maap_internal_i),
      .cfg_maap_count_i      (cfg_maap_count_i),
      .cfg_maap_seed_offset_i (cfg_maap_seed_offset_i),
      .cfg_maap_seed_valid_i (cfg_maap_seed_valid_i),
      .maap_addr_o           (maap_addr_o),
      .maap_addr_valid_o     (maap_addr_valid_o),
      .maap_state_o          (maap_state_o),
      .maap_conflicts_o      (maap_conflicts_o),
      .maap_defends_o        (maap_defends_o),
      .acmp_declaring_o      (acmp_declaring_o),
      .srp_class_a_prio_o    (srp_class_a_prio_o),
      .srp_class_a_vid_o     (srp_class_a_vid_o),
      .srp_domain_adopted_o  (srp_domain_adopted_o),
      .srp_domain_change_o   (srp_domain_change_o),
      .dbg_now_ms_o          (dbg_now_ms_o)
  );

  assign dbg_acmp_valid_o = u_dut.acmp_txn_valid_w;
  assign dbg_acmp_msg_o   = u_dut.acmp_head_w.msg_type;
  assign dbg_is_tkr_o     = u_dut.acmp_is_tkr_w;
  assign dbg_lstn_pop_o   = u_dut.lstn_txn_ready_w;
  assign dbg_lstn_busy_o  = u_dut.lstn_dbg_busy_nc_w;
  assign dbg_evr_valid_o  = u_dut.evr_valid_w;
  assign dbg_evr_src_o    = u_dut.evr_src_w;
  assign dbg_evr_ack_o    = u_dut.evr_ack_w;
  assign dbg_bound0_o     = u_dut.bound_hold_r[0];
  assign dbg_streaming0_o = u_dut.aecp_streaming_w[0];
  assign dbg_trc_wr_o     = u_dut.trc_wr_valid_w;
  assign dbg_adp_evt_o    = u_dut.adp_evt_valid_w;
  assign dbg_evt_tk_v_o   = u_dut.lstn_evt_tk_valid_w;
  assign dbg_evt_tk_rdy_o = u_dut.lstn_evt_tk_ready_w;
  assign dbg_img_valid_o  = u_dut.aecp_dbg_img_valid_w;
  assign dbg_img_fault_o  = u_dut.aecp_dbg_fault_w;
  assign dbg_aecp_cmd_o   = u_dut.aecp_dbg_cmd_w;
  assign dbg_aecp_resp_o  = u_dut.aecp_dbg_resp_w;
  assign dbg_aecp_drop_o  = u_dut.aecp_dbg_drop_w;
  assign dbg_resp_fault_o = u_dut.aecp_dbg_rfault_w;
  assign dbg_resp_err_o   = u_dut.aecp_dbg_rerr_w;
  assign dbg_resp_lane_o  = u_dut.aecp_dbg_rlane_w;
  assign dbg_ca_state_o   = u_dut.u_ca_builder.c_st_r;
  assign dbg_ca_cancel_o  = u_dut.ntfy_ca_cancel_valid_w;
  assign dbg_txc_locked_o = u_dut.txc_locked_r;
  assign dbg_txs_free_o   = u_dut.txs_free_w;
  assign dbg_org_busy_o   = u_dut.org_busy_nc_w;
  assign dbg_org_queue_o  = u_dut.laneq_org_cnt_r;
  assign dbg_txs_release_valid_o = u_dut.txs_release_valid_w;
  assign dbg_dyn_writes_o = u_dut.u_aecp.dyn_writes_nc_w;
  assign dbg_notify_enq_o = u_dut.aecp_eff_notify_stb_nc_w;
  always_comb begin : second_originator_owner
    dbg_org_second_owner_o = 4'hF;
    if (u_dut.laneq_org_cnt_r > 4'd1) begin
      for (int unsigned i = 0; i < 16; i++) begin
        if (u_dut.u_originator.valid_r[i]
            && (u_dut.u_originator.txs_r[i] == u_dut.laneq_org_r[1])) begin
          dbg_org_second_owner_o = u_dut.u_originator.owner_r[i];
        end
      end
    end
  end

endmodule : pp_top_wrap
`default_nettype wire
