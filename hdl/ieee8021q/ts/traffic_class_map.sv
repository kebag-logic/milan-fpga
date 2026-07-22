/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : traffic_class_map.sv
  Author      : Kebag Logic

  Date        : 2026-07-01
  Description : IEEE 802.1Q priority-to-queue mapping (pure combinational).

                Given the parsed VLAN/EtherType fields of a frame and the
                runtime classifier configuration (from milan_csr, REQ-CLS-01..04),
                produce the egress queue index (`tdest`). Two modes:

                  use_pcp = 1 (802.1Q, REQ-CLS-01/02/04):
                    eff_pcp  = vlan_valid ? frame PCP : default port priority
                               (REQ-CLS-03 for untagged frames)
                    regen    = PRIO_REGEN[eff_pcp]        (priority regeneration,
                               802.1Q Table 6-4 style, programmable)
                    tc       = PCP_TC_MAP[regen]          (PCP -> traffic class,
                               802.1Q Table 8-5 style, programmable)
                    queue    = TC_QUEUE_MAP[tc]           (traffic class -> queue)

                  use_pcp = 0 (legacy EtherType fallback):
                    reproduce the previous EtherType-based classification
                    (gPTP / SR-A / control / best-effort) so existing behaviour
                    is preserved until software programs the tables.

                This block is intentionally free of any FIFO/primitive so it can
                be unit-tested in Verilator (tb/verilator/cls, REQ-VER-03); the
                surrounding traffic_classifier handles buffering and parsing.

  Company     : Kebag Logic
  Project     : 802.1Q Traffic Shaper
------------------------------------------------------------------------------
*/

`include "ethernet_packet_pkg.sv"
import ethernet_packet_pkg::*;

`default_nettype none

module traffic_class_map #(
  parameter int NUMBER_OF_QUEUES = 4,                    //! Number of egress queues
  parameter int TDEST_WIDTH = $clog2(NUMBER_OF_QUEUES)   //! Width of the queue index
)(
  //! --- runtime configuration (milan_csr classifier group) ---
  input  wire        use_pcp_i,        //! 1 = PCP-table classification, 0 = legacy EtherType
  input  wire [2:0]  default_pcp_i,    //! Default port priority for untagged frames (REQ-CLS-03)
  input  wire [23:0] pcp_tc_map_i,     //! PCP->traffic-class table, 8 x 3 bits
  input  wire [23:0] prio_regen_i,     //! Priority regeneration table, 8 x 3 bits
  input  wire [31:0] tc_queue_map_i,   //! Traffic-class->queue table, 8 x 4 bits

  //! --- parsed frame fields ---
  input  wire        vlan_valid_i,     //! Frame carried an 802.1Q C-TAG (0x8100)
  input  wire [2:0]  pcp_i,            //! PCP from vlan_tci[15:13] (valid if vlan_valid_i)
  input  wire        dei_i,            //! DEI from vlan_tci[12]   (valid if vlan_valid_i)
  input  wire [15:0] eth_type_i,       //! Inner EtherType (after any C-TAG)

  output logic [TDEST_WIDTH-1:0] tdest_o //! Egress queue index
);

  //! Effective PCP: the frame's PCP if tagged, else the configured port default.
  logic [2:0] eff_pcp;
  //! Regenerated priority (802.1Q ingress priority regeneration).
  logic [2:0] regen_prio;
  //! Traffic class selected by the PCP->TC table.
  logic [2:0] traffic_class;
  //! Queue selected by the TC->queue table. Per the ABI (docs/reference/REGISTER_MAP.md)
  //! CLS_TC_QUEUE_MAP packs one TDEST_WIDTH-bit queue index per traffic class
  //! (ceil(log2 N) bits/entry), so the reset value 0xE4 is the identity map
  //! 3,2,1,0 for N=4.
  logic [TDEST_WIDTH-1:0] queue_sel;

  //! Legacy EtherType classification, matching the historical enum ordering.
  network_priority_t legacy_priority;



  //! DEI is decoded for drop-eligibility sideband use (REQ-CLS-05); it does not
  //! change the queue selection in this revision. Tie-off to keep lint quiet.
  wire _unused_dei = dei_i;

  always_comb begin : classify
    // ---- PCP table path (REQ-CLS-01..04) ----
    eff_pcp       = vlan_valid_i ? pcp_i : default_pcp_i;
    regen_prio    = prio_regen_i[eff_pcp*3 +: 3];
    traffic_class = pcp_tc_map_i[regen_prio*3 +: 3];
    queue_sel     = tc_queue_map_i[traffic_class*TDEST_WIDTH +: TDEST_WIDTH];

    // ---- legacy EtherType path (fallback, unchanged semantics) ----
    unique case (1'b1)
      (eth_type_i == ETH_TYPE_PTP):
        legacy_priority = GPTP_CLASS;
      (vlan_valid_i && (eth_type_i == ETH_TYPE_AVTP)):
        legacy_priority = SRA_CLASS;
      ((eth_type_i == ETH_TYPE_AVTP) && !vlan_valid_i):
        legacy_priority = CONTROL_CLASS;
      default:
        legacy_priority = BEST_EFFORT;
    endcase

    // ---- select mode ----
    // gPTP FAST-PATH (2026-07-13): 0x88F7 frames are untagged (no PCP) yet
    // latency-critical. The legacy arm always classed them GPTP_CLASS (q1,
    // second-highest; q0 = SRA and queue index 0 = HIGHEST at the grant's
    // priority encoder); in PCP mode they fell through default_pcp to
    // whatever the tables say. Make PCP mode match legacy: gPTP always rides
    // its own class, above best-effort and OUT of the CBS-shaped SRA queue
    // (audio credit windows must not gate sync). NOTE: the TX-flood tx-ts
    // timeouts of 2026-07-13 were NOT queue starvation - silicon ran legacy
    // mode (gPTP already q1 > TCP q3); the delay lives in the DRIVER's single
    // TX descriptor ring (256 slots ~ 30 ms of bulk backlog at 100 Mbit,
    // upstream of this classifier). tx_timestamp_timeout 50 covers it; the
    // real fix for that class is a priority TX ring/doorbell (future).
    if (eth_type_i == ETH_TYPE_PTP)
      tdest_o = TDEST_WIDTH'(GPTP_CLASS);
    else if (use_pcp_i)
      tdest_o = queue_sel;
    else
      tdest_o = legacy_priority[TDEST_WIDTH-1:0];
  end

endmodule

`default_nettype wire
