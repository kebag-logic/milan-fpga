// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Session reset asserts without a clock and releases on local edges only.
`default_nettype none
module KL_usbaudio_reset (
  input wire clk_i, //! destination clock
  input wire reset_i, //! common session reset, asynchronous assertion
  output wire rst_n //! active-low reset, two-edge release
);
  (* ASYNC_REG = "TRUE" *) logic [1:0] release_r;
  always_ff @(posedge clk_i or posedge reset_i) begin : local_release
    if (reset_i) release_r <= 0;
    else release_r <= {release_r[0], 1'b1};
  end : local_release
  assign rst_n = release_r[1];
endmodule
`default_nettype wire
