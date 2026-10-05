/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_mbx_axil.sv
//  Project     : Milan FPGA Platform (packet mailbox, #665 lane F0)
//
//  Description : The mailbox's bus adapter for an AXI4-Lite host, the shape
//                a hard core (or an AXI4 interconnect's Lite port) reaches
//                the window through. One transaction at a time: a write
//                takes AW and W together, a read takes AR, each issues one
//                request on KL_mbx's host port, and B or R answers it. Every
//                response is OKAY; a write the mailbox refuses (a partial
//                WSTRB) is counted in BUS_ERR exactly as on the Wishbone
//                adapter, so the two hosts see one contract.
//
//                The one decision that matters: a write wins a cycle in
//                which both a write and a read are offered, and nothing new
//                is accepted until the previous response has been taken, so
//                the host port never sees two requests in flight.
//---------------------------------------------------------------------------//

`default_nettype none

module KL_mbx_axil
  import KL_mbx_pkg::*;
(
  input  wire                       clk_i,           //! the mailbox clock
  input  wire                       rst_n,           //! synchronous active-low reset

  input  wire                       s_awvalid_i,     //! AXI4-Lite AWVALID
  output logic                      s_awready_o,     //! AXI4-Lite AWREADY
  input  wire  [MBX_ADDR_W_C+1:0]   s_awaddr_i,      //! AXI4-Lite AWADDR, byte address inside the window
  input  wire                       s_wvalid_i,      //! AXI4-Lite WVALID
  output logic                      s_wready_o,      //! AXI4-Lite WREADY
  input  wire  [31:0]               s_wdata_i,       //! AXI4-Lite WDATA
  input  wire  [3:0]                s_wstrb_i,       //! AXI4-Lite WSTRB
  output logic                      s_bvalid_o,      //! AXI4-Lite BVALID
  input  wire                       s_bready_i,      //! AXI4-Lite BREADY
  output logic [1:0]                s_bresp_o,       //! AXI4-Lite BRESP, always OKAY
  input  wire                       s_arvalid_i,     //! AXI4-Lite ARVALID
  output logic                      s_arready_o,     //! AXI4-Lite ARREADY
  input  wire  [MBX_ADDR_W_C+1:0]   s_araddr_i,      //! AXI4-Lite ARADDR, byte address inside the window
  output logic                      s_rvalid_o,      //! AXI4-Lite RVALID
  input  wire                       s_rready_i,      //! AXI4-Lite RREADY
  output logic [31:0]               s_rdata_o,       //! AXI4-Lite RDATA
  output logic [1:0]                s_rresp_o,       //! AXI4-Lite RRESP, always OKAY

  output logic                      host_req_o,      //! KL_mbx host port: a request this cycle
  output logic                      host_we_o,       //! the request is a write
  output logic [MBX_ADDR_W_C-1:0]   host_addr_o,     //! word address inside the window
  output logic [31:0]               host_wdata_o,    //! write data
  output logic [3:0]                host_be_o,       //! byte strobes
  input  wire                       host_ack_i,      //! the request completed
  input  wire  [31:0]               host_rdata_i     //! read data, valid with host_ack_i
);

  typedef enum logic [1:0] {IDLE_S, WAIT_S, BRESP_S, RRESP_S} state_t;

  state_t      st_r;
  logic        we_r;     //! the request in flight is a write
  logic [31:0] rdata_r;  //! the read answer, held until RREADY

  logic take_w_w;   //! a write is accepted this cycle
  logic take_r_w;   //! a read is accepted this cycle
  assign take_w_w = (st_r == IDLE_S) && s_awvalid_i && s_wvalid_i;
  assign take_r_w = (st_r == IDLE_S) && !take_w_w && s_arvalid_i;

  assign s_awready_o  = take_w_w;
  assign s_wready_o   = take_w_w;
  assign s_arready_o  = take_r_w;
  assign s_bvalid_o   = (st_r == BRESP_S);
  assign s_bresp_o    = 2'b00;
  assign s_rvalid_o   = (st_r == RRESP_S);
  assign s_rdata_o    = rdata_r;
  assign s_rresp_o    = 2'b00;

  assign host_req_o   = take_w_w || take_r_w;
  assign host_we_o    = take_w_w;
  assign host_addr_o  = take_w_w ? s_awaddr_i[MBX_ADDR_W_C+1:2] : s_araddr_i[MBX_ADDR_W_C+1:2];
  assign host_wdata_o = s_wdata_i;
  assign host_be_o    = s_wstrb_i;

  always_ff @(posedge clk_i) begin : fsm
    if (!rst_n) begin
      st_r    <= IDLE_S;
      we_r    <= 1'b0;
      rdata_r <= '0;
    end else begin
      unique case (st_r)
        IDLE_S: if (host_req_o) begin
          we_r <= take_w_w;
          st_r <= WAIT_S;
        end
        WAIT_S: if (host_ack_i) begin
          rdata_r <= host_rdata_i;
          st_r    <= we_r ? BRESP_S : RRESP_S;
        end
        BRESP_S: if (s_bready_i) st_r <= IDLE_S;
        RRESP_S: if (s_rready_i) st_r <= IDLE_S;
        default: st_r <= IDLE_S;
      endcase
    end
  end : fsm

  // the byte lane of a 32-bit access is always 0: the low address bits carry nothing
  logic unused_lane_w;
  assign unused_lane_w = ^{s_awaddr_i[1:0], s_araddr_i[1:0]};

endmodule : KL_mbx_axil

`default_nettype wire
