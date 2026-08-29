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

                ARBITRATION ORDER (802.1Q, 5-queue map): the HIGHEST queue index
                wins - q4 (SR class A) over q3 (class B) over q2 (gPTP) over q1
                (control) over q0 (best effort). The shaped
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
  parameter int NUMBER_OF_QUEUES = 5, //! Number of network queues
  //! Which queues get a credit_based_shaper INSTANCE. Default all-ones =
  //! byte-identical to every build before 2026-07-28. A masked-out queue is
  //! strict-priority only: allow_transmit is constant 1, exactly the
  //! behaviour a built CBS shows whenever its runtime cbs_shaped_i is 0 -
  //! which is how the shipping config runs EVERY queue today (AAF rides the
  //! lwSRP reservation bw-gate; per-queue CBS was never enabled on q0-q2).
  //! The two SR-class queues keep their instances; the builder derives the
  //! mask from srp.class_queue rather than a hand-typed constant. Measured
  //! (ship 8x8 place report): each pruned instance returns ~425 LUT + 6 DSP.
  parameter bit [NUMBER_OF_QUEUES-1:0] CBS_QUEUES_MASK_P = '1
)(
  input wire clk,                     //! clock signal
  input wire resetn,                  //! synchronous active low reset
  //! One-hot: indicates which queues contain data
  input wire [NUMBER_OF_QUEUES-1:0] queue_has_data_i,
  input wire is_1g_i,                 //! High when the link rate is 1GBps

  //! --- per-queue CBS runtime config, packed [q*32 +: 32] (from milan_csr) ---
  input wire [32*NUMBER_OF_QUEUES-1:0] cbs_idle_slope_bps_i, //! idleSlope per queue, bits/s
  input wire [32*NUMBER_OF_QUEUES-1:0] cbs_hi_credit_bytes_i,  //! hiCredit per queue, signed bytes
  input wire [32*NUMBER_OF_QUEUES-1:0] cbs_lo_credit_bytes_i,  //! loCredit per queue, signed bytes
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
  //! Frame end (tlast) on the accepted beat, per queue - the CBS wire-time
  //! debt charges the per-frame overhead on exactly this beat (REQ-CBS-07)
  logic [NUMBER_OF_QUEUES-1:0] frame_end_raw = 0;
  logic [NUMBER_OF_QUEUES-1:0] frame_end = 0;
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
    if (CBS_QUEUES_MASK_P[i]) begin : g_cbs
      //! Per-queue CBS instance, configured at runtime from milan_csr.
      credit_based_shaper #(
        .CLK_FREQ_HZ(CLK_FREQ_HZ)
      ) u_cbs (
        .clk               (clk),
        .resetn            (resetn),
        .shaped_i          (cbs_shaped_i[i]),
        .idle_slope_bps_i      (cbs_idle_slope_bps_i[i*32 +: 32]),
        .hi_credit_bytes_i       (cbs_hi_credit_bytes_i[i*32 +: 32]),
        .lo_credit_bytes_i       (cbs_lo_credit_bytes_i[i*32 +: 32]),
        .queue_has_data_i  (queue_has_data_i[i]),
        .is_1g_i           (is_1g_i),
        .is_transmitting_i (is_transmitting[i]),
        .is_granted_i      (hold_grant && active_queue == i),
        .bytes_sent_i      (bytes_sent[i]),
        .tlast_i           (frame_end[i]),
        .allow_transmit_o  (allow_transmit[i])
      );
    end : g_cbs
    else begin : g_nocbs
      //! Strict-priority-only queue: identical to a built CBS whose runtime
      //! cbs_shaped_i stays 0 (allow_transmit is then constant 1 - see
      //! credit_based_shaper's shaped_i bypass). Its cbs_* CSR words keep
      //! their addresses and read back as written; they are inert here, the
      //! same way LPF_CTRL is inert on a render_lpf-pruned build.
      assign allow_transmit[i] = 1'b1;
    end : g_nocbs
  end

  // --------------------------------------------------------------------------
  //  REQ-CBS-07 - EGRESS PACING, wire-time honest. `is_transmitting_raw`/
  //  `bytes_sent_raw` below are derived from ACCEPTED beats only, so they are
  //  an honest measure of this AXIS port's occupancy (tb/verilator/shaper_core
  //  proves it: throttling the sink 8x does not move the measured egress
  //  rate). The per-BYTE sendSlope debit is therefore exact.
  //
  //  The ACCRUAL used to violate 802.1Q-2018 8.6.8.2: the shaper hands 8
  //  bytes per cycle to a MAC FIFO, so at 100 MHz a beat leaves in 10 ns
  //  while 8 bytes occupy 64 ns of 1 Gb/s wire, and idleSlope accrued during
  //  the ~5.4 cycles per beat the wire was still busy - measured 9.6 / 20.5
  //  percent over-delivery at idleSlope 100 / 200 Mb/s. Since REQ-CBS-07
  //  landed, credit_based_shaper carries a per-queue Q16 wire-time debt
  //  (bytes per accepted beat + the 24-octet per-frame overhead + min-frame
  //  pad at tlast, drained at the port byte rate): the debt IS the 8.6.8.2
  //  (e) `transmit` variable, and idleSlope accrues only while it is zero.
  //  `frame_end` below gives each queue's CBS the tlast it charges the
  //  per-frame overhead on. Sink-independent by construction - the debt
  //  drains at the port rate no matter how fast the MAC FIFO absorbs.
  //
  //  Steady-state egress under the debt law (frame of L client bytes,
  //  overhead V = 24 + max(0, 60 - L)):
  //
  //      r = (S/8) * L*link / (L*link + (V)*S)        client bytes/s
  //
  //  i.e. the reservation's own per-frame overhead now comes out of the
  //  shaped rate (conservative; the old law handed it out twice).
  //  tb/verilator/shaper_core asserts this model, and tb/verilator/cbs pins
  //  the debt/credit arithmetic state-for-state against a reference model.
  // --------------------------------------------------------------------------
  for (genvar i = 0; i < NUMBER_OF_QUEUES; i++) begin : gen_transmit_info
    //! Track transmission status and byte count
    always_comb begin : transmissionStatus
      is_transmitting_raw[i] = (hold_grant && (active_queue == i) && m_axis.tvalid && m_axis.tready);
      bytes_sent_raw[i] = is_transmitting_raw[i] ? $countones(m_axis.tkeep) : 0;
      frame_end_raw[i] = is_transmitting_raw[i] && m_axis.tlast;
    end

    always_ff @(posedge clk) begin
      if (!resetn) begin
        bytes_sent[i] <= 'd0;
        is_transmitting[i] <= 'd0;
        frame_end[i] <= 'd0;
      end else begin
        bytes_sent[i] <= bytes_sent_raw[i];
        is_transmitting[i] <= is_transmitting_raw[i];
        frame_end[i] <= frame_end_raw[i];
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
