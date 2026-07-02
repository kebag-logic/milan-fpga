/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : cdc_pulse.sv
//  Description : Open, FPGA-independent single-bit **pulse** clock-domain
//                crossing (toggle synchroniser). A 1-cycle pulse in the source
//                domain produces exactly one 1-cycle pulse in the destination
//                domain. Replaces Xilinx `xpm_cdc_pulse`
//                (docs/OPEN_SOURCE_MIGRATION.md Track 1.4).
//
//                Constraint: source pulses must be spaced further apart than the
//                round-trip synchroniser latency (true for per-frame SOP events).
//                Add a false-path/max-delay on `src_level` in synthesis.
//---------------------------------------------------------------------------//
`default_nettype none

module cdc_pulse #(
    parameter int DEST_SYNC_FF = 2   //! destination synchroniser depth
)(
    input  wire src_clk,
    input  wire src_rst_n,
    input  wire src_pulse,           //! 1-cycle pulse in the source domain
    input  wire dest_clk,
    input  wire dest_rst_n,
    output wire dest_pulse           //! 1-cycle pulse in the destination domain
);

  //! source: flip a level on every input pulse
  reg src_level;
  always_ff @(posedge src_clk)
    if (!src_rst_n)      src_level <= 1'b0;
    else if (src_pulse)  src_level <= ~src_level;

  //! destination: synchronise the level + one extra stage for edge detect
  (* ASYNC_REG = "TRUE" *) reg [DEST_SYNC_FF:0] sync;
  always_ff @(posedge dest_clk)
    if (!dest_rst_n) sync <= '0;
    else             sync <= {sync[DEST_SYNC_FF-1:0], src_level};

  assign dest_pulse = sync[DEST_SYNC_FF] ^ sync[DEST_SYNC_FF-1];

endmodule

`default_nettype wire
