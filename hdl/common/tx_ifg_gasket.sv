/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : tx_ifg_gasket.sv
//  Project     : Milan AVTP
//
//  Description : Minimum inter-frame-gap enforcer on the MAC-facing TX AXIS.
//                The bare LiteEth core is cut-through to the PHY and the
//                milan_cd->sys TX CDC has finite depth: two frames emitted
//                back-to-back (no idle beat between frame1.tlast and
//                frame2 SOF) let the SECOND frame race frame1's PHY
//                serialization and be silently eaten (silicon 2026-07-19:
//                the MVRP half of every MSRP+MVRP pair vanished; the
//                intermittent ACMP CONNECT_RX_RESPONSE loss is the same
//                bug when the response follows another control frame).
//                Datapath-side proof: the merge emits both frames even at
//                a 2-cycle gap, so the eater is downstream (MAC/CDC).
//
//                This gasket passes AXIS through unchanged, but after each
//                accepted tlast it BACK-PRESSURES the upstream (s_tready=0)
//                and holds the master idle (m_tvalid=0) for GAP_CYCLES,
//                guaranteeing a clean idle window between every frame that
//                reaches the MAC - fixing ALL back-to-back cases, not just
//                lwSRP's. GAP_CYCLES covers a small-frame PHY serialization
//                (60 B @ 100 Mbit ~= 5 us) with margin.
//---------------------------------------------------------------------------//

`default_nettype none

module tx_ifg_gasket #(
  parameter int DATA_WIDTH  = 64,
  parameter int GAP_CYCLES  = 512   //! idle cycles held between frames
)(
  input  wire                     clk_i,
  input  wire                     rst_n,

  input  wire [DATA_WIDTH-1:0]    s_tdata,
  input  wire [DATA_WIDTH/8-1:0]  s_tkeep,
  input  wire                     s_tvalid,
  input  wire                     s_tlast,
  output wire                     s_tready,

  output wire [DATA_WIDTH-1:0]    m_tdata,
  output wire [DATA_WIDTH/8-1:0]  m_tkeep,
  output wire                     m_tvalid,
  output wire                     m_tlast,
  input  wire                     m_tready
);

  localparam int CW = (GAP_CYCLES <= 1) ? 1 : $clog2(GAP_CYCLES);

  reg [CW-1:0] gap_r;      //! remaining gap cycles (0 = passthrough)
  reg          gapping_r;  //! high while enforcing the idle window

  //! combinational passthrough, gated by the gap window
  assign m_tdata  = s_tdata;
  assign m_tkeep  = s_tkeep;
  assign m_tlast  = s_tlast;
  assign m_tvalid = s_tvalid & ~gapping_r;
  assign s_tready = m_tready & ~gapping_r;

  wire beat_acc = s_tvalid & s_tready;

  always_ff @(posedge clk_i or negedge rst_n) begin : gasket
    if (!rst_n) begin
      gap_r <= '0; gapping_r <= 1'b0;
    end else begin
      if (gapping_r) begin
        if (gap_r == '0) gapping_r <= 1'b0;
        else             gap_r <= gap_r - 1'b1;
      end
      //! arm the gap on end-of-frame (wins a same-cycle single-beat frame)
      else if (beat_acc && s_tlast) begin
        gapping_r <= 1'b1;
        gap_r     <= CW'(GAP_CYCLES - 1);
      end
    end
  end : gasket

endmodule

`default_nettype wire
