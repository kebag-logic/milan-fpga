/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_mbx_wb.sv
//  Project     : Milan FPGA Platform (packet mailbox, #665 lane F0)
//
//  Description : The mailbox's bus adapter for a classic Wishbone host (the
//                LiteX SoC bus of the on-chip RISC-V). One transfer at a
//                time: a cycle with CYC and STB high issues one request on
//                KL_mbx's host port, and ACK follows the port's answer one
//                cycle later. The address is a word address and only its
//                low MBX_ADDR_W_C bits reach the mailbox; the SoC maps the
//                window at a base aligned to its size.
//
//                The one decision that matters: the adapter adds nothing to
//                the contract. 32-bit accesses, the refusal of a partial
//                byte select and every register's meaning are KL_mbx's, so
//                the AXI4-Lite adapter beside this one presents the same
//                window to a hard core.
//---------------------------------------------------------------------------//

`default_nettype none

module KL_mbx_wb
  import KL_mbx_pkg::*;
(
  input  wire                       clk_i,         //! the mailbox clock
  input  wire                       rst_n,         //! synchronous active-low reset

  input  wire                       wb_cyc_i,      //! Wishbone CYC
  input  wire                       wb_stb_i,      //! Wishbone STB
  input  wire                       wb_we_i,       //! Wishbone WE
  input  wire  [29:0]               wb_adr_i,      //! Wishbone word address
  input  wire  [31:0]               wb_dat_i,      //! Wishbone write data
  input  wire  [3:0]                wb_sel_i,      //! Wishbone byte selects
  output logic                      wb_ack_o,      //! Wishbone ACK
  output logic [31:0]               wb_dat_o,      //! Wishbone read data, valid with ACK
  output logic                      wb_err_o,      //! Wishbone ERR, never raised: a refusal is counted in BUS_ERR

  output logic                      host_req_o,    //! KL_mbx host port: a request this cycle
  output logic                      host_we_o,     //! the request is a write
  output logic [MBX_ADDR_W_C-1:0]   host_addr_o,   //! word address inside the window
  output logic [31:0]               host_wdata_o,  //! write data
  output logic [3:0]                host_be_o,     //! byte strobes
  input  wire                       host_ack_i,    //! the request completed
  input  wire  [31:0]               host_rdata_i   //! read data, valid with host_ack_i
);

  logic busy_r;   //! a request is in flight; its ACK has not been given

  assign host_req_o   = wb_cyc_i && wb_stb_i && !busy_r;
  assign host_we_o    = wb_we_i;
  assign host_addr_o  = wb_adr_i[MBX_ADDR_W_C-1:0];
  assign host_wdata_o = wb_dat_i;
  assign host_be_o    = wb_sel_i;
  assign wb_ack_o     = busy_r && host_ack_i;
  assign wb_dat_o     = host_rdata_i;
  assign wb_err_o     = 1'b0;

  always_ff @(posedge clk_i) begin : track
    if (!rst_n) busy_r <= 1'b0;
    else if (host_req_o) busy_r <= 1'b1;
    else if (host_ack_i) busy_r <= 1'b0;
  end : track

  // the address bits above the window are the SoC decoder's, not the mailbox's
  logic unused_adr_w;
  assign unused_adr_w = ^wb_adr_i[29:MBX_ADDR_W_C];

endmodule : KL_mbx_wb

`default_nettype wire
