/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

interface axi_stream_if #(
  parameter TDATA_WIDTH_P = 32,
  parameter TID_WIDTH_P = 1,
  parameter TDEST_WIDTH_P = 1,
  parameter TUSER_WIDTH_P = 1
  )
  (
    input bit clk,
    input bit rst_n
  );

  clocking 
    cb @(posedge clk);
  endclocking : cb

  logic tready;
  logic tvalid;
  logic tlast;
  logic [TDATA_WIDTH_P - 1 : 0] tdata;
  logic [TDATA_WIDTH_P/8 - 1 : 0] tkeep;
  logic [TDATA_WIDTH_P/8 - 1 : 0] tstrb;
  logic [TID_WIDTH_P - 1 : 0] tid;
  logic [TDEST_WIDTH_P - 1 : 0] tdest;
  logic [TUSER_WIDTH_P - 1 : 0] tuser;

  modport master (input tready, output tvalid, tlast, tdata, tid, tstrb, tdest, tuser, tkeep);
  modport slave (input tvalid, tlast, tdata, tid, tstrb, tdest, tuser, tkeep, output tready);

endinterface : axi_stream_if