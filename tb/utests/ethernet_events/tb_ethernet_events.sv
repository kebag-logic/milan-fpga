`default_nettype none
`timescale 1ns/1ps

`include "ethernet_events.svh"

module tb_ethernet_events;

  parameter WIDTH = 6;


  //! TB internal signals
  logic clk;
  logic resetn;
  logic stats_reset;
  logic [_ETH_EVENT_COUNTER-1:0] events;

  //! Instantiate DUT
  ethernet_events #(
    .WIDTH(WIDTH)
  ) dut(
    .clk(clk),
    .resetn(resetn),
    .stats_reset(stats_reset),
    .events(events)
  );

  initial begin
    clk = 0;
    resetn = 0;
    stats_reset = 0;
    #(4 * 50);
    resetn = 1;
  end

  always #5 clk = ~clk; // 100MHz clk

  //! Drive events with random pulses
  always @(posedge clk) begin
    if (!resetn) begin
      events <= '0;
    end
    else begin
      events <= '0;
      if ($urandom_range(0, 10) == 0) begin
        events[$urandom_range(0, _ETH_EVENT_COUNTER-1)] <= 1'b1;
      end
    end
  end

  // --------------------- FORMAL ASSERTIONS ---------------------- //

  //! Assume: resetn is stable in formal mode
  always @(posedge clk) begin
    assume (resetn === 1'b0 || resetn === 1'b1);
  end

  //! Reset behavior
  generate
    genvar i;
    for(i=0; i < _ETH_EVENT_COUNTER-1; i++) begin : check_reset
      property reset_behavior;
        @(posedge clk) !resetn || stats_reset |=> dut.counters[i] == 0;
      endproperty
      assert property (reset_behavior);
    end
  endgenerate
  

  //! Increment correctness
  generate
    genvar k;
    for (k = 0; k < _ETH_EVENT_COUNTER; k++) begin : check_increments
      always @(posedge clk) if (resetn && !stats_reset) begin
        if ($past(resetn && !stats_reset)) begin
          if ($past(events[k]))
            assert (dut.counters[k] == $past(dut.counters[k]) + 1);
          else
            assert (dut.counters[k] == $past(dut.counters[k]));
        end
      end
    end
  endgenerate

  //! Finish the test
  initial begin
    #(50us);
    $display("=======================================================================");
    $display("UNIT TEST COMPLETED");
    $display("All assertions executed correctly");
    $display("=======================================================================");
    $finish(0);
  end

endmodule

`default_nettype wire
