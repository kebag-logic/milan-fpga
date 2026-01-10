/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : ethernet_events.sv
  Author      : Oguz Kahraman

                oguz.kahraman@kebag-logic.com

  Date        : 2025-08-05
  Description : Top-level Ethernet event counter aggregator. Instantiates one
                `event_counter` module per defined Ethernet event type and
                maintains individual counters for debug and monitoring.

  Company     : Kebag Logic
  Project     : Ethernet Event Counters

  Notes       :
    - Each counter increments when its corresponding event pulse is high.
    - Event definitions are provided in `ethernet_events.svh`.
    - Counters are exposed as `mark_debug` signals for Vivado ILA/VIO monitoring.
    - All counters are cleared on global synchronous reset (`resetn`).
------------------------------------------------------------------------------
*/

//! This module instantiates multiple `event_counter` modules, one for each
//! Ethernet event defined in `ethernet_events.svh`. Event pulses are fed
//! into each counter, and the resulting values are assigned to individually
//! named debug registers.
//!
//! **Key Features**
//! - Parameterizable counter width (`WIDTH`).
//! - All counters reset synchronously when `resetn` is low.
`default_nettype none

`include "ethernet_events.svh"

module ethernet_events #(
  parameter int WIDTH = 32                      //! Width of the counter in bits
)(
  input  wire  clk,                             //! Clock signal
  input  wire  resetn,                          //! Synchronous active-low global reset
  input  wire  stats_reset,                     //! 1-bit reset for all stats
  input  wire  [_ETH_EVENT_COUNTER-1:0] events  //! Event pulses
);

//! counter values
logic [WIDTH-1:0] counters [_ETH_EVENT_COUNTER];

//! Debug purpose
(* mark_debug = "true" *) logic [WIDTH-1:0] tx_error_underflow_cnt = '0;
(* mark_debug = "true" *) logic [WIDTH-1:0] tx_fifo_overflow_cnt = '0;
(* mark_debug = "true" *) logic [WIDTH-1:0] tx_fifo_bad_frame_cnt = '0;
(* mark_debug = "true" *) logic [WIDTH-1:0] tx_fifo_good_frame_cnt = '0;
(* mark_debug = "true" *) logic [WIDTH-1:0] rx_error_bad_frame_cnt = '0;
(* mark_debug = "true" *) logic [WIDTH-1:0] rx_error_bad_fcs_cnt = '0;
(* mark_debug = "true" *) logic [WIDTH-1:0] rx_fifo_overflow_cnt = '0;
(* mark_debug = "true" *) logic [WIDTH-1:0] rx_fifo_bad_frame_cnt = '0;
(* mark_debug = "true" *) logic [WIDTH-1:0] rx_fifo_good_frame_cnt = '0;

genvar i;
generate
  for(i=0; i < _ETH_EVENT_COUNTER; i++) begin : event_counter_gen
    event_counter #(
      .WIDTH(WIDTH)
    ) counter_inst(
      .clk(clk),
      .resetn(resetn),
      .stats_reset(stats_reset),
      .incr(events[i]),
      .count(counters[i])
    );
  end
endgenerate

always_ff @( posedge clk ) begin : counter_assignment
  tx_error_underflow_cnt <= counters[TX_ERROR_UNDERFLOW];
  tx_fifo_overflow_cnt <= counters[TX_FIFO_OVERFLOW];
  tx_fifo_bad_frame_cnt <= counters[TX_FIFO_BAD_FRAME];
  tx_fifo_good_frame_cnt <= counters[TX_FIFO_GOOD_FRAME];
  rx_error_bad_frame_cnt <= counters[RX_ERROR_BAD_FRAME];
  rx_error_bad_fcs_cnt <= counters[RX_ERROR_BAD_FCS];
  rx_fifo_overflow_cnt <= counters[RX_FIFO_OVERFLOW];
  rx_fifo_bad_frame_cnt <= counters[RX_FIFO_BAD_FRAME];
  rx_fifo_good_frame_cnt <= counters[RX_FIFO_GOOD_FRAME];
end

endmodule //! ethernet_events

`default_nettype wire
