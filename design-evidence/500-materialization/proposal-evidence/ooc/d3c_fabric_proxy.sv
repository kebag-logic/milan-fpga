/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : d3c_fabric_proxy.sv   (COST PROXY, design evidence #500)
//
//  Description : The FABRIC half candidate (c) cannot do without, when the
//                firmware writer materializes the records itself from values
//                it reads over CSRs. It is a FLOOR, not a design:
//                  * per-record change tracking the firmware can snapshot and
//                    retire without losing a change that lands between its
//                    read and its clear (SNAP moves the pending bits into a
//                    snapshot, a change on the same edge stays pending; DONE
//                    retires the snapshot; FAIL hands it back);
//                  * a read window over the dynamic-state rows, which the
//                    processor would export (today only some are exported);
//                  * a CSR-to-state-bus bridge for the name table and for the
//                    restore writes, with the same dispatch hold-off as (b):
//                    one access at a time, only while no program runs.
//                The firmware half (record encoding, the per-group value
//                judgement, the map coupling rules) is not in this module.
//---------------------------------------------------------------------------//
`default_nettype none

module d3c_fabric_proxy #(
    parameter int unsigned N_STREAM_IN_P  = 2,
    parameter int unsigned N_STREAM_OUT_P = 2,
    parameter int unsigned N_SPORT_IN_P   = 1,
    parameter int unsigned N_SPORT_OUT_P  = 1,
    parameter int unsigned N_NAME_P       = 38
) (
    input  wire         clk_i,
    input  wire         rst_n,
    //! change sources (the same decode as candidate (b))
    input  wire         u_dyn_ack_i,
    input  wire         u_name_ack_i,
    input  wire  [19:0] u_addr_i,
    input  wire  [15:0] u_didx_i,
    input  wire         me_stb_i,
    input  wire  [15:0] me_type_i,
    input  wire  [15:0] me_idx_i,
    //! the dynamic-state rows, exported by the processor
    input  wire  [15:0] cfg_i,
    input  wire  [31:0] rate_i,
    input  wire  [15:0] clks_i,
    input  wire  [N_STREAM_IN_P*64-1:0]  fmt_in_i,
    input  wire  [N_STREAM_OUT_P*64-1:0] fmt_out_i,
    input  wire  [N_STREAM_OUT_P*32-1:0] ptof_i,
    //! the state bus, shared with the uCPU while no program runs
    input  wire         prog_busy_i,
    output logic        own_o,
    output logic        sb_req_o,
    output logic        sb_we_o,
    output logic        sb_name_o,
    output logic [19:0] sb_addr_o,
    output logic [63:0] sb_wdata_o,
    output logic [15:0] sb_didx_o,
    input  wire         sb_ready_i,
    input  wire         sb_rvalid_i,
    input  wire  [63:0] sb_rdata_i,
    //! the firmware's CSR face
    input  wire         csr_sel_i,
    input  wire         csr_we_i,
    input  wire  [7:0]  csr_addr_i,
    input  wire  [31:0] csr_wdata_i,
    output logic [31:0] csr_rdata_o
);
  localparam int unsigned N_SO_C  = N_STREAM_OUT_P;
  localparam int unsigned N_REC_C = 3 + N_STREAM_IN_P + 2 * N_SO_C + N_SPORT_IN_P
                                  + N_SPORT_OUT_P + N_NAME_P;
  localparam int unsigned N_WRD_C = (N_REC_C + 31) / 32;
  localparam int unsigned S_FMTI_C = 3, S_FMTO_C = S_FMTI_C + N_STREAM_IN_P;
  localparam int unsigned S_PTOF_C = S_FMTO_C + N_SO_C, S_MAPI_C = S_PTOF_C + N_SO_C;
  localparam int unsigned S_MAPO_C = S_MAPI_C + N_SPORT_IN_P, S_NAME_C = S_MAPO_C + N_SPORT_OUT_P;

  // ---- change decode ---------------------------------------------------------
  logic [N_REC_C-1:0] set_w;
  logic               dyn_w;
  logic [12:0]        sel_w;
  assign dyn_w = u_dyn_ack_i && (u_addr_i[19:16] == 4'h1);
  assign sel_w = u_addr_i[15:3];
  assign set_w[0] = dyn_w && (sel_w == 13'd0);
  assign set_w[1] = dyn_w && (sel_w == 13'd1) && (u_didx_i == 16'd0);
  assign set_w[2] = dyn_w && (sel_w == 13'd2) && (u_didx_i == 16'd0);
  for (genvar i = 0; i < N_STREAM_IN_P; i++) begin : g_fi
    assign set_w[S_FMTI_C + i] = dyn_w && (sel_w == 13'd3) && (u_didx_i == 16'(i));
  end
  for (genvar i = 0; i < N_SO_C; i++) begin : g_fo
    assign set_w[S_FMTO_C + i] = dyn_w && (sel_w == 13'd4) && (u_didx_i == 16'(i));
    assign set_w[S_PTOF_C + i] = dyn_w && (sel_w == 13'd5) && (u_didx_i == 16'(i));
  end
  for (genvar i = 0; i < N_SPORT_IN_P; i++) begin : g_mi
    assign set_w[S_MAPI_C + i] = me_stb_i && (me_type_i == 16'h000E) && (me_idx_i == 16'(i));
  end
  for (genvar i = 0; i < N_SPORT_OUT_P; i++) begin : g_mo
    assign set_w[S_MAPO_C + i] = me_stb_i && (me_type_i == 16'h000F) && (me_idx_i == 16'(i));
  end
  for (genvar i = 0; i < N_NAME_P; i++) begin : g_nm
    assign set_w[S_NAME_C + i] = u_name_ack_i && (u_addr_i[15:6] == 10'(i));
  end

  // ---- the snapshot handshake ------------------------------------------------
  logic [N_REC_C-1:0] chg_r, snap_r;
  logic               snap_w, done_w, fail_w;
  assign snap_w = csr_sel_i && csr_we_i && (csr_addr_i == 8'h00) && csr_wdata_i[0];
  assign done_w = csr_sel_i && csr_we_i && (csr_addr_i == 8'h00) && csr_wdata_i[1];
  assign fail_w = csr_sel_i && csr_we_i && (csr_addr_i == 8'h00) && csr_wdata_i[2];
  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      chg_r  <= '0;
      snap_r <= '0;
    end else begin
      chg_r  <= set_w | (snap_w ? '0 : fail_w ? (chg_r | snap_r) : chg_r);
      snap_r <= snap_w ? chg_r : (done_w || fail_w) ? '0 : snap_r;
    end
  end

  // ---- the state-bus bridge ---------------------------------------------------
  logic [19:0] b_addr_r;
  logic [63:0] b_wdata_r, b_rdata_r;
  logic [15:0] b_didx_r;
  logic        b_go_r, b_we_r, b_name_r, b_busy_r;
  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      b_addr_r <= '0; b_wdata_r <= '0; b_rdata_r <= '0; b_didx_r <= '0;
      b_go_r <= 1'b0; b_we_r <= 1'b0; b_name_r <= 1'b0; b_busy_r <= 1'b0; own_o <= 1'b0;
    end else begin
      if (csr_sel_i && csr_we_i) begin
        unique case (csr_addr_i)
          8'h01: b_addr_r <= csr_wdata_i[19:0];
          8'h02: b_wdata_r[31:0] <= csr_wdata_i;
          8'h03: b_wdata_r[63:32] <= csr_wdata_i;
          8'h04: b_didx_r <= csr_wdata_i[15:0];
          8'h05: begin b_go_r <= 1'b1; b_we_r <= csr_wdata_i[0]; b_name_r <= csr_wdata_i[1]; end
          default: ;
        endcase
      end
      if (b_go_r && !b_busy_r && !prog_busy_i) begin
        own_o <= 1'b1; b_busy_r <= 1'b1; b_go_r <= 1'b0;
      end else if (b_busy_r && (b_we_r ? sb_ready_i : sb_rvalid_i)) begin
        if (!b_we_r) b_rdata_r <= sb_rdata_i;
        own_o <= 1'b0; b_busy_r <= 1'b0;
      end
    end
  end
  assign sb_req_o   = b_busy_r;
  assign sb_we_o    = b_we_r;
  assign sb_name_o  = b_name_r;
  assign sb_addr_o  = b_addr_r;
  assign sb_wdata_o = b_wdata_r;
  assign sb_didx_o  = b_didx_r;

  // ---- the read window ------------------------------------------------------------
  //! words 0x10.. the pending vector, 0x20.. the snapshot, 0x40.. the rows
  localparam int unsigned N_ROW_C = 3 + N_STREAM_IN_P + 2 * N_SO_C;
  logic [63:0] row_w [N_ROW_C];
  always_comb begin
    row_w[0] = {48'd0, cfg_i};
    row_w[1] = {32'd0, rate_i};
    row_w[2] = {48'd0, clks_i};
    for (int i = 0; i < N_STREAM_IN_P; i++) row_w[S_FMTI_C + i] = fmt_in_i[64*i +: 64];
    for (int i = 0; i < N_SO_C; i++) begin
      row_w[S_FMTO_C + i] = fmt_out_i[64*i +: 64];
      row_w[S_PTOF_C + i] = {32'd0, ptof_i[32*i +: 32]};
    end
  end
  logic [N_WRD_C*32-1:0] chg_x_w, snap_x_w;
  assign chg_x_w  = (N_WRD_C*32)'(chg_r | snap_r);
  assign snap_x_w = (N_WRD_C*32)'(snap_r);
  always_comb begin
    csr_rdata_o = 32'd0;
    if (csr_addr_i == 8'h06)      csr_rdata_o = {30'd0, own_o, b_busy_r};
    else if (csr_addr_i == 8'h07) csr_rdata_o = b_rdata_r[31:0];
    else if (csr_addr_i == 8'h08) csr_rdata_o = b_rdata_r[63:32];
    else if ((csr_addr_i >= 8'h10) && (32'(csr_addr_i) < 32'h10 + N_WRD_C))
      csr_rdata_o = chg_x_w[32 * (32'(csr_addr_i) - 32'h10) +: 32];
    else if ((csr_addr_i >= 8'h20) && (32'(csr_addr_i) < 32'h20 + N_WRD_C))
      csr_rdata_o = snap_x_w[32 * (32'(csr_addr_i) - 32'h20) +: 32];
    else if ((csr_addr_i >= 8'h40) && (32'(csr_addr_i) < 32'h40 + 2 * N_ROW_C))
      csr_rdata_o = row_w[(32'(csr_addr_i) - 32'h40) / 2][32 * (32'(csr_addr_i) % 2) +: 32];
  end

  logic unused_ok_w;
  assign unused_ok_w = ^{u_addr_i[2:0], sb_rdata_i};
endmodule

`default_nettype wire
