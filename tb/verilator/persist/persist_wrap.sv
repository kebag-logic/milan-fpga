/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : persist_wrap.sv  (testbench harness, not shipped RTL)
//  Project     : Milan saved-state fast-connect
//
//  Description : Integration slice for the persistence journal replay path:
//
//                  CSR 0x7B8-0x7C4  ->  KL_persist_journal  ->  rest_* (E1)
//                                                            ->  KL_acmp_lstn_ctx
//
//                The CSR decode below is the EXECUTABLE SPEC of the journal
//                ingest group documented in
//                docs/design/SAVED_STATE_FASTCONNECT.md §8 / REGISTER_MAP
//                0x7B8: milan_csr must reproduce exactly this behaviour
//                (same addresses, same W1S bits, same read-backs), the way
//                tb/verilator/tcam_csr mirrors the 0x700 TCAM group.
//---------------------------------------------------------------------------//

`default_nettype none

import acmp_pkg::*;

module persist_wrap #(
    parameter int unsigned CLK_FREQ_HZ_P = 10_000,
    parameter int unsigned N_SINKS_P     = 4,
    parameter logic [N_SINKS_P-1:0] PROBE_SM_EN_P  = 4'b1101,
    parameter logic [N_SINKS_P-1:0] SID_EXPLICIT_P = 4'b0010,
    parameter int unsigned MAX_REC_P     = 8
) (
    input  wire         clk_i,
    input  wire         rst_n,

    // ---- CSR plane (milan_csr stand-in) --------------------------------
    input  wire [31:0]  wr_addr_i,
    input  wire [31:0]  wr_data_i,
    input  wire         wr_p_i,        //! 1-cycle write strobe
    input  wire [31:0]  rd_addr_i,
    output logic [31:0] rd_data_o,

    // ---- identity / ticks ----------------------------------------------
    input  wire [63:0]  entity_id_i,
    input  wire [47:0]  station_mac_i,
    input  wire         tick_1s_i,
    input  wire [N_SINKS_P-1:0] ta_registered_i,
    input  wire [N_SINKS_P-1:0] ta_failed_i,

    // ---- ACMP RX monitor tap / TX master --------------------------------
    input  wire         rx_tvalid_i,
    input  wire [63:0]  rx_tdata_i,
    input  wire [7:0]   rx_tkeep_i,
    input  wire         rx_tlast_i,
    output wire [63:0]  m_axis_tdata,
    output wire [7:0]   m_axis_tkeep,
    output wire         m_axis_tvalid,
    output wire         m_axis_tlast,
    input  wire         m_axis_tready,

    // ---- context-table read port (the TB's window on the ctx RAM) -------
    input  wire                         tbl_req_i,
    input  wire [$clog2(N_SINKS_P)-1:0] tbl_idx_i,
    output wire                         tbl_gnt_o,
    output wire [ACMP_LSTN_CTX_W_C-1:0] tbl_ctx_o,

    // ---- observability ---------------------------------------------------
    output wire [N_SINKS_P-1:0] stream_active_o,
    output wire         rest_req_o,      //! probe: restore transactions seen
    output wire [3:0]   rest_idx_o
);

  localparam logic [31:0] A_JNL_CTRL_C = 32'h7B8;
  localparam logic [31:0] A_JNL_DATA_C = 32'h7BC;
  localparam logic [31:0] A_JNL_STAT_C = 32'h7C0;
  localparam logic [31:0] A_JNL_SEQ_C  = 32'h7C4;

  // -----------------------------------------------------------------------
  // CSR decode: three W1S command bits + one write-only data port. Every
  // strobe is exactly one cycle, exactly as milan_csr's register_write
  // process emits its command strobes.
  // -----------------------------------------------------------------------
  logic        jnl_start_r, jnl_end_r, jnl_abort_r, jnl_wr_r;
  logic [31:0] jnl_data_r;
  always_ff @(posedge clk_i) begin : csr_decode
    if (!rst_n) begin
      jnl_start_r <= 1'b0; jnl_end_r <= 1'b0; jnl_abort_r <= 1'b0;
      jnl_wr_r    <= 1'b0; jnl_data_r <= 32'h0;
    end else begin
      jnl_start_r <= 1'b0; jnl_end_r <= 1'b0; jnl_abort_r <= 1'b0;
      jnl_wr_r    <= 1'b0;
      if (wr_p_i) begin
        unique case (wr_addr_i)
          A_JNL_CTRL_C: begin
            jnl_start_r <= wr_data_i[0];
            jnl_end_r   <= wr_data_i[1];
            jnl_abort_r <= wr_data_i[2];
          end
          A_JNL_DATA_C: begin
            jnl_wr_r   <= 1'b1;
            jnl_data_r <= wr_data_i;
          end
          default: ;
        endcase
      end
    end
  end : csr_decode

  wire [31:0] jnl_stat_w, jnl_seq_w;
  always_comb begin : csr_read
    unique case (rd_addr_i)
      A_JNL_CTRL_C: rd_data_o = {jnl_stat_w[31:30], 30'd0};
      A_JNL_STAT_C: rd_data_o = jnl_stat_w;
      A_JNL_SEQ_C:  rd_data_o = jnl_seq_w;
      default:      rd_data_o = 32'h0;
    endcase
  end : csr_read

  // -----------------------------------------------------------------------
  // Journal decoder + replay master
  // -----------------------------------------------------------------------
  wire        rest_req_w;
  wire [3:0]  rest_idx_w;
  wire [63:0] rest_talker_w, rest_ctlr_w;
  wire [15:0] rest_tuid_w, rest_flags_w;
  wire        rest_ack_w;
  wire [1:0]  rest_status_w;

  KL_persist_journal #(
      .MAX_REC_P (MAX_REC_P)
  ) u_journal (
      .clk_i         (clk_i),
      .rst_n         (rst_n),
      .entity_id_i   (entity_id_i),
      .jnl_start_i   (jnl_start_r),
      .jnl_wr_i      (jnl_wr_r),
      .jnl_data_i    (jnl_data_r),
      .jnl_end_i     (jnl_end_r),
      .jnl_abort_i   (jnl_abort_r),
      .rest_req_o    (rest_req_w),
      .rest_idx_o    (rest_idx_w),
      .rest_talker_o (rest_talker_w),
      .rest_tuid_o   (rest_tuid_w),
      .rest_ctlr_o   (rest_ctlr_w),
      .rest_flags_o  (rest_flags_w),
      .rest_ack_i    (rest_ack_w),
      .rest_status_i (rest_status_w),
      .stat_o        (jnl_stat_w),
      .seq_o         (jnl_seq_w)
  );

  // -----------------------------------------------------------------------
  // The real N-context ACMP listener engine (unmodified shipping RTL)
  // -----------------------------------------------------------------------
  KL_acmp_lstn_ctx #(
      .CLK_FREQ_HZ_P  (CLK_FREQ_HZ_P),
      .N_SINKS_P      (N_SINKS_P),
      .PROBE_SM_EN_P  (PROBE_SM_EN_P),
      .SID_EXPLICIT_P (SID_EXPLICIT_P)
  ) u_lstn (
      .clk_i           (clk_i),
      .rst_n           (rst_n),
      .enable_i        (1'b1),
      .station_mac_i   (station_mac_i),
      .entity_id_i     (entity_id_i),
      .locked_i        (1'b0),          //! no AECP lock in this harness
      .lock_ctlr_i     (64'd0),
      .tick_1s_i       (tick_1s_i),
      .ta_registered_i (ta_registered_i),
      .ta_failed_i     (ta_failed_i),
      .lstn_declare_o  (),
      .stream_active_o (stream_active_o),
      //! TB fixture: no DMA model here, so the tapped lane is always ready
      //! (gh #65 - the tap qualifies its sample on tvalid && tready)
      .rx_tvalid_i     (rx_tvalid_i),
      .rx_tready_i     (1'b1),
      .rx_tdata_i      (rx_tdata_i),
      .rx_tkeep_i      (rx_tkeep_i),
      .rx_tlast_i      (rx_tlast_i),
      .m_axis_tdata    (m_axis_tdata),
      .m_axis_tkeep    (m_axis_tkeep),
      .m_axis_tvalid   (m_axis_tvalid),
      .m_axis_tlast    (m_axis_tlast),
      .m_axis_tready   (m_axis_tready),
      .view0_state_o   (),
      .view0_talker_o  (),
      .view0_tuid_o    (),
      .view0_sid_o     (),
      .view0_vlan_o    (),
      .view0_dmac_o    (),
      .view0_status_o  (),
      .view0_probing_o (),
      .view0_tk_avail_o(),
      .view1_bound_o   (),
      .view1_sid_o     (),
      .view1_dmac_o    (),
      .cmd_count_o     (),
      .probe_count_o   (),
      .tx_wedge_cnt_o  (),
      .dbg_o           (),
      .tbl_req_i       (tbl_req_i),
      .tbl_idx_i       (tbl_idx_i),
      .tbl_gnt_o       (tbl_gnt_o),
      .tbl_ctx_o       (tbl_ctx_o),
      .rest_req_i      (rest_req_w),
      .rest_idx_i      (rest_idx_w),
      .rest_talker_i   (rest_talker_w),
      .rest_tuid_i     (rest_tuid_w),
      .rest_ctlr_i     (rest_ctlr_w),
      .rest_flags_i    (rest_flags_w),
      .rest_ack_o      (rest_ack_w),
      .rest_status_o   (rest_status_w)
  );

  assign rest_req_o = rest_req_w;
  assign rest_idx_o = rest_idx_w;

endmodule

`default_nettype wire
