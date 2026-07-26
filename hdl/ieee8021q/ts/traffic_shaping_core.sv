/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : traffic_shaping_core.sv
  Author      : Oguz Kahraman / Kebag Logic

  Date        : 2025-07-05 (runtime-config rework 2026-07-01)
  Description : Top-level module for IEEE 802.1Qav Credit-Based Traffic Shaping.
                Implements multi-queue arbitration using per-queue CBS instances.

                - Each queue is monitored for data availability and credit level.
                - Only one queue is granted for transmission at a time.
                - Grants are held until the end of a packet (`tlast`).
                - Transmission eligibility is driven by credit logic (CBS).

                Runtime configuration (REQ-CBS-01/02): the per-queue idleSlope,
                hiCredit, loCredit and shaped-enable arrive packed from milan_csr
                (o_cbs_*). Unshaped queues (shaped_i = 0) behave as strict-
                priority: their CBS forces `allow_transmit` high, so the priority
                encoder always considers them eligible when they have data.

                ARBITRATION ORDER (802.1Q, 6-queue map): the HIGHEST queue index
                wins - q5 (SR class A) over q4 (class B) over q3 (gPTP) over q2
                (control) over q1 (spare) over q0 (best effort). The shaped
                classes therefore sit at the TOP of the strict-priority order,
                which is what 802.1Q-2018 8.6.8.2 credit-based shaping assumes;
                a strict-priority queue above them would void the credit
                accounting. See ethernet_packet_pkg::priority_encode and
                docs/reference/EGRESS_QUEUE_MAP.md.

  Company     : Kebag Logic
  Project     : 802.1Q Traffic Shaper
------------------------------------------------------------------------------
*/

`include "ethernet_packet_pkg.sv"
import ethernet_packet_pkg::*;

`default_nettype none

