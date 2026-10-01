// Variant: the old snapshot read asynchronously from the ring and subtracted
// in the write cycle, so no fabric register holds it (a LUT-RAM-friendly form).
module ring_probe_async #(parameter int DEPTH = 8, parameter int SHIFT = 3,
                          parameter logic [31:0] SPAN = 32'd4_096_000_000) (
  input  logic        clk_i,
  input  logic        rst_n,
  input  logic        we_i,
  input  logic [31:0] pick_i,
  output logic signed [31:0] rate_o
);
  localparam int AW = $clog2(DEPTH);
  logic [31:0] mem [DEPTH];
  logic [AW-1:0] ptr_r;
  always_ff @(posedge clk_i) if (we_i) mem[ptr_r] <= pick_i;
  always_ff @(posedge clk_i) begin
    if (!rst_n) ptr_r <= '0;
    else if (we_i) ptr_r <= ptr_r + 1'b1;
  end
  always_ff @(posedge clk_i)
    if (we_i) rate_o <= $signed(pick_i - mem[ptr_r] - SPAN) >>> SHIFT;
endmodule
