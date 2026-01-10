/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : event_counter.sv
  Author      : Oguz Kahraman

                oguz.kahraman@kebag-logic.com

  Date        : 2025-08-05
  Description : Simple event counter module that increments on an `incr` pulse.
                Intended for counting Ethernet or system events in hardware.

  Company     : Kebag Logic
  Project     : Ethernet Event Counters

  Notes       :
    - Counter increments by 1 on each clock cycle where `incr` is high.
    - Global reset (`resetn`) clears the counter synchronously.
    - Optional `stats_reset` input allows clearing counters without
      affecting the rest of the system logic.
------------------------------------------------------------------------------
*/

//! This module implements a simple synchronous event counter.
//! The counter width is configurable via the `WIDTH` parameter.
//! When `incr` is high for one or more clock cycles, the counter
//! increments by 1 on each high cycle.
//!
//! Two types of reset are available:
//! - **Global reset (`resetn`)**: Clears all counters at system reset.
//! - **Stats reset (`stats_reset`)**: Clears counters without affecting
//!   the rest of the logic (useful for periodic stats collection).

`default_nettype none

module event_counter #(
  parameter int WIDTH = 32       //! Width of the counter in bits
)(
  input  wire  clk,              //! Clock signal
  input  wire  resetn,           //! Synchronous active-low global reset
  input  wire  stats_reset,      //! Counter-only reset (active high)
  input  wire  incr,             //! Increment signal
  output logic [WIDTH-1:0] count //! Current counter value 
);

always_ff @( posedge clk ) begin : count_event
  if(!resetn)begin
    count <= '0;
  end
  else if (stats_reset) begin
    count <= '0;
  end
  else if (incr)begin
    count <= count + 'd1;
  end
end

endmodule

`default_nettype wire
