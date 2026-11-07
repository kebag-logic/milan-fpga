// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//---------------------------------------------------------------------------//
//  File        : KL_mbx_cdc_window.sv
//  Description : One request and answer window of contract 2.3 across the
//                mailbox (sys) and datapath (dp) clocks, for KL_mbx_cdc
//                (#665 F-INT PR 2).
//
//                The mailbox opens a request with a new tag and holds it
//                until the answer under that tag, or its wait bound
//                (docs/design/MAILBOX_SPLIT.md, the face block). One
//                cdc_handshake carries the tag and the request in. In the
//                datapath clock a requester then speaks the processor's
//                protocol to the datapath's answer logic, which the split
//                keeps unchanged: it waits until wait is low, raises req
//                with the fields, and while req is up takes the answer in
//                the first cycle wait is low; then req falls for a cycle
//                at least. A second cdc_handshake carries the answer back
//                with the tag it was asked under, and the mailbox side
//                posts it as one pulse.
//
//                THE ONE DECISION: a newer request wins. One that lands
//                while the datapath still serves an older one, whose
//                window the mailbox has closed by its wait bound, restarts
//                the requester; the older answer, if it was already on its
//                way, carries the older tag, which KL_mbx discards.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_mbx_cdc_window #(
  parameter int unsigned TAG_W_P = 4,    //! the window's tag
  parameter int unsigned RQ_W_P  = 38,   //! the request's fields
  parameter int unsigned ANS_W_P = 32    //! the answer
) (
  input  wire                sys_clk_i,
  input  wire                sys_rst_n,
  input  wire                dp_clk_i,
  input  wire                dp_rst_n,
  //! ---- the mailbox side (sys)
  input  wire                m_req_i,       //! a request is open: tag and fields hold
  input  wire  [TAG_W_P-1:0] m_tag_i,
  input  wire  [RQ_W_P-1:0]  m_rq_i,
  output logic               m_ans_p_o,     //! one-cycle pulse: the answer
  output logic [TAG_W_P-1:0] m_ans_tag_o,   //! the tag it was asked under
  output logic [ANS_W_P-1:0] m_ans_data_o,
  //! ---- the datapath side (dp): the processor's request protocol
  output logic               d_req_o,
  output logic [RQ_W_P-1:0]  d_rq_o,
  input  wire  [ANS_W_P-1:0] d_data_i,
  input  wire                d_wait_i
);

  // ---- in: a rising request, carried with its tag ---------------------------
  logic m_req_q_r, m_send_r, m_rcv_w;
  always_ff @(posedge sys_clk_i) begin : m_in
    if (!sys_rst_n) begin
      m_req_q_r <= 1'b0;
      m_send_r  <= 1'b0;
    end else begin
      m_req_q_r <= m_req_i;
      //! held until the destination took it, then low for a cycle at least
      if (m_send_r) begin
        if (m_rcv_w) m_send_r <= 1'b0;
      end else if (m_req_i && !m_req_q_r) begin
        m_send_r <= 1'b1;
      end
    end
  end : m_in

  logic [TAG_W_P+RQ_W_P-1:0] in_w;
  logic                      in_p_w;
  cdc_handshake #(.WIDTH(TAG_W_P + RQ_W_P)) u_in (
    .src_clk(sys_clk_i), .src_rst_n(sys_rst_n), .src_in({m_tag_i, m_rq_i}), .src_send(m_send_r),
    .src_rcv(m_rcv_w), .dest_clk(dp_clk_i), .dest_rst_n(dp_rst_n), .dest_out(in_w), .dest_req(in_p_w));

  // ---- the requester, in the datapath clock -----------------------------------
  typedef enum logic [1:0] {IDLE_S, PRE_S, REQ_S, ANS_S} rq_state_e;
  rq_state_e          st_r;
  logic [TAG_W_P-1:0] tag_r;
  logic [RQ_W_P-1:0]  rq_r;
  logic [ANS_W_P-1:0] ans_r;
  logic               again_r, out_send_r, out_rcv_w;

  assign d_req_o = (st_r == REQ_S);
  assign d_rq_o  = rq_r;

  always_ff @(posedge dp_clk_i) begin : requester
    if (!dp_rst_n) begin
      st_r       <= IDLE_S;
      tag_r      <= '0;
      rq_r       <= '0;
      ans_r      <= '0;
      again_r    <= 1'b0;
      out_send_r <= 1'b0;
    end else begin
      if (in_p_w) begin
        tag_r <= in_w[RQ_W_P +: TAG_W_P];
        rq_r  <= in_w[RQ_W_P-1:0];
      end
      unique case (st_r)
        //! a request: req stays low for this cycle, so every face sees an edge
        IDLE_S: if (in_p_w) st_r <= PRE_S;
        //! the datapath is not waiting before the request is raised
        PRE_S:  if (in_p_w) st_r <= PRE_S; else if (!d_wait_i) st_r <= REQ_S;
        REQ_S: begin
          if (in_p_w) begin
            st_r <= PRE_S;
          end else if (!d_wait_i) begin
            ans_r      <= d_data_i;
            out_send_r <= 1'b1;
            st_r       <= ANS_S;
          end
        end
        default: begin   // ANS_S: the answer is on its way back
          if (in_p_w) again_r <= 1'b1;
          if (out_rcv_w) begin
            out_send_r <= 1'b0;
            again_r    <= 1'b0;
            st_r       <= (again_r || in_p_w) ? PRE_S : IDLE_S;
          end
        end
      endcase
    end
  end : requester

  // ---- out: the answer and the tag it was asked under ------------------------
  logic [TAG_W_P+ANS_W_P-1:0] out_w;
  logic                       out_p_w;
  cdc_handshake #(.WIDTH(TAG_W_P + ANS_W_P)) u_out (
    .src_clk(dp_clk_i), .src_rst_n(dp_rst_n), .src_in({tag_r, ans_r}), .src_send(out_send_r),
    .src_rcv(out_rcv_w), .dest_clk(sys_clk_i), .dest_rst_n(sys_rst_n), .dest_out(out_w), .dest_req(out_p_w));

  assign m_ans_p_o    = out_p_w;
  assign m_ans_tag_o  = out_w[ANS_W_P +: TAG_W_P];
  assign m_ans_data_o = out_w[ANS_W_P-1:0];

endmodule

`default_nettype wire