module traffic_shaping_core #(
  parameter int TDATA_WIDTH = 64,     //! Width of tdata bus
  parameter int NUMBER_OF_QUEUES = 6  //! Number of network queues
)(
  input wire clk,                     //! clock signal
  input wire resetn,                  //! synchronous active low reset
  //! One-hot: indicates which queues contain data
  input wire [NUMBER_OF_QUEUES-1:0] queue_has_data_i,
  input wire is_1g_i,                 //! High when the link rate is 1GBps

  //! --- per-queue CBS runtime config, packed [q*32 +: 32] (from milan_csr) ---
  input wire [32*NUMBER_OF_QUEUES-1:0] cbs_idle_slope_i, //! idleSlope per queue, bits/s
  input wire [32*NUMBER_OF_QUEUES-1:0] cbs_hi_credit_i,  //! hiCredit per queue, signed bytes
  input wire [32*NUMBER_OF_QUEUES-1:0] cbs_lo_credit_i,  //! loCredit per queue, signed bytes
  input wire [NUMBER_OF_QUEUES-1:0]    cbs_shaped_i,     //! 1 = shaped, 0 = strict priority

  //! One-hot: indicates which queue is granted
  output logic [NUMBER_OF_QUEUES-1:0] grant_queue_o,
  axi_stream_if.slave  s_axis,        //! slave interface of AXIS
  axi_stream_if.master m_axis         //! master interface of AXIS
);

  //! Indicates whether each queue is currently transmitting
  logic [NUMBER_OF_QUEUES-1:0] is_transmitting = 0;
  logic [NUMBER_OF_QUEUES-1:0] is_transmitting_raw = 0;
  //! Number of bytes transmitted in the current cycle (per queue)
  logic [15:0] bytes_sent_raw [NUMBER_OF_QUEUES];
  logic [15:0] bytes_sent [NUMBER_OF_QUEUES];
  //! Credit-based decision signal from CBS modules
  logic [NUMBER_OF_QUEUES-1:0] allow_transmit;
  //! Currently active queue index
  logic [$clog2(NUMBER_OF_QUEUES)-1:0] active_queue;
  //! Latch to hold current grant until end of packet (tlast)
  logic hold_grant;
  //! Priority-encoded index of the highest eligible queue; -1 if none.
  //! `priority_encode` scans from the TOP index down (802.1Q order).
  int sel_comb;

  assign m_axis.tdata = s_axis.tdata;
  assign m_axis.tvalid = s_axis.tvalid;
  assign m_axis.tkeep = s_axis.tkeep;
  assign m_axis.tlast = s_axis.tlast;
  assign m_axis.tdest = s_axis.tdest;
  assign s_axis.tready = m_axis.tready;

  assign grant_queue_o = hold_grant ? (1 << active_queue) : '0;

  for (genvar i = 0; i < NUMBER_OF_QUEUES; i++) begin : gen_cbs
    //! Per-queue CBS instance, configured at runtime from milan_csr.
    credit_based_shaper #(
      .CLK_FREQ_HZ(CLK_FREQ_HZ)
    ) u_cbs (
      .clk               (clk),
      .resetn            (resetn),
      .shaped_i          (cbs_shaped_i[i]),
      .idle_slope_i      (cbs_idle_slope_i[i*32 +: 32]),
      .hi_credit_i       (cbs_hi_credit_i[i*32 +: 32]),
      .lo_credit_i       (cbs_lo_credit_i[i*32 +: 32]),
      .queue_has_data_i  (queue_has_data_i[i]),
      .is_1g_i           (is_1g_i),
      .is_transmitting_i (is_transmitting[i]),
      .is_granted_i      (hold_grant && active_queue == i),
      .bytes_sent_i      (bytes_sent[i]),
      .allow_transmit_o  (allow_transmit[i])
    );
  end

  // --------------------------------------------------------------------------
  //  REQ-CBS-07 - EGRESS PACING. `is_transmitting_raw`/`bytes_sent_raw` below
  //  are derived from ACCEPTED beats only, so they are an honest measure of
  //  this AXIS port's occupancy (tb/verilator/shaper_core proves it: throttling
  //  the sink 8x moves the measured egress rate by 0.00 %). The per-BYTE
  //  sendSlope debit is therefore exact.
  //
  //  What is NOT exact is the accrual, and this is a real, measured deviation
  //  from 802.1Qav rather than a rounding artefact. The shaper hands 8 bytes
  //  per cycle to a MAC FIFO: at 100 MHz a beat leaves in 10 ns while 8 bytes
  //  on a 1 Gb/s wire occupy 64 ns. The queue accrues idleSlope during the
  //  ~5.4 cycles per beat that the wire is still busy, so with accrual on every
  //  non-transmitting cycle the steady state is
  //
  //      (CLK - r/8) * S/(8*CLK)  +  r * (S - link)/link  =  0
  //   => r = (S/8) / [ S/(64*CLK) + (link - S)/link ]           bytes/s
  //
  //  against the standard's r = S/8. Measured on the harness at 100 MHz /
  //  1 Gb/s: idleSlope 100 Mb/s over-delivers 9.6 %, 200 Mb/s over-delivers
  //  20.5 % - the error grows with idleSlope and with the CLK-to-link
  //  compression ratio.
  //
  //  UPSTREAM CONTRACT: the accounting is exact only if the egress is paced to
  //  line rate, i.e. a transmitting queue holds the port for the frame's real
  //  wire time. Our MAC TX FIFO absorbs frames faster than that, so the gap is
  //  live whenever per-queue CBS is enabled (it is disabled in the shipping
  //  config today - AAF rides the reservation bandwidth gate instead).
  //
  //  Two ways to close it, neither blind-safe without a bench run:
  //    (a) pace the sink - only correct if the MAC really backpressures at line
  //        rate, which a store-and-forward FIFO does not; or
  //    (b) make the accrual wall-clock-honest: after B bytes, suppress accrual
  //        for B*8*CLK/link cycles (a fractional "wire-time debt" accumulator).
  //        Sink-independent, and the natural home for the currently DEAD
  //        `is_granted_i` port of credit_based_shaper.
  //  tb/verilator/shaper_core asserts the accounting model above, so any change
  //  to the credit arithmetic shows up there immediately.
  // --------------------------------------------------------------------------
  for (genvar i = 0; i < NUMBER_OF_QUEUES; i++) begin : gen_transmit_info
    //! Track transmission status and byte count
    always_comb begin : transmissionStatus
      is_transmitting_raw[i] = (hold_grant && (active_queue == i) && m_axis.tvalid && m_axis.tready);
      bytes_sent_raw[i] = is_transmitting_raw[i] ? $countones(m_axis.tkeep) : 0;
    end

    always_ff @(posedge clk) begin
      if (!resetn) begin
        bytes_sent[i] <= 'd0;
        is_transmitting[i] <= 'd0;
      end else begin
        bytes_sent[i] <= bytes_sent_raw[i];
        is_transmitting[i] <= is_transmitting_raw[i];
      end
    end
  end

  always_comb begin : queue_selection
    sel_comb = priority_encode(allow_transmit & queue_has_data_i);
  end

  //! Queue grant logic - one queue should be grant a time
  always_ff @(posedge clk) begin
    if (!resetn) begin
      active_queue <= 0;
      hold_grant   <= 0;
    end else begin
      if (hold_grant) begin
        //! Release grant after end of packet
        if (m_axis.tvalid && m_axis.tready && m_axis.tlast)
          hold_grant <= 0;
      end else begin
      if (sel_comb >= 0) begin
        active_queue <= sel_comb;
        hold_grant   <= 1;
      end
    end
    end
  end


endmodule

`default_nettype wire
