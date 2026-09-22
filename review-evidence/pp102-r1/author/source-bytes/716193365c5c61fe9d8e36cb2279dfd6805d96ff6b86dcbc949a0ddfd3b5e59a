/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : side_port_tb_wrap.sv (TB-only integration, tb/side_port)
//
//  Description : Instantiates KL_pp_side_port "A" (EN_FW_ASSIST_P = 1, so
//                all six 07 §5.5 windows are live) with the REAL
//                KL_pp_trace_ring behind window 0x40000 and the other five
//                windows exposed to the C++ harness as stub ports; plus a
//                second KL_pp_side_port "B" at the F01.5 default
//                (EN_FW_ASSIST_P = 0) with auto-acknowledged backends, to
//                prove window 0x50000 vanishes when the parameter is off.
//
//                TB glue for the trace window (the in-window layout is not
//                pinned by 07 §5.5 — an integration choice mirrored by the
//                C++ model): offset bit 10 clear = ring records, word
//                offset {record[7:0], lane[1:0]}; offset bit 10 set = the
//                16-bit monotonic write counter.
//---------------------------------------------------------------------------//
`default_nettype none

module side_port_tb_wrap (
    input  wire          clk_i,
    input  wire          rst_n,
    input  wire          entity_enable_i,

    // ---- host A (all six windows live) ----
    input  wire          req_valid_i,
    input  wire          we_i,
    input  wire  [19:0]  addr_i,
    input  wire  [31:0]  wdata_i,
    output logic [31:0]  rdata_o,
    output logic         rvalid_o,
    output logic         err_o,

    // ---- five stubbed windows, exposed to the C++ harness ----
    output logic         img_req_o,
    output logic         img_we_o,
    output logic [15:0]  img_addr_o,
    output logic [31:0]  img_wdata_o,
    input  wire  [31:0]  img_rdata_i,
    input  wire          img_rvalid_i,

    output logic         dbg_req_o,
    output logic [15:0]  dbg_addr_o,
    input  wire  [31:0]  dbg_rdata_i,
    input  wire          dbg_rvalid_i,

    output logic         snap_req_o,
    output logic [15:0]  snap_addr_o,
    input  wire  [31:0]  snap_rdata_i,
    input  wire          snap_rvalid_i,

    output logic         ctrl_req_o,
    output logic         ctrl_we_o,
    output logic  [7:0]  ctrl_addr_o,
    output logic [31:0]  ctrl_wdata_o,
    input  wire  [31:0]  ctrl_rdata_i,
    input  wire          ctrl_rvalid_i,

    output logic         fw_req_o,
    output logic         fw_we_o,
    output logic [15:0]  fw_addr_o,
    output logic [31:0]  fw_wdata_o,
    input  wire  [31:0]  fw_rdata_i,
    input  wire          fw_rvalid_i,

    // ---- trace ring write side + observation ----
    input  wire          trc_wr_valid_i,
    input  wire  [127:0] trc_wr_data_i,
    output logic [15:0]  trc_wr_count_o,
    output logic         trace_req_o,
    output logic [15:0]  trace_addr_o,

    // ---- host B (EN_FW_ASSIST_P = 0, auto-acked backends) ----
    input  wire          b_req_valid_i,
    input  wire          b_we_i,
    input  wire  [19:0]  b_addr_i,
    input  wire  [31:0]  b_wdata_i,
    output logic [31:0]  b_rdata_o,
    output logic         b_rvalid_o,
    output logic         b_err_o
);

  // -------------------------------------------------- trace window glue (A)
  logic [31:0] trace_rdata_w;
  logic [31:0] ring_q_w;
  logic [15:0] count_w;
  logic        t_rv_r;
  logic        t_cnt_r;
  logic [15:0] t_cnt_snap_r;

  always_ff @(posedge clk_i) begin : t_glue
    if (!rst_n) begin
      t_rv_r       <= 1'b0;
      t_cnt_r      <= 1'b0;
      t_cnt_snap_r <= 16'h0;
    end else begin
      t_rv_r  <= trace_req_o;
      t_cnt_r <= trace_addr_o[10];
      if (trace_req_o && trace_addr_o[10]) t_cnt_snap_r <= count_w;
    end
  end

  assign trace_rdata_w  = t_cnt_r ? {16'h0, t_cnt_snap_r} : ring_q_w;
  assign trc_wr_count_o = count_w;

  KL_pp_trace_ring u_ring (
      .clk_i     (clk_i),
      .rst_n     (rst_n),
      .wr_valid_i(trc_wr_valid_i),
      .wr_data_i (trc_wr_data_i),
      .wr_count_o(count_w),
      .rd_en_i   (trace_req_o && !trace_addr_o[10]),
      .rd_addr_i (trace_addr_o[9:2]),
      .rd_lane_i (trace_addr_o[1:0]),
      .rd_data_o (ring_q_w)
  );

  KL_pp_side_port #(
      .EN_FW_ASSIST_P(1'b1)
  ) u_dut_a (
      .clk_i          (clk_i),
      .rst_n          (rst_n),
      .entity_enable_i(entity_enable_i),
      .req_valid_i    (req_valid_i),
      .we_i           (we_i),
      .addr_i         (addr_i),
      .wdata_i        (wdata_i),
      .rdata_o        (rdata_o),
      .rvalid_o       (rvalid_o),
      .err_o          (err_o),
      .img_req_o      (img_req_o),
      .img_we_o       (img_we_o),
      .img_addr_o     (img_addr_o),
      .img_wdata_o    (img_wdata_o),
      .img_rdata_i    (img_rdata_i),
      .img_rvalid_i   (img_rvalid_i),
      .dbg_req_o      (dbg_req_o),
      .dbg_addr_o     (dbg_addr_o),
      .dbg_rdata_i    (dbg_rdata_i),
      .dbg_rvalid_i   (dbg_rvalid_i),
      .snap_req_o     (snap_req_o),
      .snap_addr_o    (snap_addr_o),
      .snap_rdata_i   (snap_rdata_i),
      .snap_rvalid_i  (snap_rvalid_i),
      .ctrl_req_o     (ctrl_req_o),
      .ctrl_we_o      (ctrl_we_o),
      .ctrl_addr_o    (ctrl_addr_o),
      .ctrl_wdata_o   (ctrl_wdata_o),
      .ctrl_rdata_i   (ctrl_rdata_i),
      .ctrl_rvalid_i  (ctrl_rvalid_i),
      .trace_req_o    (trace_req_o),
      .trace_addr_o   (trace_addr_o),
      .trace_rdata_i  (trace_rdata_w),
      .trace_rvalid_i (t_rv_r),
      .fw_req_o       (fw_req_o),
      .fw_we_o        (fw_we_o),
      .fw_addr_o      (fw_addr_o),
      .fw_wdata_o     (fw_wdata_o),
      .fw_rdata_i     (fw_rdata_i),
      .fw_rvalid_i    (fw_rvalid_i)
  );

  // ------------------------------- instance B: F01.5 default, auto-acked
  logic b_img_req_w, b_dbg_req_w, b_snap_req_w, b_ctrl_req_w;
  logic b_trace_req_w, b_fw_req_w;
  logic b_ack_r;

  // sinks for instance-B outputs the harness never samples
  logic        b_img_we_w, b_ctrl_we_w, b_fw_we_w;
  logic [15:0] b_img_addr_w, b_dbg_addr_w, b_snap_addr_w;
  logic [15:0] b_trace_addr_w, b_fw_addr_w;
  logic  [7:0] b_ctrl_addr_w;
  logic [31:0] b_img_wdata_w, b_ctrl_wdata_w, b_fw_wdata_w;

  always_ff @(posedge clk_i) begin : b_auto_ack
    if (!rst_n) begin
      b_ack_r <= 1'b0;
    end else begin
      b_ack_r <= b_img_req_w | b_dbg_req_w | b_snap_req_w | b_ctrl_req_w
               | b_trace_req_w | b_fw_req_w;
    end
  end

  KL_pp_side_port #(
      .EN_FW_ASSIST_P(1'b0)
  ) u_dut_b (
      .clk_i          (clk_i),
      .rst_n          (rst_n),
      .entity_enable_i(entity_enable_i),
      .req_valid_i    (b_req_valid_i),
      .we_i           (b_we_i),
      .addr_i         (b_addr_i),
      .wdata_i        (b_wdata_i),
      .rdata_o        (b_rdata_o),
      .rvalid_o       (b_rvalid_o),
      .err_o          (b_err_o),
      .img_req_o      (b_img_req_w),
      .img_we_o       (b_img_we_w),
      .img_addr_o     (b_img_addr_w),
      .img_wdata_o    (b_img_wdata_w),
      .img_rdata_i    (32'hB0B0_B0B0),
      .img_rvalid_i   (b_ack_r),
      .dbg_req_o      (b_dbg_req_w),
      .dbg_addr_o     (b_dbg_addr_w),
      .dbg_rdata_i    (32'hB0B0_B0B0),
      .dbg_rvalid_i   (b_ack_r),
      .snap_req_o     (b_snap_req_w),
      .snap_addr_o    (b_snap_addr_w),
      .snap_rdata_i   (32'hB0B0_B0B0),
      .snap_rvalid_i  (b_ack_r),
      .ctrl_req_o     (b_ctrl_req_w),
      .ctrl_we_o      (b_ctrl_we_w),
      .ctrl_addr_o    (b_ctrl_addr_w),
      .ctrl_wdata_o   (b_ctrl_wdata_w),
      .ctrl_rdata_i   (32'hB0B0_B0B0),
      .ctrl_rvalid_i  (b_ack_r),
      .trace_req_o    (b_trace_req_w),
      .trace_addr_o   (b_trace_addr_w),
      .trace_rdata_i  (32'hB0B0_B0B0),
      .trace_rvalid_i (b_ack_r),
      .fw_req_o       (b_fw_req_w),
      .fw_we_o        (b_fw_we_w),
      .fw_addr_o      (b_fw_addr_w),
      .fw_wdata_o     (b_fw_wdata_w),
      .fw_rdata_i     (32'hB0B0_B0B0),
      .fw_rvalid_i    (b_ack_r)
  );

endmodule

`default_nettype wire
