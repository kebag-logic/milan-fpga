/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : axis_mux_rr_2in_1out_sva.sv
//  Project     : Milan TSN NIC -- assertion-based verification (#372)
//
//  Description : Simulation-only checker for hdl/common/axis_mux_rr_2in_1out.sv,
//                attached to every instance of that module by the bind in
//                axis_mux_rr_2in_1out_bind.sv. It never drives anything.
//
//                Whose obligation each property is:
//                  u_s0_stimulus, u_s1_stimulus  the two input streams obey
//                      AXI4-Stream (axis_stream_source_sva). These belong to
//                      whatever drives s0/s1 - the testbench here - and the
//                      mux is only correct while they hold.
//                  u_m_dut                       the output stream obeys
//                      AXI4-Stream. This is the mux's obligation.
//                  every ap_/ai_ property below  grant, ownership, state and
//                      forwarding laws of the mux itself: DUT obligations.
//
//                The one design decision that matters: packet OWNERSHIP is the
//                mux's state, so it is read from the DUT rather than guessed
//                from its ports. The bind decodes `state` against the DUT's
//                own enum literals and hands this checker three flags, so no
//                encoding is copied here. A state that decodes to none of them
//                is exactly what ap_state_legal exists to report.
//
//                Clocked laws (ap_*) are concurrent assertions sampled at the
//                rising edge and disabled while rst_n is low, except
//                ap_reset_releases_owner, which is ABOUT reset and so has no
//                disable. Combinational laws (ai_*) are deferred immediate
//                assertions: they hold at every settled point, in reset too.
//
//                Witness flags follow axis_stream_source_sva: a pass action
//                runs at every passing edge (pinned Verilator 5.050), so each
//                one reports whether the interesting case really occurred,
//                and the harness counts only those reports.
//                See docs/testing/ASSERTIONS.md.
//---------------------------------------------------------------------------//

