// Lockstep top: main's arm-port block (armq_ref) beside the candidate's (armq_dut),
// identical inputs; both outputs and the candidate's ring state exposed for coverage.
module armq_ls #(parameter int unsigned AW = 6) (
    input  wire              clk_i,
    input  wire              rst_n,
    input  wire [7:0]        vld,
    input  wire [7:0]        cancel,
    input  wire [8*8-1:0]    slot,      // 8 bits per face, low AW used
    input  wire [8*8-1:0]    owner,
    input  wire [8*32-1:0]   deadline,
    output logic [63:0]      ref_port,
    output logic [63:0]      dut_port,
    output logic             ref_valid,
    output logic             dut_valid,
    output logic [15:0]      ref_drop,
    output logic [15:0]      dut_drop,
    output logic [7:0]       cov_full_pop_push,  // face full, pops and pushes this clock
    output logic [7:0]       cov_drop_face       // face refuses an offer this clock
);
  logic r_v, r_c, d_v, d_c;
  logic [AW-1:0] r_s, d_s;
  logic [7:0] r_o, d_o;
  logic [31:0] r_d, d_d;
`define FACE(inst, k) \
      .in_``inst``_valid(vld[k]), .in_``inst``_cancel(cancel[k]), \
      .in_``inst``_slot(slot[8*k +: AW]), .in_``inst``_owner(owner[8*k +: 8]), \
      .in_``inst``_deadline(deadline[32*k +: 32])
  armq_ref #(.AW(AW)) u_ref (.clk_i, .rst_n,
      `FACE(lstn, 0), `FACE(tkr, 1), `FACE(adp, 2), `FACE(srp, 3),
      `FACE(org, 4), `FACE(maapeng, 5), `FACE(ntfy, 6), `FACE(ntfy_mon, 7),
      .o_valid(r_v), .o_cancel(r_c), .o_slot(r_s), .o_owner(r_o), .o_deadline(r_d),
      .o_drop(ref_drop));
  armq_dut #(.AW(AW)) u_dut (.clk_i, .rst_n,
      `FACE(lstn, 0), `FACE(tkr, 1), `FACE(adp, 2), `FACE(srp, 3),
      `FACE(org, 4), `FACE(maapeng, 5), `FACE(ntfy, 6), `FACE(ntfy_mon, 7),
      .o_valid(d_v), .o_cancel(d_c), .o_slot(d_s), .o_owner(d_o), .o_deadline(d_d),
      .o_drop(dut_drop));
  assign ref_port = 64'({r_c, r_s, r_o, r_d});
  assign dut_port = 64'({d_c, d_s, d_o, d_d});
  assign ref_valid = r_v;
  assign dut_valid = d_v;
  always_comb begin
    for (int k = 0; k < 8; k++) begin
      cov_full_pop_push[k] = (u_dut.armq_cnt_r[k] == 3'd4) && u_dut.armq_pop_w[k]
                             && u_dut.armq_push_ok_w[k];
      cov_drop_face[k] = u_dut.armq_in_vld_w[k] && !u_dut.armq_push_ok_w[k];
    end
  end
endmodule
