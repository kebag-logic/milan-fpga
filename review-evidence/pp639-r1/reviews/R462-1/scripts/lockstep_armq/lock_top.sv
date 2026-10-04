// two arm-port blocks side by side: main's (armq_ref) and the head's (armq_dut)
/* verilator lint_off DECLFILENAME */
module lock_top #(parameter int unsigned AW = 6) (
  input  logic clk_i,
  input  logic rst_n,
  input  logic [7:0] in_vld_i,
  input  logic [7:0][1 + AW + 8 + 32 - 1:0] in_arm_i,
  output logic       r_valid_o, d_valid_o,
  output logic [1 + AW + 8 + 32 - 1:0] r_arm_o, d_arm_o,
  output logic [15:0] r_drop_o, d_drop_o,
  output logic [7:0][2:0] r_cnt_o, d_cnt_o
);
  armq_ref #(.TMR_AW_C(AW)) u_ref (.clk_i, .rst_n, .in_vld_i, .in_arm_i,
    .arm_valid_o(r_valid_o), .arm_o(r_arm_o), .drop_o(r_drop_o), .cnt_o(r_cnt_o));
  armq_dut #(.TMR_AW_C(AW)) u_dut (.clk_i, .rst_n, .in_vld_i, .in_arm_i,
    .arm_valid_o(d_valid_o), .arm_o(d_arm_o), .drop_o(d_drop_o), .cnt_o(d_cnt_o));
endmodule
