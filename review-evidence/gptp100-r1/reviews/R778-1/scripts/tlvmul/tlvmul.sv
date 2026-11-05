module tlvmul #(parameter int unsigned CLK_HZ_P = 100_000_000) (
  input logic clk_i, input logic [31:0] phc_addend_o, input logic [31:0] st_wdata_w_i,
  output logic signed [31:0] freq_o, output logic [31:0] k_o);
  wire [63:0] st_wdata_w = {32'd0, st_wdata_w_i};
  localparam longint unsigned TLV_K_C =
      ((64'(CLK_HZ_P) << 33) + 64'd500_000_000) / 64'd1_000_000_000;
  logic signed [24:0] tlv_dlt_r;
  logic signed [31:0] tlv_freq_r;
  wire signed [63:0] tlv_prod_w = 64'(tlv_dlt_r) *
                                  $signed({1'b0, TLV_K_C[31:0]});
  always_ff @(posedge clk_i) begin
    tlv_dlt_r <= 25'sd0
                   + 25'(phc_addend_o - st_wdata_w[31:0]);
      tlv_freq_r <= 32'(tlv_prod_w >>> 16);
  end
  assign freq_o = tlv_freq_r; assign k_o = TLV_K_C[31:0];
endmodule
module tlvtop(input logic clk_i, input logic [31:0] a_i, input logic [31:0] e_i,
  output logic signed [31:0] f2_o, f50_o, f100_o, f125_o, output logic [31:0] k2_o, k50_o, k100_o, k125_o);
  tlvmul #(.CLK_HZ_P(2_000_000)) u2 (.clk_i, .phc_addend_o(a_i), .st_wdata_w_i(e_i), .freq_o(f2_o), .k_o(k2_o));
  tlvmul #(.CLK_HZ_P(50_000_000)) u50 (.clk_i, .phc_addend_o(a_i), .st_wdata_w_i(e_i), .freq_o(f50_o), .k_o(k50_o));
  tlvmul #(.CLK_HZ_P(100_000_000)) u100 (.clk_i, .phc_addend_o(a_i), .st_wdata_w_i(e_i), .freq_o(f100_o), .k_o(k100_o));
  tlvmul #(.CLK_HZ_P(125_000_000)) u125 (.clk_i, .phc_addend_o(a_i), .st_wdata_w_i(e_i), .freq_o(f125_o), .k_o(k125_o));
endmodule
