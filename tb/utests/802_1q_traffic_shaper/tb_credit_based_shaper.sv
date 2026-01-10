/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

`timescale 1ns/1ps
import ethernet_packet_pkg::*;

`include "parameters.svh"

module tb_credit_based_shaper;
  //! Local parameters
  localparam CLK_FREQ_HZ = 125_000_000;
  localparam int TICK_NS = 8;

  //! Clock and async reset signals
  logic clk = 0;
  logic resetn = 0;
  //! DUT internal signals
  logic queue_has_data = 1;
  logic is_transmitting;
  logic [15:0] bytes_sent;
  wire allow_transmit;

  //! Clock generation
  always #(TICK_NS/2) clk = ~clk;

  //! DUT instantiation with parameters
  credit_based_shaper #(
    .IDLE_SLOPE_1G(750_000_000),
    .IDLE_SLOPE_100M(75_000_000),
    .HI_CREDIT(1536),
    .LO_CREDIT(-1536),
    .CLK_FREQ_HZ(CLK_FREQ_HZ)
  ) dut (
    .clk(clk),
    .resetn(resetn),
    .queue_has_data_i(queue_has_data),
    .is_1g_i('d1),
    .is_transmitting_i(is_transmitting),
    .bytes_sent_i(bytes_sent),
    .allow_transmit_o(allow_transmit)
  );

  initial begin
    //! Reset generation
    is_transmitting = 0;
    bytes_sent = 0;
    resetn = 0;
    repeat (3) @(posedge clk);
    resetn = 1;

    //! 1000 clk cycle idle time - credit should increase
    $display("[TEST] Credit accumulation in idle");
    repeat (1000) @(posedge clk);  // simulate idle

    //! Start transmission - credit should decrease
    $display("[TEST] Begin transmission");
    is_transmitting = 1;
    bytes_sent = 8;
    repeat (400) @(posedge clk);

    is_transmitting = 0;
    bytes_sent = 0;

    //! Based-on this scnario credit should be negative therfore no transmission should not be
    //! allowed.
    $display("[TEST] Final transmit check: %0d", allow_transmit);
    if (!allow_transmit)
      $display("[PASS] Transmit allowed at end");
    else
      $fatal("[FAIL] Transmit allowed unexpectedly");

    $finish;
  end
endmodule
