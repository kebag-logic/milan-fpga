/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : aempatch_wrap.sv   (TB ONLY — not shipped RTL)
//  Project     : Milan saved-state fast-connect — E4 AEM ingest port
//
//  Description : Harness top for the AEM dynamic-state patch port. It does
//                two jobs and no others:
//
//                1. THE CSR DECODE BELOW IS THE EXECUTABLE SPEC of the
//                   0x7C8-0x7D4 group documented in
//                   docs/design/SAVED_STATE_FASTCONNECT.md §10c and
//                   docs/reference/REGISTER_MAP.md. milan_csr must reproduce
//                   exactly this behaviour — same addresses, same one-cycle
//                   strobes, same read-back — the way
//                   tb/verilator/persist/persist_wrap.sv does for the 0x7B8
//                   journal group and tb/verilator/tcam_csr does for 0x700.
//
//                2. It ties off the ~90 identity / counter / listener-state
//                   ports of KL_aecp_top that this suite does not exercise,
//                   so sim_main.cpp only has to think about the three things
//                   under test: the CSR plane, the ADP enable, and the AECP
//                   frame path the restored value must be READABLE through.
//
//                enable_i is exported UNCHANGED and deliberately: in the real
//                datapath it is cfg_adp_enable (0x600[0]), so this one wire
//                is simultaneously "the entity is advertising" and "the patch
//                port is closed". The suite drives it directly because that
//                coupling IS the property being tested.
//
//  Spec refs   : Milan v1.2 §5.3.5.1 / 5.3.7.1 / 5.3.8.1 / 5.3.11.1
//  Company     : Kebag Logic
//---------------------------------------------------------------------------//

