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
//                the window through. Each of AW, W and AR is taken into a
//                one-entry slot by its own handshake, in any order and any
//                cycle; a write goes to KL_mbx's host port once its AW and
//                W slots are both full, a read once its AR slot is, one
//                request at a time, and B or R answers it and holds until
//                BREADY or RREADY. Every response is OKAY; a write the
//                mailbox refuses (a partial WSTRB) is counted in BUS_ERR
//                exactly as on the Wishbone adapter, so the two hosts see
//                one contract.
//
//                The one decision that matters: every AXI output is a
//                register or a function of registers only. A READY is the
//                emptiness of its slot, never a function of a VALID, so no
//                path runs from an input to an output (AMBA AXI, IHI0022H,
//                A3.1.1 and A3.2.1). A write goes first when a write and a
//                read both wait; the cycle after it its B slot is full, so a
//                waiting read goes next and neither starves the other.
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

  logic                    aw_full_r;  //! an AW is held: its W or its turn is awaited
  logic [MBX_ADDR_W_C-1:0] aw_addr_r;  //! the held write's word address
  logic                    w_full_r;   //! a W is held
  logic [31:0]             w_data_r;   //! the held write's data
  logic [3:0]              w_strb_r;   //! the held write's strobes
  logic                    ar_full_r;  //! an AR is held
  logic [MBX_ADDR_W_C-1:0] ar_addr_r;  //! the held read's word address
  logic                    busy_r;     //! a request is on the host port, its ack not seen
  logic                    busy_we_r;  //! that request is a write
  logic                    bvalid_r;   //! the write response, held until BREADY
  logic                    rvalid_r;   //! the read response, held until RREADY
  logic [31:0]             rdata_r;    //! the read answer, held with RVALID

  logic wr_ok_w;   //! a whole write waits and its B slot is free
  logic rd_ok_w;   //! a read waits and its R slot is free
  logic go_wr_w;   //! the write goes to the host port this cycle
  logic go_rd_w;   //! the read goes to the host port this cycle
  assign wr_ok_w = aw_full_r && w_full_r && !bvalid_r && !busy_r;
  assign rd_ok_w = ar_full_r && !rvalid_r && !busy_r;
  assign go_wr_w = wr_ok_w;
  assign go_rd_w = rd_ok_w && !wr_ok_w;

  assign s_awready_o  = !aw_full_r;
  assign s_wready_o   = !w_full_r;
  assign s_arready_o  = !ar_full_r;
  assign s_bvalid_o   = bvalid_r;
  assign s_bresp_o    = 2'b00;
  assign s_rvalid_o   = rvalid_r;
  assign s_rdata_o    = rdata_r;
  assign s_rresp_o    = 2'b00;

  assign host_req_o   = go_wr_w || go_rd_w;
  assign host_we_o    = go_wr_w;
  assign host_addr_o  = go_wr_w ? aw_addr_r : ar_addr_r;
  assign host_wdata_o = w_data_r;
  assign host_be_o    = w_strb_r;

  always_ff @(posedge clk_i) begin : slots
    if (!rst_n) begin
      aw_full_r <= 1'b0;
      aw_addr_r <= '0;
      w_full_r  <= 1'b0;
      w_data_r  <= '0;
      w_strb_r  <= '0;
      ar_full_r <= 1'b0;
      ar_addr_r <= '0;
    end else begin
      if (s_awvalid_i && !aw_full_r) begin
        aw_full_r <= 1'b1;
        aw_addr_r <= s_awaddr_i[MBX_ADDR_W_C+1:2];
      end else if (go_wr_w) begin
        aw_full_r <= 1'b0;
      end
      if (s_wvalid_i && !w_full_r) begin
        w_full_r <= 1'b1;
        w_data_r <= s_wdata_i;
        w_strb_r <= s_wstrb_i;
      end else if (go_wr_w) begin
        w_full_r <= 1'b0;
      end
      if (s_arvalid_i && !ar_full_r) begin
        ar_full_r <= 1'b1;
        ar_addr_r <= s_araddr_i[MBX_ADDR_W_C+1:2];
      end else if (go_rd_w) begin
        ar_full_r <= 1'b0;
      end
    end
  end : slots

  always_ff @(posedge clk_i) begin : answer
    if (!rst_n) begin
      busy_r    <= 1'b0;
      busy_we_r <= 1'b0;
      bvalid_r  <= 1'b0;
      rvalid_r  <= 1'b0;
      rdata_r   <= '0;
    end else begin
      if (host_req_o) begin
        busy_r    <= 1'b1;
        busy_we_r <= go_wr_w;
      end else if (host_ack_i) begin
        busy_r <= 1'b0;
      end
      if (busy_r && host_ack_i && busy_we_r) bvalid_r <= 1'b1;
      else if (s_bready_i) bvalid_r <= 1'b0;
      if (busy_r && host_ack_i && !busy_we_r) begin
        rvalid_r <= 1'b1;
        rdata_r  <= host_rdata_i;
      end else if (s_rready_i) begin
        rvalid_r <= 1'b0;
      end
    end
  end : answer

  // the byte lane of a 32-bit access is always 0: the low address bits carry nothing
  logic unused_lane_w;
  assign unused_lane_w = ^{s_awaddr_i[1:0], s_araddr_i[1:0]};

endmodule : KL_mbx_axil

`default_nettype wire
