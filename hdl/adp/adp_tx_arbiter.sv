/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : adp_tx_arbiter.sv
//  Project     : Milan ADP  (MAC TX integration)
//
//  Description : Two-input AXI4-Stream *packet* arbiter that merges the ADP
//                advertiser's frames (`s_adp`) with the normal shaped datapath
//                (`s_data`) into the single MAC TX stream (`m`). It grants at
//                frame boundaries and locks the granted source until its `tlast`,
//                so **a frame is never interrupted mid-packet** and ADP frames are
//                only ever inserted in inter-frame gaps of the datapath.
//
//                Arbitration is round-robin (grant alternates between the two
//                sources) so neither can be starved: the low-rate ADP stream is
//                always served in a gap, and the datapath is never blocked by ADP
//                for more than the ADP frame in flight.
//
//  Latency     : combinational grant (no start-of-frame bubble); fully
//                back-pressure safe — `m.tready` is routed only to the granted
//                source, the other source sees `tready = 0`.
//---------------------------------------------------------------------------//

`default_nettype none

module adp_tx_arbiter #(
    parameter int DATA_WIDTH = 64,
    parameter int KEEP_WIDTH = DATA_WIDTH/8
)(
    input  wire                    clk_i,
    input  wire                    rst_n,

    // ---- slave 0: normal datapath (shaper -> MAC) ----
    input  wire [DATA_WIDTH-1:0]   s_data_tdata,
    input  wire [KEEP_WIDTH-1:0]   s_data_tkeep,
    input  wire                    s_data_tvalid,
    input  wire                    s_data_tlast,
    output wire                    s_data_tready,

    // ---- slave 1: ADP advertiser ----
    input  wire [DATA_WIDTH-1:0]   s_adp_tdata,
    input  wire [KEEP_WIDTH-1:0]   s_adp_tkeep,
    input  wire                    s_adp_tvalid,
    input  wire                    s_adp_tlast,
    output wire                    s_adp_tready,

    // ---- master: to MAC TX ----
    output wire [DATA_WIDTH-1:0]   m_tdata,
    output wire [KEEP_WIDTH-1:0]   m_tkeep,
    output wire                    m_tvalid,
    output wire                    m_tlast,
    input  wire                    m_tready
);

  // sel: 0 = datapath, 1 = adp
  reg  locked_r;        //! a source is granted and being forwarded until tlast
  reg  sel_r;           //! the granted source while locked
  reg  last_grant_r;    //! last source granted (for round-robin fairness)

  // Combinational grant: while locked keep sel_r; else pick a valid source,
  // preferring the one that was NOT granted last (round-robin).
  logic gsel;           //! source selected this cycle
  logic active;         //! a source is selected (locked or a fresh grant)
  always_comb begin
    gsel   = sel_r;
    active = locked_r;
    if (!locked_r) begin
      active = s_data_tvalid | s_adp_tvalid;
      if (s_data_tvalid && s_adp_tvalid) gsel = ~last_grant_r; // both -> alternate
      else if (s_adp_tvalid)             gsel = 1'b1;
      else                               gsel = 1'b0;
    end
  end

  // Output mux + per-source ready routing
  assign m_tvalid      = active & (gsel ? s_adp_tvalid : s_data_tvalid);
  assign m_tdata       = gsel ? s_adp_tdata : s_data_tdata;
  assign m_tkeep       = gsel ? s_adp_tkeep : s_data_tkeep;
  assign m_tlast       = gsel ? s_adp_tlast : s_data_tlast;
  assign s_data_tready = active & ~gsel & m_tready;
  assign s_adp_tready  = active &  gsel & m_tready;

  wire beat_accepted = m_tvalid & m_tready;

  always_ff @(posedge clk_i) begin : lock_fsm
    if (!rst_n) begin
      locked_r <= 1'b0; sel_r <= 1'b0; last_grant_r <= 1'b0;
    end else begin
      // lock onto the granted source on its first accepted beat
      if (!locked_r && active && beat_accepted) begin
        locked_r <= 1'b1; sel_r <= gsel;
      end
      // release at end-of-frame (this wins a same-cycle single-beat frame)
      if (active && beat_accepted && m_tlast) begin
        locked_r     <= 1'b0;
        last_grant_r <= gsel;
      end
    end
  end

endmodule

`default_nettype wire
