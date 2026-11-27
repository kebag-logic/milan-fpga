/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
// Fabric status for LD2/LD3. Register the complete predicates before crossing
// clocks, so a source change cannot combine independently synchronized bits.
// Authority: #1020 ruling, #1018; IEEE 1722.1-2021 7.4.23.
//---------------------------------------------------------------------------//
`default_nettype none
module KL_status_led_truth (
  input wire clk_i,              //! datapath clock
  input wire rst_ni,             //! synchronous active-low datapath reset
  input wire input_locked_i,     //! any stream input media-locked
  input wire output_open_i,      //! any stream output transmit gate open
  input wire clock_internal_i,   //! selected source is internal
  input wire clock_stream_i,     //! selected source is a stream input
  input wire source_locked_i,    //! selected stream input media-locked
  input wire clock_locked_i,     //! existing media clock-domain lock level
  output logic stream_o,         //! registered LD2 level
  output logic clock_o           //! registered LD3 level
);
  always_ff @(posedge clk_i) begin : status
    if (!rst_ni) begin
      stream_o <= 1'b0;
      clock_o <= 1'b0;
    end else begin
      stream_o <= input_locked_i || output_open_i;
      clock_o <= clock_internal_i ||
                 (clock_locked_i && (!clock_stream_i || source_locked_i));
    end
  end : status
endmodule
`default_nettype wire
