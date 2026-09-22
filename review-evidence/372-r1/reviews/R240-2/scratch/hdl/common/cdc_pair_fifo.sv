/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : cdc_pair_fifo.sv
  Author      : Kebag Logic

  Date        : 2026-07-18
  Description : Small dual-clock FIFO (gray-coded pointers, 2-FF sync) for
                the audio sample-pair path: the 48 kHz stream crosses from
                cd_milan into the clean MMCM audio domain here. Depth is a
                power of two; wr side never writes full, rd side never reads
                empty (callers gate). Device-portable - no vendor prims.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! Gray-pointer dual-clock FIFO, WIDTH x 2^LOG2D. Flags are conservative
//! (synchronizer latency) which only costs a couple of entries of headroom.

`default_nettype none

module cdc_pair_fifo #(
  parameter int WIDTH = 48,   //! payload width (a stereo 24-bit pair)
  parameter int LOG2D = 4     //! depth = 2^LOG2D entries
)(
  input  wire              wclk_i,    //! write clock (producer domain)
  input  wire              wrst_n,    //! write-side sync reset (active low)
  input  wire              wen_i,     //! write enable (qualified by !wfull_o)
  input  wire [WIDTH-1:0]  wdata_i,   //! write data
  output logic             wfull_o,   //! FIFO full (write side view)

  input  wire              rclk_i,    //! read clock (consumer domain)
  input  wire              rrst_n,    //! read-side sync reset (active low)
  input  wire              ren_i,     //! read enable (qualified by !rempty_o)
  output logic [WIDTH-1:0] rdata_o,   //! read data (registered)
  output logic             rempty_o   //! FIFO empty (read side view)
);

  localparam int PW = LOG2D + 1;      //! pointer width (wrap bit)

  logic [WIDTH-1:0] mem_r [0:(1<<LOG2D)-1];

  //! binary + gray pointers, each owned by its side
  logic [PW-1:0] wptr_bin_r, wptr_gray_r;
  logic [PW-1:0] rptr_bin_r, rptr_gray_r;
  //! cross-domain synchronizers (2-FF)
  logic [PW-1:0] rgray_w1_r, rgray_w2_r;   //! rptr gray into wclk
  logic [PW-1:0] wgray_r1_r, wgray_r2_r;   //! wptr gray into rclk

  function automatic [PW-1:0] bin2gray(input [PW-1:0] b);
    bin2gray = b ^ (b >> 1);
  endfunction

  // ---- write side -------------------------------------------------------
  wire [PW-1:0] wptr_bin_n  = wptr_bin_r + PW'(wen_i && !wfull_o);
  wire [PW-1:0] wptr_gray_n = bin2gray(wptr_bin_n);

  always_ff @(posedge wclk_i) begin : wr_side
    if (!wrst_n) begin
      wptr_bin_r  <= '0;
      wptr_gray_r <= '0;
      rgray_w1_r  <= '0;
      rgray_w2_r  <= '0;
      wfull_o     <= 1'b0;
    end
    else begin
      if (wen_i && !wfull_o)
        mem_r[wptr_bin_r[LOG2D-1:0]] <= wdata_i;
      wptr_bin_r  <= wptr_bin_n;
      wptr_gray_r <= wptr_gray_n;
      {rgray_w2_r, rgray_w1_r} <= {rgray_w1_r, rptr_gray_r};
      //! full: next wptr gray == read gray with the top two bits inverted
      wfull_o <= (wptr_gray_n ==
                  {~rgray_w2_r[PW-1:PW-2], rgray_w2_r[PW-3:0]});
    end
  end : wr_side

  // ---- read side --------------------------------------------------------
  wire [PW-1:0] rptr_bin_n  = rptr_bin_r + PW'(ren_i && !rempty_o);
  wire [PW-1:0] rptr_gray_n = bin2gray(rptr_bin_n);

  always_ff @(posedge rclk_i) begin : rd_side
    if (!rrst_n) begin
      rptr_bin_r  <= '0;
      rptr_gray_r <= '0;
      wgray_r1_r  <= '0;
      wgray_r2_r  <= '0;
      rempty_o    <= 1'b1;
      rdata_o     <= '0;
    end
    else begin
      if (ren_i && !rempty_o)
        rdata_o <= mem_r[rptr_bin_r[LOG2D-1:0]];
      rptr_bin_r  <= rptr_bin_n;
      rptr_gray_r <= rptr_gray_n;
      {wgray_r2_r, wgray_r1_r} <= {wgray_r1_r, wptr_gray_r};
      rempty_o <= (rptr_gray_n == wgray_r2_r);
    end
  end : rd_side

endmodule

`default_nettype wire