`default_nettype none

module aempatch_wrap (
    input  wire         clk_i,
    input  wire         rst_n,

    //! cfg_adp_enable (0x600[0]): HIGH = advertising = patch port CLOSED
    input  wire         enable_i,

    //! identity the AECP engine answers as
    input  wire [47:0]  station_mac_i,
    input  wire [63:0]  entity_id_i,

    // ---- CSR plane (one-cycle write strobe, combinational read) --------
    input  wire [31:0]  wr_addr_i,
    input  wire [31:0]  wr_data_i,
    input  wire         wr_p_i,
    input  wire [31:0]  rd_addr_i,
    output logic [31:0] rd_data_o,

    // ---- MAC RX tap (AECP commands in) ---------------------------------
    input  wire         rx_tvalid_i,
    input  wire [63:0]  rx_tdata_i,
    input  wire [7:0]   rx_tkeep_i,
    input  wire         rx_tlast_i,

    // ---- response AXIS (AECP responses out) ----------------------------
    output wire [63:0]  m_axis_tdata,
    output wire [7:0]   m_axis_tkeep,
    output wire         m_axis_tvalid,
    output wire         m_axis_tlast,
    input  wire         m_axis_tready,

    //! probe: the live clock_source_index shadow, so the suite can SAY that
    //! a store patch does NOT move the fabric's clock selector (see the
    //! honesty note in sim_main.cpp phase [P7])
    output wire [15:0]  clk_src_o
);

  // ---- the group under spec ------------------------------------------
  localparam [31:0] A_AEMP_SEL_C   = 32'h7C8;  //! W: {desc_type, index}
  localparam [31:0] A_AEMP_FIELD_C = 32'h7CC;  //! W: [2:0] field code
  localparam [31:0] A_AEMP_DATA_C  = 32'h7D0;  //! W: payload word, MSW first
  localparam [31:0] A_AEMP_CTRL_C  = 32'h7D4;  //! W1S: [0] commit [1] abort; R: status

  logic [31:0] pat_wdata_r;
  logic        pat_sel_p_r, pat_field_p_r, pat_data_p_r;
  logic        pat_commit_p_r, pat_abort_p_r;
  wire  [31:0] pat_stat_w;

  //! one-cycle command strobes, exactly as milan_csr's write decode makes
  //! them: default low every cycle, raised only by the address that owns
  //! them. pat_wdata_r deliberately HOLDS (it is data, not a command).
  always_ff @(posedge clk_i) begin : csr_decode
    if (!rst_n) begin
      pat_wdata_r    <= 32'h0;
      pat_sel_p_r    <= 1'b0;
      pat_field_p_r  <= 1'b0;
      pat_data_p_r   <= 1'b0;
      pat_commit_p_r <= 1'b0;
      pat_abort_p_r  <= 1'b0;
    end else begin
      pat_sel_p_r    <= 1'b0;
      pat_field_p_r  <= 1'b0;
      pat_data_p_r   <= 1'b0;
      pat_commit_p_r <= 1'b0;
      pat_abort_p_r  <= 1'b0;
      if (wr_p_i) begin
        pat_wdata_r <= wr_data_i;
        unique case (wr_addr_i)
          A_AEMP_SEL_C:   pat_sel_p_r   <= 1'b1;
          A_AEMP_FIELD_C: pat_field_p_r <= 1'b1;
          A_AEMP_DATA_C:  pat_data_p_r  <= 1'b1;
          A_AEMP_CTRL_C: begin
            pat_commit_p_r <= wr_data_i[0];
            pat_abort_p_r  <= wr_data_i[1];
          end
          default: ;
        endcase
      end
    end
  end : csr_decode

  //! SEL/FIELD/DATA are write-only and read 0 (nothing to read back — the
  //! engine's whole observable state is the status word); CTRL reads it.
  always_comb begin : csr_read
    unique case (rd_addr_i)
      A_AEMP_CTRL_C: rd_data_o = pat_stat_w;
      default:       rd_data_o = 32'h0;
    endcase
  end : csr_read

  // ---- DUT: the shipping AECP top, unmodified -------------------------
  KL_aecp_top #(.CLK_FREQ_HZ_P(100_000_000)) u_dut (
    .clk_i(clk_i), .rst_n(rst_n), .enable_i(enable_i),
    .station_mac_i(station_mac_i), .entity_id_i(entity_id_i),
    .entity_model_id_i(64'd0), .entity_name8_i(64'd0),
    .entity_caps_i(32'h0000_8588),
    .talker_sources_i(16'd8), .talker_caps_i(16'h4801),
    .listener_sinks_i(16'd8), .listener_caps_i(16'h4801),
    .controller_caps_i(32'd0), .available_index_i(32'd7),
    .association_id_i(64'd0), .gptp_gm_id_i(64'd0),
    .pdelay_ns_i(32'd0), .gptp_domain_i(8'd0),
    .aaf_dmac_i(48'd0), .aaf_vid_i(12'd2),
    .talker_active_i(1'b0), .listener_observed_i(1'b0),
    .pres_offset_o(), .identify_o(),
    .dmap_l_ch_o(), .dmap_l_en_o(), .dmap_r_ch_o(), .dmap_r_en_o(),
    .dmap_wr_p_o(), .dmap_wr_addr_o(), .dmap_wr_word_o(),
    .odmap_wr_p_o(), .odmap_wr_slot_o(), .odmap_wr_word_o(),
    .link_up_i(1'b1),
    .gs_diag_idx_o(), .rxdiag_cnt_i('0), .tkdiag_cnt_i('0),
    .tkdiag_dirty_p_i(16'd0), .rxdiag_dirty_p_i(16'd0),
    .crf_cnt_dirty_p_i(1'b0), .n_aaf_sinks_i(16'd8),
    .crf_cnt_locked_i(32'd0), .crf_cnt_unlocked_i(32'd0),
    .crf_cnt_intr_i(32'd0), .crf_cnt_seqerr_i(32'd0),
    .crf_cnt_mreset_i(32'd0), .crf_cnt_tu_i(32'd0),
    .crf_cnt_fmterr_i(32'd0), .crf_cnt_late_i(32'd0),
    .crf_cnt_early_i(32'd0), .crf_cnt_pdu_i(32'd0),
    .lstn_bound_i(1'b0), .lstn_sid_i(64'd0), .lstn_dmac_i(48'd0),
    .lstn1_bound_i(1'b0), .lstn1_sid_i(64'd0), .lstn1_dmac_i(48'd0),
    .bdbg0_o(), .bdbg1_o(), .bdbg2_o(),
    .lstn_vlan_i(12'd0), .lstn_pbsta_i(2'd0), .lstn_acmpsta_i(5'd0),
    .lstn_ta_reg_i(1'b0), .lstn_ta_fail_i(1'b0),
    .as_parent_ckid_i(64'd0),
    .lstn_fail_code_i(8'd0), .lstn_fail_bridge_i(64'd0),
    .lstn_ta_vlan_i(12'd0), .lstn_ta_acclat_i(32'd0),
    .tk_fail_valid_i(1'b0), .tk_fail_code_i(8'd0), .tk_fail_bridge_i(64'd0),
    .srp_domain_vid_i(12'd2),
    .in0_cnt_locked_i(32'd0), .in0_cnt_unlocked_i(32'd0),
    .in0_fmt_o(), .clk_src_o(clk_src_o),
    //! TB fixture: no DMA model here, so the tapped lane is always ready
    //! (gh #65 - the tap qualifies its sample on tvalid && tready)
    .rx_tvalid_i(rx_tvalid_i), .rx_tready_i(1'b1), .rx_tdata_i(rx_tdata_i),
    .rx_tkeep_i(rx_tkeep_i), .rx_tlast_i(rx_tlast_i),
    .adp_discover_o(), .adp_disc_seen_o(),
    .m_axis_tdata(m_axis_tdata), .m_axis_tkeep(m_axis_tkeep),
    .m_axis_tvalid(m_axis_tvalid), .m_axis_tlast(m_axis_tlast),
    .m_axis_tready(m_axis_tready),
    .pat_wdata_i(pat_wdata_r),
    .pat_sel_p_i(pat_sel_p_r), .pat_field_p_i(pat_field_p_r),
    .pat_data_p_i(pat_data_p_r), .pat_commit_p_i(pat_commit_p_r),
    .pat_abort_p_i(pat_abort_p_r),
    .pat_stat_o(pat_stat_w),
    .locked_o(), .current_config_o(), .cmd_count_o(), .resp_count_o(),
    //! gh #59 departing-controller tallies: this suite registers no
    //! controllers, so the word stays 0 and nothing here reads it
    .ca_diag_o()
  );

endmodule

`default_nettype wire
