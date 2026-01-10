/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : timestamp_counter.sv
  Author      : Oguz Kahraman

                oguz.kahraman@kebag-logic.com

  Date        : 2025-07-12
  Description : Global nanosecond-resolution timestamp counter used for
                PTP hardware timestamping. The counter increments at a
                configurable step size on each clock cycle and can be shared
                across TX/RX timestamping blocks.

  Company     : Kebag Logic
  Project     : PTP Timestamping for Custom RGMII MAC

------------------------------------------------------------------------------
*/

`default_nettype none

module timestamp_counter #(
  parameter int COUNTER_WIDTH = 64, //! Width of the counter
  parameter int STEP_SIZE = 8 //! Step size per clock cycle (e.g., 8 for 125 MHz = 8 ns resolution).
)(
  input wire clk, //! src clock input
  input wire resetn, //! Active low synchronous reset

  output wire [COUNTER_WIDTH-1:0] timestamp_out //! Current timestamp output (nanoseconds).
);

//! Internal counter register
logic [COUNTER_WIDTH-1:0] timestamp;

//! Assign output.
assign timestamp_out = timestamp;

//! Timestamp coutner logic: increment on each clock cycle and overflows.
always_ff @(posedge clk ) begin : timestamp_counter
  if(!resetn)begin
    timestamp <= 'd0;
  end
  else begin
    timestamp <= timestamp + STEP_SIZE;
  end
end

endmodule

`default_nettype wire
