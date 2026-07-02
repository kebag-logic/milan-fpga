/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : timestamp_counter.sv
  Author      : Oguz Kahraman / Kebag Logic

  Date        : 2025-07-12 (PHC rework 2026-07-01)
  Description : Register-controlled nanosecond timestamp counter for the PTP
                hardware clock (PHC). Replaces the fixed "+STEP_SIZE" counter
                with a fractional-nanosecond phase accumulator so software can
                discipline the clock rate and time (REQ-PTP-01..03):

                  * rate    (adjfine): each tick adds (incr_i + adj_i), both in
                    Q(INT).(FRAC_WIDTH) nanoseconds. incr_i is the nominal
                    per-tick step (e.g. 8.0 ns at 125 MHz); adj_i is the signed
                    fine-frequency addend written by ptp adjfine().
                  * settime (adjtime abs): cmd_load_i loads tod_wr_i into the
                    integer-ns field and clears the fraction.
                  * adjtime (offset): cmd_adjust_i adds the signed offset_i (ns)
                    to the integer-ns field on top of the normal tick.
                  * gettime: cmd_snapshot_i latches the current integer-ns value
                    into tod_snapshot_o (read back through milan_csr).

                The accumulator is {ns[COUNTER_WIDTH-1:0], frac[FRAC_WIDTH-1:0]};
                timestamp_out exposes the integer-ns field for TX/RX capture.
                All control inputs are expected to be already synchronised into
                this clock domain (see ptp_csr_sync); this block is single-clock
                and therefore directly unit-testable in Verilator.

  Company     : Kebag Logic
  Project     : PTP Timestamping for Custom RGMII MAC
------------------------------------------------------------------------------
*/

`default_nettype none

module timestamp_counter #(
  parameter int COUNTER_WIDTH = 64, //! Width of the integer-nanosecond field
  parameter int INCR_WIDTH    = 32, //! Width of the per-tick increment/addend
  parameter int FRAC_WIDTH    = 24  //! Fractional-nanosecond bits: PTP_INCR is Q8.24 (8 int ns + 24 frac)
)(
  input  wire clk,                              //! PHC clock (fixed 125 MHz source recommended, REQ-PTP-07)
  input  wire resetn,                           //! Active-low synchronous reset

  input  wire enable_i,                         //! 1 = counter runs; 0 = hold (rate updates paused)
  input  wire [INCR_WIDTH-1:0]        incr_i,   //! Nominal per-tick increment, Q(INT).FRAC ns
  input  wire signed [INCR_WIDTH-1:0] adj_i,    //! Signed adjfine addend, Q(INT).FRAC ns
  input  wire [COUNTER_WIDTH-1:0]     tod_wr_i, //! settime target time-of-day, ns
  input  wire                         cmd_load_i,   //! settime apply strobe (1 cycle, this domain)
  input  wire signed [COUNTER_WIDTH-1:0] offset_i,  //! adjtime signed delta, ns
  input  wire                         cmd_adjust_i, //! adjtime apply strobe (1 cycle)
  input  wire                         cmd_snapshot_i,//! gettime latch strobe (1 cycle)

  output wire [COUNTER_WIDTH-1:0] timestamp_out,      //! Live integer-ns time (for packet capture)
  output wire [COUNTER_WIDTH-1:0] tod_snapshot_o,     //! Integer-ns value latched on snapshot
  output wire                     tod_snapshot_valid_o //! 1-cycle pulse when a snapshot is latched
);

  localparam int ACC_WIDTH = COUNTER_WIDTH + FRAC_WIDTH;

  //! Phase accumulator: high COUNTER_WIDTH bits are integer ns, low FRAC_WIDTH are the fraction.
  logic [ACC_WIDTH-1:0] acc;
  //! Latched integer-ns snapshot for gettime.
  logic [COUNTER_WIDTH-1:0] tod_snapshot;
  //! Snapshot-valid pulse.
  logic tod_snapshot_valid;

  //! Per-tick signed step = nominal increment + adjfine addend (Q.FRAC ns).
  //! Sign-extended to the accumulator width before the add.
  wire signed [ACC_WIDTH-1:0] tick_step =
      ACC_WIDTH'($signed({1'b0, incr_i})) + ACC_WIDTH'($signed(adj_i));

  //! adjtime offset promoted to accumulator units (ns shifted into integer field).
  wire signed [ACC_WIDTH-1:0] offset_acc =
      ACC_WIDTH'($signed(offset_i)) <<< FRAC_WIDTH;

  assign timestamp_out        = acc[ACC_WIDTH-1 -: COUNTER_WIDTH];
  assign tod_snapshot_o       = tod_snapshot;
  assign tod_snapshot_valid_o = tod_snapshot_valid;

  //! Time-of-day accumulator with settime/adjtime/rate control.
  always_ff @(posedge clk) begin : tod_accumulator
    if (!resetn) begin
      acc <= '0;
    end
    else if (cmd_load_i) begin
      //! settime: load integer ns, clear fraction (absolute set wins over ticking)
      acc <= {tod_wr_i, {FRAC_WIDTH{1'b0}}};
    end
    else begin
      //! normal rate tick (when enabled), plus optional one-shot adjtime offset
      logic signed [ACC_WIDTH-1:0] next;
      next = $signed(acc);
      if (enable_i)     next = next + tick_step;
      if (cmd_adjust_i) next = next + offset_acc;
      acc <= next;
    end
  end

  //! gettime snapshot latch.
  always_ff @(posedge clk) begin : snapshot_latch
    if (!resetn) begin
      tod_snapshot       <= '0;
      tod_snapshot_valid <= 1'b0;
    end
    else begin
      tod_snapshot_valid <= cmd_snapshot_i;
      if (cmd_snapshot_i)
        tod_snapshot <= acc[ACC_WIDTH-1 -: COUNTER_WIDTH];
    end
  end

endmodule

`default_nettype wire
