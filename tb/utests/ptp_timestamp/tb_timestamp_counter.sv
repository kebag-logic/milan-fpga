/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

`timescale 1ns/1ps

module tb_timestamp_counter;

  //! Parameters
  parameter int COUNTER_WIDTH = 64;
  parameter int STEP_SIZE = 8;

  //! DUT signals
  logic clk;
  logic resetn;
  logic [COUNTER_WIDTH-1:0] timestamp_out;

  //! Instantiate DUT
  timestamp_counter #(
    .COUNTER_WIDTH(COUNTER_WIDTH),
    .STEP_SIZE(STEP_SIZE)
  ) dut (
    .clk(clk),
    .resetn(resetn),
    .timestamp_out(timestamp_out)
  );

  //! Clock generation
  always #4 clk = ~clk; // 125MHz clock -> 8ns period

  //! Initial conditions
  initial begin
    clk = 0;
    resetn = 0;
    #(4 * 50);
    resetn = 1;
  end

  //! Track previous value
  logic [COUNTER_WIDTH-1:0] timestamp_prev;
  always_ff @(posedge clk) begin
    timestamp_prev <= timestamp_out;
  end

  // --------------------- FORMAL ASSERTIONS ---------------------- //

  //! Assume: resetn is stable in formal mode
  always @(posedge clk) begin
    assume (resetn === 1'b0 || resetn === 1'b1);
  end

  //! Reset behavior
  property reset_behavior;
    @(posedge clk) !resetn |=> timestamp_out == 0;
  endproperty
  assert property (reset_behavior);

  //! Increment behavior
  property increment_behavior;
    @(posedge clk)
    resetn && $past(resetn) && !$past(!resetn) |=> timestamp_out == $past(timestamp_out) + STEP_SIZE;
  endproperty
  assert property (increment_behavior);

  //! Reset behavior
  property hold_during_reset;
    @(posedge clk)
    !resetn && $past(!resetn) |=> timestamp_out == 0;
  endproperty
  assert property (hold_during_reset);

  //! Fatal error if not incrementing correctly
  always @(posedge clk) begin
    if (resetn && $past(resetn)) begin
      assert (timestamp_out == $past(timestamp_out) + STEP_SIZE)
        else $fatal("Timestamp did not increment by STEP_SIZE!");
    end
  end

  //! Finish the test
  initial begin
    #(100us);
    $display("=======================================================================");
    $display("UNIT TEST COMPLETED");
    $display("All assertions executed correctly");
    $display("=======================================================================");
    $finish(0);
  end

endmodule
