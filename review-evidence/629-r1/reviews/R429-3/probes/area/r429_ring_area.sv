// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer area probe (R429-3): only the rate-history part that D8 changes.
// E1: KL_crf_rx-style 256-entry read-old/write-new ring, rate per pick.
// E8: 8-entry snapshot ring written every 256 picks, rate = (P - S8 - 8*512e6) >>> 3.
`default_nettype none
module r429_e1 (input wire clk, input wire rst, input wire restart, input wire pick_v,
                input wire [31:0] pick, output logic signed [31:0] rate, output logic valid);
  logic [31:0] ring [256];
  logic [7:0] wa;
  logic [8:0] fresh;
  logic [31:0] old;
  always_ff @(posedge clk) begin
    if (rst || restart) begin wa <= '0; fresh <= '0; valid <= 1'b0; end
    else if (pick_v) begin
      old <= ring[wa];
      ring[wa] <= pick;
      wa <= wa + 1'b1;
      if (fresh != 9'd256) fresh <= fresh + 1'b1;
      valid <= (fresh == 9'd256);
      rate <= $signed(pick - ring[wa] - 32'd512_000_000);
    end
  end
endmodule
module r429_e8 (input wire clk, input wire rst, input wire restart, input wire pick_v,
                input wire [31:0] pick, output logic signed [31:0] rate, output logic valid);
  logic [31:0] ring [8];
  logic [2:0] wa;
  logic [7:0] sub;
  logic [11:0] fresh;
  logic [31:0] d;
  always_ff @(posedge clk) begin
    if (rst || restart) begin wa <= '0; sub <= '0; fresh <= '0; valid <= 1'b0; end
    else if (pick_v) begin
      sub <= sub + 1'b1;
      if (fresh != 12'd2048) fresh <= fresh + 1'b1;
      if (sub == 8'd0) begin
        ring[wa] <= pick;
        wa <= wa + 1'b1;
        d = pick - ring[wa] - 32'd4_096_000_000;
        if (fresh == 12'd2048) begin rate <= $signed(d) >>> 3; valid <= 1'b1; end
      end
    end
  end
endmodule
`default_nettype wire
