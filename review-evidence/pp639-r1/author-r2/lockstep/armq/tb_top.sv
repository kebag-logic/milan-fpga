// lockstep: main's arm-port block (armq_ref) beside the head's (armq_dut)
`default_nettype none
module tb_top
  import pp_pkg::*;
#(parameter int unsigned TMR_AW_C = 6) (
    input  wire clk_i,
    input  wire rst_n,
    input  wire [7:0]                vld_i,
    input  wire [7:0]                cancel_i,
    input  wire [8*TMR_AW_C-1:0]     slot_i,
    input  wire [63:0]               owner_i,
    input  wire [255:0]              deadline_i,
    // ref outputs
    output logic                     r_valid, r_cancel,
    output logic [TMR_AW_C-1:0]      r_slot,
    output logic [7:0]               r_owner,
    output logic [31:0]              r_deadline,
    output logic [15:0]              r_drop,
    // dut outputs
    output logic                     d_valid, d_cancel,
    output logic [TMR_AW_C-1:0]      d_slot,
    output logic [7:0]               d_owner,
    output logic [31:0]              d_deadline,
    output logic [15:0]              d_drop,
    // coverage (ref's internals; the dut's for the full-and-pop case)
    output logic [7:0][2:0]          cnt_o,
    output logic [7:0]               pop_o,
    output logic [7:0]               push_o
);
  logic [7:0][2:0] d_cnt;
  logic [7:0] d_pop, d_push;
`define FACE(blk, k, pfx) \
      .pfx``arm_valid_w   (vld_i[k]), \
      .pfx``arm_cancel_w  (cancel_i[k]), \
      .pfx``arm_slot_w    (slot_i[k*TMR_AW_C +: TMR_AW_C]), \
      .pfx``arm_owner_w   (owner_i[k*8 +: 8]), \
      .pfx``arm_deadline_w(deadline_i[k*32 +: 32])
  armq_ref #(.TMR_AW_C(TMR_AW_C)) u_ref (
      .clk_i, .rst_n,
      `FACE(r, 0, lstn_), `FACE(r, 1, tkr_), `FACE(r, 2, adp_), `FACE(r, 3, srp_),
      `FACE(r, 4, org_), `FACE(r, 5, maapeng_), `FACE(r, 6, i_ntfy_), `FACE(r, 7, i_ntfy_mon_),
      .tmr_arm_valid_w(r_valid), .tmr_arm_cancel_w(r_cancel), .tmr_arm_slot_w(r_slot),
      .tmr_arm_owner_w(r_owner), .tmr_arm_deadline_w(r_deadline), .arm_drop_o(r_drop),
      .dbg_cnt_o(cnt_o), .dbg_pop_o(pop_o), .dbg_push_o(push_o));
  armq_dut #(.TMR_AW_C(TMR_AW_C)) u_dut (
      .clk_i, .rst_n,
      `FACE(d, 0, lstn_), `FACE(d, 1, tkr_), `FACE(d, 2, adp_), `FACE(d, 3, srp_),
      `FACE(d, 4, org_), `FACE(d, 5, maapeng_), `FACE(d, 6, i_ntfy_), `FACE(d, 7, i_ntfy_mon_),
      .tmr_arm_valid_w(d_valid), .tmr_arm_cancel_w(d_cancel), .tmr_arm_slot_w(d_slot),
      .tmr_arm_owner_w(d_owner), .tmr_arm_deadline_w(d_deadline), .arm_drop_o(d_drop),
      .dbg_cnt_o(d_cnt), .dbg_pop_o(d_pop), .dbg_push_o(d_push));
endmodule
`default_nettype wire