`default_nettype none

module axis_mux_rr_2in_1out_sva #(
  parameter int unsigned TDATA_WIDTH_P = 64 //! the mux's TDATA_WIDTH
) (
  input wire                       clk_i,        //! the mux clock
  input wire                       rst_n,        //! the mux's synchronous, active-low reset

  input wire [TDATA_WIDTH_P-1:0]   s0_tdata_i,   //! input stream 0, as driven into the mux
  input wire                       s0_tvalid_i,  //! input stream 0 TVALID
  input wire                       s0_tready_i,  //! input stream 0 TREADY, as the mux drives it
  input wire                       s0_tlast_i,   //! input stream 0 TLAST
  input wire [TDATA_WIDTH_P/8-1:0] s0_tkeep_i,   //! input stream 0 TKEEP

  input wire [TDATA_WIDTH_P-1:0]   s1_tdata_i,   //! input stream 1, as driven into the mux
  input wire                       s1_tvalid_i,  //! input stream 1 TVALID
  input wire                       s1_tready_i,  //! input stream 1 TREADY, as the mux drives it
  input wire                       s1_tlast_i,   //! input stream 1 TLAST
  input wire [TDATA_WIDTH_P/8-1:0] s1_tkeep_i,   //! input stream 1 TKEEP

  input wire [TDATA_WIDTH_P-1:0]   m_tdata_i,    //! output stream, as the mux drives it
  input wire                       m_tvalid_i,   //! output stream TVALID
  input wire                       m_tready_i,   //! output stream TREADY, as the sink drives it
  input wire                       m_tlast_i,    //! output stream TLAST
  input wire [TDATA_WIDTH_P/8-1:0] m_tkeep_i,    //! output stream TKEEP

  input wire                       owner_none_i, //! the mux is IDLE: no packet owns the output
  input wire                       owner_s0_i,   //! STREAM_0: a packet from s0 owns the output
  input wire                       owner_s1_i    //! STREAM_1: a packet from s1 owns the output
);

  //! See axis_stream_source_sva.
  import "DPI-C" context function void axis_sva_witness(input string rule_name,
                                                        input bit nonvacuous);

  // ---- AXI4-Stream source obligations, one instance per interface ---------
  axis_stream_source_sva #(.TDATA_WIDTH_P(TDATA_WIDTH_P)) u_s0_stimulus (
    .clk_i   (clk_i),
    .rst_n   (rst_n),
    .tvalid_i(s0_tvalid_i),
    .tready_i(s0_tready_i),
    .tdata_i (s0_tdata_i),
    .tkeep_i (s0_tkeep_i),
    .tlast_i (s0_tlast_i)
  );

  axis_stream_source_sva #(.TDATA_WIDTH_P(TDATA_WIDTH_P)) u_s1_stimulus (
    .clk_i   (clk_i),
    .rst_n   (rst_n),
    .tvalid_i(s1_tvalid_i),
    .tready_i(s1_tready_i),
    .tdata_i (s1_tdata_i),
    .tkeep_i (s1_tkeep_i),
    .tlast_i (s1_tlast_i)
  );

  axis_stream_source_sva #(.TDATA_WIDTH_P(TDATA_WIDTH_P)) u_m_dut (
    .clk_i   (clk_i),
    .rst_n   (rst_n),
    .tvalid_i(m_tvalid_i),
    .tready_i(m_tready_i),
    .tdata_i (m_tdata_i),
    .tkeep_i (m_tkeep_i),
    .tlast_i (m_tlast_i)
  );

  // ---- events the ownership laws are written in ---------------------------
  //! the owning source hands over its TLAST beat at this edge
  logic owner_last_handshake_w;
  //! a source owns the output and has not yet handed over its TLAST beat
  logic s0_mid_packet_w;
  logic s1_mid_packet_w;
  assign owner_last_handshake_w = (owner_s0_i && s0_tvalid_i && s0_tready_i && s0_tlast_i)
                               || (owner_s1_i && s1_tvalid_i && s1_tready_i && s1_tlast_i);
  assign s0_mid_packet_w = owner_s0_i && !(s0_tvalid_i && s0_tready_i && s0_tlast_i);
  assign s1_mid_packet_w = owner_s1_i && !(s1_tvalid_i && s1_tready_i && s1_tlast_i);

  // ---- clocked laws: state, grant and packet ownership (DUT) --------------
  ap_state_legal: assert property (
      @(posedge clk_i) disable iff (!rst_n) $onehot({owner_none_i, owner_s0_i, owner_s1_i}))
    axis_sva_witness("ap_state_legal", 1'b1);
  else
    $error("the mux state decodes to none, or to more than one, of IDLE, STREAM_0 and STREAM_1");

  ap_grant_only_to_requester: assert property (
      @(posedge clk_i) disable iff (!rst_n)
      owner_none_i |=> (!owner_s0_i || $past(s0_tvalid_i)) && (!owner_s1_i || $past(s1_tvalid_i)))
    axis_sva_witness("ap_grant_only_to_requester",
                     $past(rst_n && owner_none_i) && (owner_s0_i || owner_s1_i));
  else
    $error("the arbiter granted the output to a source that was not offering a beat");

  ap_owner_held_until_tlast_handshake: assert property (
      @(posedge clk_i) disable iff (!rst_n)
      (s0_mid_packet_w || s1_mid_packet_w) |=> $stable({owner_s0_i, owner_s1_i}))
    axis_sva_witness("ap_owner_held_until_tlast_handshake",
                     $past(rst_n && (s0_mid_packet_w || s1_mid_packet_w)));
  else
    $error("the output changed owner before the owning packet's TLAST beat was taken");

  ap_owner_released_after_tlast: assert property (
      @(posedge clk_i) disable iff (!rst_n) owner_last_handshake_w |=> 1'b1)
    axis_sva_witness("ap_owner_released_after_tlast", $past(rst_n && owner_last_handshake_w));
  else
    $error("the owner kept the output after its TLAST beat was taken");

  //! No disable: this law is about reset. A reset sampled at one edge must
  //! leave no owner at the next, whatever was stalled when it arrived.
  ap_reset_releases_owner: assert property (
      @(posedge clk_i) !rst_n |=> owner_none_i)
    axis_sva_witness("ap_reset_releases_owner", $past(!rst_n));
  else
    $error("an owner survived a reset");

  // ---- combinational laws: grant and forwarding (DUT) ---------------------
  always_comb begin : forwarding_laws
    ai_grants_mutually_exclusive: assert final (!(s0_tready_i && s1_tready_i))
      axis_sva_witness("ai_grants_mutually_exclusive", s0_tready_i || s1_tready_i);
    else
      $error("s0 and s1 were both given TREADY in the same cycle");

    ai_ready_only_for_owner_and_ready_sink: assert final (
        s0_tready_i == (owner_s0_i && m_tready_i) && s1_tready_i == (owner_s1_i && m_tready_i))
      axis_sva_witness("ai_ready_only_for_owner_and_ready_sink",
                       (owner_s0_i || owner_s1_i) && m_tready_i);
    else
      $error("a source's TREADY is not exactly 'it owns the output and the sink is ready'");

    ai_tvalid_forwarded: assert final (
        m_tvalid_i == ((owner_s0_i && s0_tvalid_i) || (owner_s1_i && s1_tvalid_i)))
      axis_sva_witness("ai_tvalid_forwarded",
                       (owner_s0_i && s0_tvalid_i) || (owner_s1_i && s1_tvalid_i));
    else
      $error("m TVALID is not the owning source's TVALID, or is high with no owner");

    if (m_tvalid_i && m_tready_i) begin
      ai_payload_forwarded_on_transfer: assert final (
          owner_s0_i ? (m_tdata_i == s0_tdata_i && m_tkeep_i == s0_tkeep_i && m_tlast_i == s0_tlast_i)
                     : (owner_s1_i && m_tdata_i == s1_tdata_i && m_tkeep_i == s1_tkeep_i
                        && m_tlast_i == s1_tlast_i))
        axis_sva_witness("ai_payload_forwarded_on_transfer", 1'b1);
      else
        $error("an accepted m beat does not carry the owning source's TDATA, TKEEP and TLAST");
    end
  end : forwarding_laws

endmodule

`default_nettype wire
