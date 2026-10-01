// Reviewer area probe (PR #631, head a463a1de): the E8 snapshot ring against
// the E1 256-entry ring. Read-old, write-new at one address, as the design page
// describes (MEDIA_CLOCK_FOLLOWING.md:591-597; KL_crf_rx.sv:320-325 pattern).
// Not the meter; only the storage, its pointer and the rate difference.
module ring_probe #(parameter int DEPTH = 8, parameter int SHIFT = 3,
                    parameter logic [31:0] SPAN = 32'd4_096_000_000) (
  input  logic        clk_i,
  input  logic        rst_n,
  input  logic        we_i,      // one snapshot (every 256 picks / every pick)
  input  logic [31:0] pick_i,
  output logic signed [31:0] rate_o
);
  localparam int AW = $clog2(DEPTH);
  logic [31:0] mem [DEPTH];
  logic [AW-1:0] ptr_r;
  logic [31:0] old_r, cur_r;
  always_ff @(posedge clk_i) begin
    if (we_i) begin
      mem[ptr_r] <= pick_i;
      old_r <= mem[ptr_r];
      cur_r <= pick_i;
    end
  end
  always_ff @(posedge clk_i) begin
    if (!rst_n) ptr_r <= '0;
    else if (we_i) ptr_r <= ptr_r + 1'b1;
  end
  always_ff @(posedge clk_i) rate_o <= $signed(cur_r - old_r - SPAN) >>> SHIFT;
endmodule
