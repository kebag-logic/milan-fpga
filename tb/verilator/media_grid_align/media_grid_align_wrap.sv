// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
//! Closed-loop harness: KL_media_grid_align steering the REAL KL_media_nco,
//! exactly the datapath's #74 wiring (u_o -> servo_trim_i, one selection
//! gate feeding both). The C++ side is the physical grid: it pulses
//! frame_ev_i on a fractional-period model of the TDM fsync and grades the
//! loop on the NCO's own tick_o - the oracle is the grid that comes out,
//! never an internal signal.

`default_nettype none

module media_grid_align_wrap (
  input  wire         clk,
  input  wire         rst_n,
  input  wire         sel_i,      //! the live CRF selection, gating BOTH
  input  wire         frame_ev_i, //! physical-grid frame marker (C++ model)
  output wire         tick_o,     //! the packet grid under test
  output wire signed [15:0] u_o,
  output wire         engaged_o,
  output wire signed [15:0] err_cyc_o,
  output wire [15:0]  phase_o
);

  wire signed [15:0] u_w;

  //! NEGATIVE CONTROL (the test-evidence contract): MGA_MUT_U_SIGN compiles
  //! the one defect this loop must never ship - the command sign inverted
  //! into the NCO, the runaway the whole sign chain exists to prevent. The
  //! Makefile runs that build expecting FAILURE; if it ever passes, the
  //! G2/G3 sign checks have gone vacuous.
`ifdef MGA_MUT_U_SIGN
  wire signed [15:0] u_nco_w = -u_w;
`else
  wire signed [15:0] u_nco_w = u_w;
`endif

  KL_media_grid_align #(
    .CLK_FREQ_HZ_P (100_000_000),
    .FS_HZ_P       (48_000)
  ) u_align (
    .clk_i (clk), .rst_n (rst_n),
    .sel_i (sel_i),
    .frame_ev_i (frame_ev_i),
    .tick_i (tick_o),
    .u_o (u_w),
    .engaged_o (engaged_o),
    .err_cyc_o (err_cyc_o)
  );

  KL_media_nco #(
    .CLK_FREQ_HZ_P (100_000_000),
    .FS_HZ_P       (48_000)
  ) u_nco (
    .clk_i (clk), .rst_n (rst_n),
    .trim_i (16'sd0),           //! the datapath ties trim_i off; INTERNAL
                                //! free-run must stay bit-exact nominal
    .servo_trim_i (u_nco_w),
    .servo_en_i (sel_i),
    .tick_o (tick_o),
    .phase_o (phase_o)
  );

  assign u_o = u_w;

endmodule

`default_nettype wire
