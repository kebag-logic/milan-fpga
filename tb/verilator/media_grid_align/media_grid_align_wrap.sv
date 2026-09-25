// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
//! Closed-loop harness: KL_media_grid_align steering the REAL KL_media_nco,
//! exactly the datapath's #74 wiring (u_o -> servo_trim_i, one selection
//! gate feeding both). The C++ side is the physical grid: it pulses
//! frame_ev_i on a fractional-period model of the TDM fsync and grades the
//! loop on the NCO's own tick_o - the oracle is the grid that comes out,
//! never an internal signal. The REAL KL_chan_map_capture sits beside them
//! on the same frame marker and tick, so [G7]-[G9] read the junction
//! counters the datapath ships, not a copy of their law.

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
  output wire [15:0]  phase_o,
  output wire [15:0]  tdm_dup_cnt_o,  //! the shipped junction counters
  output wire [15:0]  tdm_skip_cnt_o
);

  wire signed [15:0] u_w;

  //! NEGATIVE CONTROL (the test-evidence contract): MGA_MUT_U_SIGN compiles
  //! the one defect this loop must never ship - the command sign inverted
  //! into the NCO, the runaway the whole sign chain exists to prevent. The
  //! Makefile runs that build expecting FAILURE; if it ever passes, the
  //! G2/G3 sign checks have gone vacuous. MGA_MUT_NO_KEEPOFF zeroes the
  //! lock-phase keep-off (#74 item 2): the loop then locks on its raw
  //! engagement capture, and [G7] must fail.
`ifdef MGA_MUT_U_SIGN
  wire signed [15:0] u_nco_w = -u_w;
`else
  wire signed [15:0] u_nco_w = u_w;
`endif

  KL_media_grid_align #(
    .CLK_FREQ_HZ_P (100_000_000),
    .FS_HZ_P       (48_000)
`ifdef MGA_MUT_NO_KEEPOFF
    , .LOCK_KEEPOFF_CYC_P (0)
`endif
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

  //! the junction detector, wired as milan_datapath wires it: the loop's
  //! frame marker is its slot-0 pair write and the packet grid is its tick.
  //! The smallest legal shape - the tdm_slip_count block reads only those
  //! two, whatever the map and the lanes.
  KL_chan_map_capture #(
    .N_SLOTS_P (2), .N_TDM_P (2), .N_LB_STREAMS_P (1), .N_LB_CH_P (2)
  ) u_junction (
    .clk_i (clk), .rst_n (rst_n),
    .map_wr_en_i (1'b0), .map_wr_addr_i (2'd0), .map_wr_data_i (13'd0),
    .map_rd_en_i (1'b0), .map_rd_addr_i (2'd0),
    .map_rd_data_o (), .map_rd_valid_o (), .map_flat_o (),
    .i2s_pair_valid_i (1'b0), .i2s_l_i (24'd0), .i2s_r_i (24'd0),
    .tdm_pair_valid_i (frame_ev_i), .tdm_pair_slot_i (4'd0),
    .tdm_l_i (24'd0), .tdm_r_i (24'd0),
    .tone_smp_i (24'd0),
    .tick_i (tick_o),
    .pair_valid_o (), .pair_slot_o (), .pair_l_o (), .pair_r_o (),
    .lb_dup_cnt_o (), .lb_skip_cnt_o (),
    .tdm_dup_cnt_o (tdm_dup_cnt_o), .tdm_skip_cnt_o (tdm_skip_cnt_o)
  );

endmodule

`default_nettype wire
