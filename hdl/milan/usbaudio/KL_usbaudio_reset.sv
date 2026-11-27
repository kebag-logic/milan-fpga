// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Session reset asserts without a clock and releases on local edges only.
`default_nettype none
module KL_usbaudio_reset (
  input wire clk_i, //! destination clock
  input wire reset_i, //! common session reset, asynchronous assertion
  output wire rst_n //! active-low reset, two-edge release
);
  (* ASYNC_REG = "TRUE" *) logic release_meta_r, release_sync_r;
  always_ff @(posedge clk_i or posedge reset_i) begin : local_release
    if (reset_i) begin
      release_meta_r <= 0;
      release_sync_r <= 0;
    end else begin
      release_meta_r <= 1;
      release_sync_r <= release_meta_r;
    end
  end : local_release
  assign rst_n = release_sync_r;
endmodule
`default_nettype wire
