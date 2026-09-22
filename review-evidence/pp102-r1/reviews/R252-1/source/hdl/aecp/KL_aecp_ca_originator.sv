/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  CONTROLLER_AVAILABLE command builder for Milan v1.2 5.4.5.3.
//
//  The builder writes one complete, padded Ethernet frame into the shared TX
//  slot pool, then hands the committed slot to KL_pp_originator. The latter
//  owns the sequence counter, the 250 ms timeout, the one exact retry and the
//  response/failure routing. The slot is therefore immutable after ISSUE.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_aecp_ca_originator #(
    parameter int unsigned TMR_SLOTS_P  = pp_pkg::PP_TIMER_SLOTS_C,
    parameter int unsigned TMR_CA_BASE_P = 57,
    parameter int unsigned TX_STD_SLOTS_P = 4,
    parameter int unsigned TX_OVERSIZE_BYTES_P = 1600,
    localparam int unsigned TMR_AW_C = (TMR_SLOTS_P > 1) ? $clog2(TMR_SLOTS_P) : 1,
    localparam int unsigned TXS_W_C = $clog2(TX_STD_SLOTS_P + 1),
    localparam int unsigned TXA_W_C = $clog2(TX_OVERSIZE_BYTES_P + 1)
) (
    input  wire                 clk_i,
    input  wire                 rst_n,
    input  wire [63:0]          entity_id_i,
    input  wire [47:0]          own_mac_i,

    input  wire                 req_valid_i,
    input  wire [3:0]           req_owner_i,
    input  wire [63:0]          req_ctlr_eid_i,
    input  wire [47:0]          req_mac_i,
    output logic                req_ready_o,
    input  wire                 cancel_valid_i,
    input  wire [3:0]           cancel_owner_i,
    output logic                cancel_release_valid_o,
    output logic [TXS_W_C-1:0]  cancel_release_slot_o,
    output logic                issued_valid_o,
    output logic [3:0]          issued_owner_o,

    output logic                txs_alloc_req_o,
    input  wire                 txs_alloc_gnt_i,
    input  wire [TXS_W_C-1:0]   txs_alloc_slot_i,
    output logic [TXS_W_C-1:0]  txs_wr_slot_o,
    output logic [TXA_W_C-1:0]  txs_wr_addr_o,
    output logic                txs_wr_valid_o,
    output logic [7:0]          txs_wr_data_o,
    output logic                txs_wr_commit_o,
    output logic [TXA_W_C-1:0]  txs_wr_len_o,
    output logic                txs_abort_o,

    output logic                iss_valid_o,
    output logic [3:0]          iss_owner_o,
    output logic [2:0]          iss_tx_slot_o,
    output logic [111:0]        iss_key_o,
    output logic [TMR_AW_C-1:0] iss_tmr_slot_o,
    output logic [15:0]         iss_timeout_ms_o,
    input  wire                 iss_ready_i,
    input  wire                 iss_gnt_i,
    input  wire [15:0]          iss_seq_i,
    input  wire [3:0]           iss_id_i
);

  typedef enum logic [2:0] {C_IDLE, C_ALLOC, C_WRITE, C_COMMIT, C_ISSUE} c_st_e;
  c_st_e c_st_r;

  logic [3:0]  owner_r;
  logic [63:0] ctlr_eid_r;
  logic [47:0] ctlr_mac_r;
  logic [15:0] seq_r;
  logic [TXS_W_C-1:0] slot_r;
  logic [5:0] byte_r;
  logic       alloc_wait_r;
  logic       cancel_hit_w;

  always_comb begin : frame_byte
    txs_wr_data_o = 8'd0;
    if (byte_r < 6)
      txs_wr_data_o = ctlr_mac_r[47 - 8*byte_r -: 8];
    else if (byte_r < 12)
      txs_wr_data_o = own_mac_i[47 - 8*(byte_r - 6) -: 8];
    else if (byte_r == 12) txs_wr_data_o = 8'h22;
    else if (byte_r == 13) txs_wr_data_o = 8'hF0;
    else if (byte_r == 14) txs_wr_data_o = 8'hFB; // cd=1, subtype AECP
    else if (byte_r == 15) txs_wr_data_o = 8'h00; // AEM_COMMAND
    else if (byte_r == 16) txs_wr_data_o = 8'h00; // SUCCESS, cdl[10:8]
    else if (byte_r == 17) txs_wr_data_o = 8'h0C; // base AEM cdl
    else if (byte_r < 26)
      txs_wr_data_o = ctlr_eid_r[63 - 8*(byte_r - 18) -: 8];
    else if (byte_r < 34)
      txs_wr_data_o = entity_id_i[63 - 8*(byte_r - 26) -: 8];
    else if (byte_r == 34) txs_wr_data_o = seq_r[15:8];
    else if (byte_r == 35) txs_wr_data_o = seq_r[7:0];
    else if (byte_r == 36) txs_wr_data_o = 8'h00;
    else if (byte_r == 37) txs_wr_data_o = 8'h03; // CONTROLLER_AVAILABLE
  end

  assign cancel_hit_w      = cancel_valid_i && (cancel_owner_i == owner_r)
                             && (c_st_r != C_IDLE);
  assign req_ready_o       = (c_st_r == C_IDLE);
  // The slot pool returns its grant one cycle after sampling a request. A
  // held request would therefore allocate twice before the first grant is
  // visible. Pulse once, wait for that result, then retry if the pool was
  // full. The top arbiter parks the request while another builder owns it.
  assign txs_alloc_req_o   = (c_st_r == C_ALLOC) && !cancel_hit_w
                             && !alloc_wait_r;
  assign txs_wr_slot_o     = slot_r;
  assign txs_wr_addr_o     = TXA_W_C'(byte_r);
  assign txs_wr_valid_o    = (c_st_r == C_WRITE) && !cancel_hit_w;
  assign txs_wr_commit_o   = (c_st_r == C_COMMIT) && !cancel_hit_w;
  assign txs_wr_len_o      = TXA_W_C'(60);
  assign iss_valid_o       = (c_st_r == C_ISSUE) && !cancel_hit_w;
  assign iss_owner_o       = owner_r;
  assign iss_tx_slot_o     = 3'(slot_r);
  assign iss_key_o         = {ctlr_eid_r, ctlr_mac_r};
  assign iss_tmr_slot_o    = TMR_AW_C'(TMR_CA_BASE_P + 32'(iss_id_i));
  assign iss_timeout_ms_o  = 16'd250;

  always_ff @(posedge clk_i) begin : builder
    if (!rst_n) begin
      c_st_r         <= C_IDLE;
      owner_r        <= 4'd0;
      ctlr_eid_r     <= 64'd0;
      ctlr_mac_r     <= 48'd0;
      seq_r          <= 16'd0;
      slot_r         <= '0;
      byte_r         <= 6'd0;
      alloc_wait_r   <= 1'b0;
      issued_valid_o <= 1'b0;
      issued_owner_o <= 4'd0;
      txs_abort_o    <= 1'b0;
      cancel_release_valid_o <= 1'b0;
      cancel_release_slot_o  <= '0;
    end else begin
      issued_valid_o <= 1'b0;
      txs_abort_o <= 1'b0;
      cancel_release_valid_o <= 1'b0;
      cancel_release_slot_o  <= '0;
      unique case (c_st_r)
        C_IDLE: if (req_valid_i) begin
          owner_r    <= req_owner_i;
          ctlr_eid_r <= req_ctlr_eid_i;
          ctlr_mac_r <= req_mac_i;
          alloc_wait_r <= 1'b0;
          c_st_r     <= C_ALLOC;
        end
        C_ALLOC: if (cancel_hit_w) begin
          txs_abort_o <= 1'b1;
          if (txs_alloc_gnt_i) begin
            cancel_release_valid_o <= 1'b1;
            cancel_release_slot_o  <= txs_alloc_slot_i;
          end
          alloc_wait_r <= 1'b0;
          c_st_r <= C_IDLE;
        end else if (txs_alloc_gnt_i) begin
          slot_r <= txs_alloc_slot_i;
          seq_r  <= iss_seq_i;
          byte_r <= 6'd0;
          alloc_wait_r <= 1'b0;
          c_st_r <= C_WRITE;
        end else begin
          alloc_wait_r <= !alloc_wait_r;
        end
        C_WRITE: if (cancel_hit_w) begin
          txs_abort_o <= 1'b1;
          cancel_release_valid_o <= 1'b1;
          cancel_release_slot_o  <= slot_r;
          c_st_r <= C_IDLE;
        end else begin
          if (byte_r == 6'd59) c_st_r <= C_COMMIT;
          else                 byte_r <= byte_r + 6'd1;
        end
        C_COMMIT: if (cancel_hit_w) begin
          txs_abort_o <= 1'b1;
          cancel_release_valid_o <= 1'b1;
          cancel_release_slot_o  <= slot_r;
          c_st_r <= C_IDLE;
        end else begin
          c_st_r <= C_ISSUE;
        end
        C_ISSUE: if (cancel_hit_w) begin
          txs_abort_o <= 1'b1;
          cancel_release_valid_o <= 1'b1;
          cancel_release_slot_o  <= slot_r;
          c_st_r <= C_IDLE;
        end else if (iss_gnt_i) begin
          issued_valid_o <= 1'b1;
          issued_owner_o <= owner_r;
          c_st_r         <= C_IDLE;
        end
        default: c_st_r <= C_IDLE;
      endcase
    end
  end

  logic unused_ready_w;
  assign unused_ready_w = iss_ready_i;

endmodule : KL_aecp_ca_originator
`default_nettype wire
