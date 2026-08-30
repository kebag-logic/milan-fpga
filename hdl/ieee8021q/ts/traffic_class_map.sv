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
                    queue    = TC_QUEUE_MAP[tc]           (traffic class -> queue,
                               clamped to BEST_EFFORT when the programmed
                               index is >= NUMBER_OF_QUEUES - see below)

                  dmac_check (REQ-CLS-07, both modes):
                    the 0x88F7 gPTP fast path additionally requires the
                    reserved destination multicast 01-80-C2-00-00-0E; a
                    spoofed 0x88F7 otherwise takes the priority queue.

                  ctrl_class_en (REQ-CLS-10, both modes):
                    the control fast path - a DMAC-KEYED table of reserved
                    group addresses, see below.

                  use_pcp = 0 (legacy EtherType fallback):
                    reproduce the previous EtherType-based classification
                    (gPTP / SR-A / control / best-effort) so existing behaviour
                    is preserved until software programs the tables.

                ONE RULE PER TRAFFIC KIND (REQ-CLS-10):

                  TAGGED frames carry a real PCP, so 802.1Q decides: PCP ->
                  regen -> traffic class -> queue. That is the AVTP streams,
                  and they land on the CBS-shaped q4/q3.

                  UNTAGGED CONTROL frames carry NO PCP at all, so any queue
                  assignment expressed as a PCP mapping is fiction for them.
                  They are identified by their reserved DESTINATION GROUP
                  ADDRESS - the same thing a bridge classifies on, and far
                  harder to spoof than an EtherType. EtherType refines the
                  decision ONLY where one address carries two protocols.

                  Everything else falls through to the tables (best effort at
                  the reset configuration).

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
  parameter int NUMBER_OF_QUEUES = 5,                    //! Number of egress queues
  parameter int TDEST_WIDTH = $clog2(NUMBER_OF_QUEUES)   //! Width of the queue index
)(
  //! --- runtime configuration (milan_csr classifier group) ---
  input  wire        use_pcp_i,        //! 1 = PCP-table classification, 0 = legacy EtherType
  input  wire [2:0]  default_pcp_i,    //! Default port priority for untagged frames (REQ-CLS-03)
  input  wire [23:0] pcp_tc_map_i,     //! PCP->traffic-class table, 8 x 3 bits
  input  wire [23:0] prio_regen_i,     //! Priority regeneration table, 8 x 3 bits
  input  wire [31:0] tc_queue_map_i,   //! Traffic-class->queue table, 8 x 4 bits

  input  wire        dmac_check_i,     //! 1 = the gPTP fast path also demands the reserved DMAC (REQ-CLS-07)
  input  wire        ctrl_class_en_i,  //! 1 = untagged control frames take CONTROL_CLASS (REQ-CLS-10, CLS_CTRL[2], reset 1)

  //! --- parsed frame fields ---
  input  wire        vlan_valid_i,     //! Frame carried an 802.1Q C-TAG (0x8100)
  input  wire [2:0]  pcp_i,            //! PCP from vlan_tci[15:13] (valid if vlan_valid_i)
  input  wire        dei_i,            //! DEI from vlan_tci[12]   (valid if vlan_valid_i)
  input  wire [MAC_ADDR_BIT_WIDTH-1:0] dmac_i, //! Frame destination MAC, wire byte order (byte 0 = MSB)
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
  //! (ceil(log2 N) bits/entry), so at N=5 (still 3 bits/entry) the reset value
  //! 0x004898C0 is the map TC0,1 -> q0 - TC2 -> q3 - TC3 -> q4 - TC4,5 -> q1 -
  //! TC6,7 -> q2 (docs/reference/EGRESS_QUEUE_MAP.md).
  logic [TDEST_WIDTH-1:0] queue_sel_raw;
  //! ...clamped to a queue that EXISTS (see below).
  logic [TDEST_WIDTH-1:0] queue_sel;

  //! Legacy EtherType classification, matching the historical enum ordering.
  network_priority_t legacy_priority;



  //! DEI does not change the queue selection: 802.1Q §6.9.4 conveys
  //! drop_eligible WITH the frame for a downstream policer, it is not a
  //! priority input. The sideband itself is produced by traffic_classifier on
  //! `m_axis.tuser[0]` (REQ-CLS-05); the port stays here so the decode lives
  //! next to the PCP decode. Tie-off to keep lint quiet.
  wire _unused_dei = dei_i;

  // ---------------------------------------------------------------------------
  //  RESERVED CONTROL DESTINATION ADDRESSES - the table (REQ-CLS-10)
  // ---------------------------------------------------------------------------
  //! DMAC is the PRIMARY key for control traffic, and this table is the whole
  //! of it. Adding a protocol is A NEW ROW, not a redesign: bump
  //! CTRL_DMAC_N and add the address. Deliberately there is **no EtherType
  //! precondition** on a table hit, because the next protocol through this door
  //! is RSTP and RSTP HAS NO ETHERTYPE - a BPDU is an 802.3/LLC frame whose
  //! length field sits where an EtherType would, identified by DSAP/SSAP 0x42.
  //! Any `(eth_type == X) && (dmac == Y)` shape would lock it out permanently.
  //! (RSTP rides the Bridge Group Address 01-80-C2-00-00-00; the row, the LLC
  //! decode and its queue are a future decision. There is no spare queue to
  //! put it in any more - the 5-queue map dropped it for area - so adding RSTP
  //! means either sharing CONTROL_CLASS or renumbering.)
  localparam int CTRL_DMAC_N = 4;
  //! Row index of the ONE address that carries two protocols - see below.
  localparam int CTRL_ROW_NEAREST_BRIDGE = 0;
  //! The reserved control group addresses (ethernet_packet_pkg).
  localparam logic [MAC_ADDR_BIT_WIDTH-1:0] CTRL_DMAC_TBL [CTRL_DMAC_N] = '{
    MAC_DST_NEAREST_BRIDGE,  //!< 01-80-C2-00-00-0E  gPTP (q2) *and* MSRP (q1)
    MAC_DST_MVRP,            //!< 01-80-C2-00-00-21  MVRP
    MAC_DST_ATDECC,          //!< 91-E0-F0-01-00-00  1722.1 ADP / ACMP
    MAC_DST_MAAP             //!< 91-E0-F0-00-FF-00  1722 MAAP
  };

  //! Per-row destination-address match.
  wire [CTRL_DMAC_N-1:0] dmac_hit;
  for (genvar g = 0; g < CTRL_DMAC_N; g++) begin : g_ctrl_dmac
    assign dmac_hit[g] = (dmac_i == CTRL_DMAC_TBL[g]);
  end

  //! Frame is addressed to one of the reserved control group addresses.
  wire dmac_ctrl = |dmac_hit;
  //! I/G flag: 1 = group (multicast/broadcast), 0 = individual (unicast).
  wire dmac_group = dmac_i[MAC_IG_BIT];
  //! Untagged: no C-TAG, therefore no PCP. Control PDUs are untagged link-local
  //! frames by construction; a C-TAG means the frame carries a real priority and
  //! 802.1Q says that priority decides (which is what keeps a tagged 0x22F0 - an
  //! AVTP STREAM - on the shaped SR queues instead of here).
  wire untagged = !vlan_valid_i;

  //! Reserved-DMAC validation (REQ-CLS-07, 802.1AS-2020 §10.5 / 802.1Q Table 8-1).
  //! EtherType 0x88F7 alone is NOT proof of a gPTP frame - any station can mint
  //! one at an arbitrary destination, and the fast path below hands it the
  //! second-highest queue ahead of every shaped stream. With `dmac_check_i` set
  //! the fast path additionally demands the reserved multicast
  //! 01-80-C2-00-00-0E; a spoofed 0x88F7 then falls through to the ordinary
  //! PCP tables (or BEST_EFFORT in legacy mode) instead of stealing priority.
  //! Default is OFF (CLS_CTRL[1] reset 0) so wire behaviour is unchanged until
  //! software opts in. UNCHANGED by REQ-CLS-10 - including the fact that it does
  //! not test `untagged`; this arm is the one thing the control fast path was
  //! told not to disturb.
  wire gptp_frame = (eth_type_i == ETH_TYPE_PTP) &&
                    (!dmac_check_i || dmac_hit[CTRL_ROW_NEAREST_BRIDGE]);

  // ---------------------------------------------------------------------------
  //  CONTROL FAST PATH (REQ-CLS-10)
  // ---------------------------------------------------------------------------
  //! ARM 1 - the table. Any untagged frame to a reserved control group address
  //! is control traffic. No EtherType precondition (see the RSTP note above).
  //!
  //! THE ONE PLACE THE ETHERTYPE REFINES: 01-80-C2-00-00-0E carries BOTH gPTP
  //! (0x88F7 -> q2) AND MSRP (0x22EA -> q1), and they must not collapse into one
  //! queue. The split is the `gptp_frame` arm winning the priority chain below,
  //! so at that single address 0x88F7 leaves for GPTP_CLASS and everything else
  //! - MSRP included - stays here on CONTROL_CLASS.
  wire ctrl_reserved = dmac_ctrl;

  //! ARM 2 - AECP, the protocol with NO group address. An AECP command or
  //! response is addressed to the PEER entity's individual MAC (on egress that
  //! is the controller we are answering, not our own station MAC - our address
  //! is the SOURCE here, so `rx_mac_filter`'s station identity is of no use on
  //! this side of the wire). There is nothing to look up, so this arm and only
  //! this arm is keyed on the EtherType: an untagged 0x22F0 to an INDIVIDUAL
  //! address is AECP. It is the weakest arm by construction - say so plainly
  //! rather than pretend the table covers it - but it is bounded: CONTROL_CLASS
  //! is q1, below gPTP and below both CBS-shaped classes, so the worst a forged
  //! 0x22F0 buys is a lift over best effort.
  wire ctrl_unicast = !dmac_group && (eth_type_i == ETH_TYPE_AVTP);

  //! Control fast path, gated by CLS_CTRL[2] (reset 1 = ON, REQ-CLS-10).
  //! Clearing the bit restores the VERSION 0x0011 behaviour bit-for-bit.
  wire control_frame = ctrl_class_en_i && untagged && (ctrl_reserved || ctrl_unicast);

  always_comb begin : classify
    // ---- PCP table path (REQ-CLS-01..04) ----
    eff_pcp       = vlan_valid_i ? pcp_i : default_pcp_i;
    regen_prio    = prio_regen_i[eff_pcp*3 +: 3];
    traffic_class = pcp_tc_map_i[regen_prio*3 +: 3];
    queue_sel_raw = tc_queue_map_i[traffic_class*TDEST_WIDTH +: TDEST_WIDTH];

    // ---- OUT-OF-RANGE QUEUE CLAMP (needed at N=6, still needed at N=5) ----
    // With N a power of two the queue index could not overflow: every
    // TDEST_WIDTH-bit value named a real queue. At N=5 the 3-bit field can
    // name q5/q6/q7, which do not exist - and the downstream axis_demux SILENTLY
    // DROPS a frame whose `select >= M_COUNT` (verilog-axis axis_demux.v:
    // `drop_ctl = drop || select >= M_COUNT`). A single mis-programmed
    // CLS_TC_QUEUE_MAP nibble would therefore turn into an invisible TX black
    // hole. Clamp instead: an unmapped traffic class rides BEST_EFFORT, which
    // is observable (frames arrive, just unprioritised) rather than silent.
    // No-op for N = 2/4/8, so this costs nothing on a power-of-two build.
    queue_sel     = (32'(queue_sel_raw) >= NUMBER_OF_QUEUES)
                    ? TDEST_WIDTH'(BEST_EFFORT) : queue_sel_raw;

    // ---- legacy EtherType path (fallback, unchanged semantics) ----
    unique case (1'b1)
      gptp_frame:
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
    // latency-critical. The legacy arm always classed them GPTP_CLASS; in PCP
    // mode they fell through default_pcp to whatever the tables say. Make PCP
    // mode match legacy: gPTP always rides its own class, above best-effort
    // and control, and OUT of the CBS-shaped SR queues.
    //
    // 802.1Q-ORDER MAP: GPTP_CLASS is q2 and sits BELOW the shaped q4/q3, not
    // above them. That is deliberate and it is a CORRECTNESS requirement, not
    // a preference - 802.1Q credit-based shaping assumes the shaped queues are
    // the top of the strict-priority order, and any strict-priority queue
    // above them invalidates the credit accounting that bounds class-A
    // latency. gPTP is unharmed: every event message is timestamped in
    // hardware at the egress SFD (ptp_ts_top), so a queueing delay moves only
    // *when* the frame leaves, never the value it carries. The full argument
    // lives in ethernet_packet_pkg::network_priority_t and
    // docs/reference/EGRESS_QUEUE_MAP.md - do not "fix" this by promoting
    // gPTP back above the SR classes.
    //
    // Fabric control sources join after this classifier through dedicated
    // arbitration. Bulk traffic classified here therefore cannot be used to
    // infer or tune the latency of those control sources.
    // CONTROL FAST-PATH (2026-07-26, REQ-CLS-10): same argument as gPTP, for
    // the same reason. MAAP, MSRP, MVRP and the 1722.1 ADP/ACMP/AECP trio are
    // untagged link-local frames - they carry no PCP, so the PCP tables could
    // never route them anywhere but `default_pcp_i`, and at the reset
    // configuration (use_pcp = 1, default_pcp = 0) that is BEST EFFORT. The
    // CONTROL_CLASS row of docs/reference/EGRESS_QUEUE_MAP.md was
    // therefore unimplemented on the wire: only the legacy arm ever reached it,
    // and only for 0x22F0. This arm makes the documented map true at reset.
    //
    // ORDER IS LOAD-BEARING: gPTP is tested FIRST, and that test is what splits
    // the shared 01-80-C2-00-00-0E address - 0x88F7 to GPTP_CLASS (q2), MSRP
    // 0x22EA at the same address falls through to CONTROL_CLASS (q1).
    //
    // A TAGGED 0x22F0 IS A STREAM, NOT CONTROL: `control_frame` requires
    // `untagged`, so an AVTP stream keeps its PCP and rides the shaped SR
    // queues (q4 class A / q3 class B). Do not relax that term.
    if (gptp_frame)
      tdest_o = TDEST_WIDTH'(GPTP_CLASS);
    else if (control_frame)
      tdest_o = TDEST_WIDTH'(CONTROL_CLASS);
    else if (use_pcp_i)
      tdest_o = queue_sel;
    else
      tdest_o = legacy_priority[TDEST_WIDTH-1:0];
  end

endmodule

`default_nettype wire
