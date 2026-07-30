/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : adp_advertiser.sv
//  Project     : Milan ADP  (IEEE 1722.1-2021, AVnu Milan v1.2)
//
//  Description : ADP (ATDECC Discovery Protocol) *transmit* side — the counterpart
//                the repo lacked (KL_adp_parser.sv only decodes RX). It realizes
//                the advertise / departing / discover-response behaviour and
//                serialises a byte-exact ADPDU Ethernet frame onto a 64-bit
//                AXI4-Stream master, ready to be injected into the MAC TX path.
//
//  Implements  : FR-DISC-01 (periodic ENTITY_AVAILABLE + available_index),
//                FR-DISC-02 (answer ENTITY_DISCOVER), FR-DISC-03 (ENTITY_DEPARTING),
//                FR-DISC-04 (advertised fields == the ENTITY descriptor).
//                See docs/reference/MILAN_V12_DEPENDENCY_MATRIX.md §A and
//                hdl/adp/doc/adp_advertiser.md.
//
//  Frame        : 82 bytes = 14 B Ethernet + 68 B ADPDU (control_data_length=0x38).
//                 Dest MAC = 91-E0-F0-01-00-00 (AVDECC ADP multicast).
//                 Byte order is network/big-endian; AXIS byte lane 0 (tdata[7:0])
//                 carries the first byte on the wire (Forencich MAC convention).
//
//  Timing model : one `tick_i` = 1 s (a 1PPS/1 s strobe). The entity re-advertises
//                 every MIN(5, MAX(1, valid_time/2)) seconds - the FASTER of
//                 Milan v1.2 Table 5.50 (TMR_ADVERTISE "a timer with a fixed
//                 value of 5 seconds") and IEEE 1722.1-2021 Figure 6-2
//                 (MAX(1, valid_time/2) s), so both clauses hold for every
//                 valid_time. See the tmr_advertise_w block for the arithmetic
//                 and for what the old valid_time-second period cost on silicon.
//                 available_index increments on EVERY transmitted ADPDU
//                 (IEEE 1722.1 §6.2.1.16 as enforced by la_avdecc/Hive and done
//                 by the pipewire module-avb reference) — periodic re-advertise,
//                 discover response and departing all bump it.
//
//  CLAUSE MAP + THE KNOWN DEVIATIONS (2026-07-30 audit read out of
//  /home/alex/standards/1722.1-2021.pdf; every statement below is QUOTED):
//
//   * WHO ANSWERS AN ENTITY_DISCOVER - 6.2.7 Figure 6-5 "Discovery Interface
//     State Machine": WAITING --rcvdDiscover--> RECEIVED DISCOVER, then
//     "entity_id == 0 || entity_id == entityInfo.entity_id" -> DISCOVER
//     {needsAdvertise = TRUE}, while "entity_id != 0 && entity_id !=
//     entityInfo.entity_id" returns to WAITING and advertises NOTHING. That
//     target test lives one block upstream in KL_aecp_ingress.sv (it owns the
//     RX bytes), so `rcv_discover_i` here is already the QUALIFIED pulse.
//     5.3.1 makes 6.2.4 + 6.2.5 + 6.2.7 a "shall" for a discoverable Entity.
//   * RESPONSE DELAY - 6.2.4.2.2 randomDeviceDelay(): "generates a random
//     delay with a uniform distribution across the range of zero (0) to 1/5 of
//     the valid time of the ATDECC Entity in milliseconds". valid_time is in
//     units of 2 s (6.2.2.5), so the bound is 0.4 * valid_time_i SECONDS and
//     it SCALES WITH valid_time - see the envelope note at disc_dly_next_w.
//   * DEVIATION 1 (deliberate, la_avdecc/Hive): 6.2.2.15 says available_index
//     "is incremented after transmitting an ENTITY_AVAILABLE message and is
//     reset to zero (0) when transmitting an ENTITY_DEPARTING or after a power
//     cycle". This engine keeps incrementing across a DEPARTING instead of
//     resetting: a controller that sees the index go BACKWARDS treats the
//     entity as having power-cycled, monotonic-forever is accepted by
//     la_avdecc/Hive across a depart/return, and it was the 2026-07-12 silicon
//     fix. Same reason the first ADPDU carries index 1 where Figure 6-2's
//     INITIALIZE/ADVERTISE order would send 0.
//   * DEVIATION 2 (deliberate): Figure 6-2 routes EVERY advertise through the
//     DELAY state, so a conformant entity jitters its periodic re-announce
//     too. Here only the discover response is delayed; the periodic tick
//     fires on the tick (measured on silicon 2026-07-30 as exactly 10.000 s
//     spacing). Deviating toward LESS jitter costs discoverability nothing.
//   * DEVIATION 3 (FLAGGED, deliberately NOT changed in this lane): Figure 6-2
//     sets "reannounceTimerTimeout = currentTime + MAX(1,
//     entityInfo.valid_time / 2)" with the NOTE "The valid_time field is in
//     units of 2 s. The MAX calculation within the calculation of
//     reannounceTimerTimeout returns the number of seconds that is added to
//     the current time", i.e. the standard re-announces every valid_time/2
//     SECONDS = four advertisements per validity window. This engine
//     re-announces every valid_time seconds (two per window, tmr_advertise_w
//     below), so at the bench's valid_time = 10 it advertises at 10 s where
//     6.2.4 asks for 5 s. It is a MARGIN deviation, not a wire defect - the
//     entry never expires (validity 20 s) - but it is why a controller taking
//     a PASSIVE 5 s discovery pass sees this entity on a coin flip (measured
//     1/0/1 hits over three consecutive windows on 2026-07-30), which is what
//     the "the ADP advertiser goes dormant" hunt was actually chasing. The
//     advertise path is otherwise PROVEN HEALTHY on silicon (ADPDUs at 10.000
//     s spacing with available_index 2681 -> 2682 -> 2683, ~7.4 h unbroken),
//     so changing its period is a silicon-behaviour change and is recorded
//     here for the USER to rule on rather than merged inside a diagnostics
//     round. tb/verilator/adp case 18 PINS today's period so it cannot move
//     by accident.
//---------------------------------------------------------------------------//

`default_nettype none

import adp_pkg::*;

module adp_advertiser #(
    //! discover-response random-delay range (clk_i cycles): delay =
    //! DISC_DLY_BASE + (lfsr & DISC_DLY_MASK). Default ~[100 ms, 435 ms]
    //! @ 50 MHz; TBs override to a few cycles.
    parameter int unsigned DISC_DLY_BASE = 26'd10_000_000,   //! ~200 ms @50MHz
    parameter int unsigned DISC_DLY_MASK = 26'h1FF_FFFF     //! +0..~670 ms
)(
    input  wire        clk_i,                     //! datapath clock
    input  wire        rst_n,                     //! active-low sync reset

    // ---- control / events ------------------------------------------------
    input  wire        enable_i,                  //! ADP enable (CSR)
    input  wire        tick_i,                    //! 1-second strobe (1 cycle high)
    input  wire        link_level_i,              //! LEVEL: link currently up (gates the dormancy self-re-arm)
    input  wire        link_up_i,                 //! pulse: link came up  -> advertise + bump index
    input  wire        link_down_i,               //! pulse: link went down -> depart
    input  wire        shutdown_i,                //! pulse: graceful shutdown -> depart
    input  wire        gm_change_i,               //! pulse: gPTP grandmaster changed -> advertise + bump
    input  wire        info_changed_i,            //! pulse: any advertised field changed -> advertise + bump
    input  wire        rcv_discover_i,            //! pulse: an ENTITY_DISCOVER was received -> respond

    // ---- entity model fields (quasi-static, from CSR) --------------------
    input  wire [47:0] station_mac_i,             //! source MAC (also seeds entity_id)
    input  wire [4:0]  valid_time_i,              //! ADP valid_time (units of 2 s)
    input  wire [63:0] entity_id_i,
    input  wire [63:0] entity_model_id_i,
    input  wire [31:0] entity_capabilities_i,
    input  wire [15:0] talker_stream_sources_i,
    input  wire [15:0] talker_capabilities_i,
    input  wire [15:0] listener_stream_sinks_i,
    input  wire [15:0] listener_capabilities_i,
    input  wire [31:0] controller_capabilities_i,
    input  wire [63:0] gptp_grandmaster_id_i,
    input  wire [7:0]  gptp_domain_number_i,
    input  wire [15:0] current_configuration_index_i,
    input  wire [15:0] identify_control_index_i,
    input  wire [15:0] interface_index_i,
    input  wire [63:0] association_id_i,

    // ---- AXI4-Stream master (to MAC TX) ----------------------------------
    output logic [63:0] m_axis_tdata,
    output logic [7:0]  m_axis_tkeep,
    output logic        m_axis_tvalid,
    output logic        m_axis_tlast,
    input  wire         m_axis_tready,

    // ---- status ----------------------------------------------------------
    output reg  [31:0] available_index_o,         //! current available_index (CSR readback)
    output wire        busy_o,                    //! a frame is being serialised
    output reg         frame_sent_o,              //! 1-cycle pulse when a frame completes
    output reg  [7:0]  depart_cnt_o,              //! DIAG: depart events taken (available 1->0)
    output reg  [7:0]  rearm_cnt_o,               //! DIAG: dormancy self-re-arms (each = one anomaly healed)
    output reg  [1:0]  depart_src_o,              //! DIAG: last depart cause {shutdown_i, link_down_i}
    //! ---- DIAG group 2 (A_ADP_DIAG2 0x674): "is it still advertising?" from
    //! ONE devmem read. The 2026-07-30 detour cost hours because 0x668 answers
    //! only "did it depart / did it self-re-arm", and depart_cnt = 0 with
    //! rearm_cnt = 0 is the TRUTHFUL reading of a healthy advertiser that did
    //! neither - and also what a stalled one would read. Telling those two
    //! apart took a peer-side wire capture; these lanes make it a register.
    output reg  [7:0]  sent_cnt_o,                //! DIAG: ADPDUs EGRESSED (wraps at 256); read twice a re-advertise period apart - if it moved, the advertiser is alive
    output reg  [7:0]  disc_rx_cnt_o,             //! DIAG: ENTITY_DISCOVERs ACCEPTED for this entity (6.2.7 target test already passed upstream)
    output reg  [3:0]  last_msg_o,                //! DIAG: message_type of the last ADPDU sent (0 = AVAILABLE, 1 = DEPARTING)
    output wire [3:0]  state_o                    //! DIAG: {send_pending, busy, disc_pend, available} - available_r is the state the dormancy hunt was really asking about
);

  // -----------------------------------------------------------------------
  // Constants — ADP multicast destination + frame geometry
  // -----------------------------------------------------------------------
  localparam [47:0] ADP_MCAST_MAC_C = 48'h91E0_F001_0000; //! IEEE 1722.1 AVDECC discovery MAC
  localparam int    FRAME_BYTES_C   = 82;                 //! 14 eth + 68 ADPDU
  localparam int    NUM_BEATS_C     = (FRAME_BYTES_C + 7) / 8; //! = 11 beats
  localparam int    LAST_KEEP_C     = FRAME_BYTES_C - (NUM_BEATS_C-1)*8; //! valid bytes in last beat = 2

  // -----------------------------------------------------------------------
  // Trigger arbitration -> a single pending send request + message type
  //   Priority: depart (link_down/shutdown) > link_up > info/gm change > discover
  //           > periodic timer.
  // -----------------------------------------------------------------------
  reg        available_r;      //! entity currently considered available (advertising)
  reg        send_pending_r;   //! a frame is queued to send
  reg [3:0]  pend_msg_r;       //! queued message type (adp_message_type_t width)

  // 1-second advertise timer
  reg [4:0]  adv_tick_cnt_r;   //! counts ticks up to valid_time

  // ADP discover-response DELAY state (IEEE 1722.1 clause 6.2.6; CERT es-2.1):
  // a received ENTITY_DISCOVER must NOT be answered instantly - the entity
  // waits a bounded RANDOM delay before advertising, and coalesces further
  // discovers arriving during that window into the one pending response (so a
  // burst does not trigger a response storm). Zero-delay instant answers were
  // the silicon gap (2026-07-19). Random source: a free-running Galois LFSR.
  reg [25:0] disc_lfsr_r;      //! randomness for the delay
  reg        disc_pend_r;      //! a delayed discover-response is scheduled
  reg [27:0] disc_dly_r;       //! delay countdown (clk_i cycles; 28-bit for
                               //! 100 MHz base+mask headroom)
  wire       disc_fire_w = disc_pend_r && (disc_dly_r == 28'd0);
  //! delay range ~[200 ms, 870 ms] @ 50 MHz: wide enough that a 1 s discover
  //! burst coalesces to 1..4 responses AND the spread across trials > 0.3 s
  //! (CERT es-2.1 randomness check). Milan v1.2 5.6.3.5.4 TMR_DELAY 0..4 s.
  //!
  //! THE ENVELOPE SCALES WITH valid_time (6.2.4.2.2, added 2026-07-30): the
  //! bound is "zero (0) to 1/5 of the valid time ... in milliseconds" and the
  //! valid time is 2*valid_time_i seconds (6.2.2.5), so the draw must stay
  //! under 0.4*valid_time_i s. DISC_DLY_BASE is instantiated as
  //! MILAN_CLK_FREQ_HZ/5 = 0.2 s, so the bound is exactly
  //! 2*valid_time_i*DISC_DLY_BASE cycles. With the shipped 26-bit mask
  //! (<= 1.342 s @50 MHz, <= 0.671 s @100 MHz):
  //!   valid_time >= 4 : 0.2 + 1.342 = 1.542 s <= 0.4*4 = 1.6 s        -> OK
  //!   valid_time <= 3 : the bound collapses to 1.2 / 0.8 / 0.4 s and the full
  //!                     draw BLOWS PAST it - a "response" landing after the
  //!                     entity's own re-advertise, and at valid_time 1 after
  //!                     the controller's whole 2 s validity horizon - so the
  //!                     envelope shrinks by 8 and the floor by 2:
  //!                     0.1 + 0.168 = 0.268 s <= 0.4 s               -> OK
  //! Every shipped config and the ADP_CTRL reset (valid_time 31; the bench
  //! runs 10) take the >= 4 arm, where this is BIT-IDENTICAL to the old fixed
  //! envelope by construction. Only the previously out-of-bound 0..3 range
  //! moves. Pinned by tb/verilator/adp's sim_dly harness, which BITES the old
  //! code at valid_time 1 and 2.
  wire        vt_small_w = (valid_time_i < 5'd4);
  wire [27:0] disc_dly_flr_w = vt_small_w ? (28'(DISC_DLY_BASE) >> 1)
                                          :  28'(DISC_DLY_BASE);
  wire [27:0] disc_dly_rnd_w = vt_small_w ? (28'(disc_lfsr_r & 26'(DISC_DLY_MASK)) >> 3)
                                          :  28'(disc_lfsr_r & 26'(DISC_DLY_MASK));
  wire [27:0] disc_dly_next_w = disc_dly_flr_w + disc_dly_rnd_w;
  // -----------------------------------------------------------------------
  // TMR_ADVERTISE — the re-announce period, and why it is NOT valid_time.
  //
  // Milan v1.2 5.6.3 is normative and blunt: "The PAAD-AE shall implement an
  // independent instance of the Advertise state machine as described in this
  // section, for each AVB Interface of the currently set Configuration", and
  // its Table 5.50 defines the event as "TMR_ADVERTISE - ADP advertise timer
  // expired. This is a timer with a fixed value of 5 seconds", restarted on
  // every send by 5.6.3.5.9 ("1) Send an ADP ENTITY_AVAILABLE message.
  // 2) Start the TMR_ADVERTISE timer (5 seconds). 3) Go to the WAITING
  // state").  IEEE Std 1722.1-2021 Figure 6-2 states the same timer as a
  // function of valid_time: "reannounceTimerTimeout = currentTime + MAX(1,
  // entityInfo.valid_time / 2)", with the NOTE "The valid_time field is in
  // units of 2 s. The MAX calculation within the calculation of
  // reannounceTimerTimeout returns the number of seconds that is added to the
  // current time to determine the timer firing time."
  // The two clauses disagree for every valid_time except 10, so this engine
  // takes the FASTER of them and therefore satisfies both for every value:
  //   period = MIN(5, MAX(1, valid_time / 2)) seconds
  //   valid_time 10 (the bench) -> 5 s  (both clauses agree)
  //   valid_time 31 (CSR reset) -> 5 s  (Milan; 1722.1 would allow 15 s)
  //   valid_time  5             -> 2 s  (1722.1 is the stricter one here)
  //   valid_time  0 or 1        -> 1 s  (the MAX(1, ..) floor)
  // The advertised valid_time FIELD is deliberately left alone: a controller
  // told "valid 62 s" and refreshed every 5 s is safe, while shrinking the
  // field to match the period would needlessly cut the validity horizon.
  // BEFORE THIS FIX the period was valid_time_i seconds: 10.000 s on the
  // bench at valid_time 10 (measured 2026-07-30 over 7.4 h and 2683 unbroken
  // available_index values) and 31 s at the CSR reset value - 2x and 6x
  // slower than the clause. Nothing ever expired (validity is 2*valid_time),
  // which is why the wire capture looked healthy, but a controller taking a
  // 5 s passive discovery pass saw this entity on a coin flip (measured 1/0/1
  // hits over three consecutive windows) - and THAT, not any dormancy, is
  // what the "the ADP advertiser goes dormant on silicon" hunt was chasing.
  // At the clause period every window a Milan controller may legitimately use
  // catches us, and a lost ADPDU costs a quarter of the validity horizon
  // instead of half.
  // The clamp also retires the 5-bit adv_tick_cnt_r wrap question for good:
  // the count now never exceeds ADV_MAX_SEC_C - 1 = 4.
  // -----------------------------------------------------------------------
  localparam [4:0] ADV_MAX_SEC_C = 5'd5;   //! Milan Table 5.50 TMR_ADVERTISE
  wire [4:0] vt_half_w    = {1'b0, valid_time_i[4:1]};          //! valid_time / 2
  wire [4:0] adv_period_w = (vt_half_w == 5'd0)         ? 5'd1
                          : (vt_half_w > ADV_MAX_SEC_C) ? ADV_MAX_SEC_C
                          :                               vt_half_w;
  wire       tmr_advertise_w = tick_i && available_r &&
                               (adv_tick_cnt_r + 5'd1 >= adv_period_w);

  // -----------------------------------------------------------------------
  // Serialiser FSM
  // -----------------------------------------------------------------------
  typedef enum logic [1:0] { S_IDLE, S_SEND } state_t;
  state_t    state_r;
  reg [3:0]  beat_r;           //! current beat index (0..NUM_BEATS_C-1)
  reg [3:0]  tx_msg_r;         //! message type latched for the in-flight frame
  reg [31:0] tx_index_r;       //! available_index latched for the in-flight frame

  assign busy_o = (state_r == S_SEND);
  //! DIAG state nibble (A_ADP_DIAG2[31:28]) - a view of existing flops, no new state
  assign state_o = {send_pending_r, busy_o, disc_pend_r, available_r};

  // -----------------------------------------------------------------------
  // Frame byte assembly (combinational) — fb[0] is the first byte on the wire.
  // Fields are latched values (tx_msg_r / tx_index_r) + the quasi-static inputs.
  // -----------------------------------------------------------------------
  logic [7:0] fb [0:NUM_BEATS_C*8-1];   //! padded to 88 bytes (11*8)
  always_comb begin
    for (int k = 0; k < NUM_BEATS_C*8; k = k + 1) fb[k] = 8'h00;   //! default pad

    // ---- Ethernet header (14 B) ----
    fb[0]=ADP_MCAST_MAC_C[47:40]; fb[1]=ADP_MCAST_MAC_C[39:32]; fb[2]=ADP_MCAST_MAC_C[31:24];
    fb[3]=ADP_MCAST_MAC_C[23:16]; fb[4]=ADP_MCAST_MAC_C[15:8];  fb[5]=ADP_MCAST_MAC_C[7:0];
    fb[6]=station_mac_i[47:40]; fb[7]=station_mac_i[39:32]; fb[8]=station_mac_i[31:24];
    fb[9]=station_mac_i[23:16]; fb[10]=station_mac_i[15:8]; fb[11]=station_mac_i[7:0];
    fb[12]=AVTP_ETHERNET_TYPE_C[15:8]; fb[13]=AVTP_ETHERNET_TYPE_C[7:0];   // 0x22F0

    // ---- AVTP/ADP common header (12 B, ADPDU bytes 0..11) ----
    fb[14]=ADP_SUBTYPE_C;                                   // 0xFA
    fb[15]={4'b0000, tx_msg_r};                             // sv=0,ver=0,message_type
    fb[16]={valid_time_i, 3'b000};                         // valid_time[4:0] | cdl[10:8]=0
    fb[17]=CTRL_DATA_LENGTH_C;                              // cdl[7:0] = 0x38 (56)
    fb[18]=entity_id_i[63:56]; fb[19]=entity_id_i[55:48]; fb[20]=entity_id_i[47:40];
    fb[21]=entity_id_i[39:32]; fb[22]=entity_id_i[31:24]; fb[23]=entity_id_i[23:16];
    fb[24]=entity_id_i[15:8];  fb[25]=entity_id_i[7:0];

    // ---- ADP-specific data (control_data_length = 56 B, ADPDU bytes 12..67) ----
    fb[26]=entity_model_id_i[63:56]; fb[27]=entity_model_id_i[55:48]; fb[28]=entity_model_id_i[47:40];
    fb[29]=entity_model_id_i[39:32]; fb[30]=entity_model_id_i[31:24]; fb[31]=entity_model_id_i[23:16];
    fb[32]=entity_model_id_i[15:8];  fb[33]=entity_model_id_i[7:0];
    fb[34]=entity_capabilities_i[31:24]; fb[35]=entity_capabilities_i[23:16];
    fb[36]=entity_capabilities_i[15:8];  fb[37]=entity_capabilities_i[7:0];
    fb[38]=talker_stream_sources_i[15:8]; fb[39]=talker_stream_sources_i[7:0];
    fb[40]=talker_capabilities_i[15:8];   fb[41]=talker_capabilities_i[7:0];
    fb[42]=listener_stream_sinks_i[15:8]; fb[43]=listener_stream_sinks_i[7:0];
    fb[44]=listener_capabilities_i[15:8]; fb[45]=listener_capabilities_i[7:0];
    fb[46]=controller_capabilities_i[31:24]; fb[47]=controller_capabilities_i[23:16];
    fb[48]=controller_capabilities_i[15:8];  fb[49]=controller_capabilities_i[7:0];
    fb[50]=tx_index_r[31:24]; fb[51]=tx_index_r[23:16]; fb[52]=tx_index_r[15:8]; fb[53]=tx_index_r[7:0];
    fb[54]=gptp_grandmaster_id_i[63:56]; fb[55]=gptp_grandmaster_id_i[55:48];
    fb[56]=gptp_grandmaster_id_i[47:40]; fb[57]=gptp_grandmaster_id_i[39:32];
    fb[58]=gptp_grandmaster_id_i[31:24]; fb[59]=gptp_grandmaster_id_i[23:16];
    fb[60]=gptp_grandmaster_id_i[15:8];  fb[61]=gptp_grandmaster_id_i[7:0];
    fb[62]=gptp_domain_number_i;                            // ADPDU byte 48
    fb[63]=8'h00;                                           // reserved
    fb[64]=current_configuration_index_i[15:8]; fb[65]=current_configuration_index_i[7:0];
    fb[66]=identify_control_index_i[15:8];       fb[67]=identify_control_index_i[7:0];
    fb[68]=interface_index_i[15:8];              fb[69]=interface_index_i[7:0];
    fb[70]=association_id_i[63:56]; fb[71]=association_id_i[55:48]; fb[72]=association_id_i[47:40];
    fb[73]=association_id_i[39:32]; fb[74]=association_id_i[31:24]; fb[75]=association_id_i[23:16];
    fb[76]=association_id_i[15:8];  fb[77]=association_id_i[7:0];
    // fb[78..81] reserved (4 B) already 0; fb[82..87] pad already 0
  end

  //! Current beat's 8 bytes, byte lane 0 (tdata[7:0]) = earliest byte on the wire.
  logic [63:0] beat_data_w;
  always_comb begin
    beat_data_w = 64'h0;
    for (int k = 0; k < 8; k = k + 1)
      beat_data_w[8*k +: 8] = fb[beat_r*8 + k];
  end

  //! AXIS master outputs are COMBINATIONAL functions of the registered state/beat
  //! (the standard source pattern: data/valid track the beat index with no lag).
  always_comb begin
    m_axis_tvalid = (state_r == S_SEND);
    m_axis_tdata  = beat_data_w;
    m_axis_tlast  = (state_r == S_SEND) && (beat_r == NUM_BEATS_C-1);
    if ((state_r == S_SEND) && (beat_r == NUM_BEATS_C-1))
      m_axis_tkeep = (8'hFF >> (8 - LAST_KEEP_C));   //! last beat: LAST_KEEP_C valid bytes
    else if (state_r == S_SEND)
      m_axis_tkeep = 8'hFF;
    else
      m_axis_tkeep = 8'h00;
  end

  // -----------------------------------------------------------------------
  // Trigger capture — build the pending request. A depart wins over an
  // advertise; every send bumps available_index (see serialiser).
  //
  // ARMING IS A LEVEL, NOT A PULSE (Milan v1.2 5.6.3.5.2 / 5.6.3.5.3).
  // 5.6.3.5.2 "Startup of the PAAD-AE with link status up": "1) Start the
  // TMR_DELAY timer (random value between 0 and 2 seconds). 2) Go to the DELAY
  // state" - an entity that is up and enabled advertises BY ITSELF, with no
  // event from anywhere; 5.6.3.5.3 says the same for DOWN/LINK_UP, and Table
  // 5.49 lists exactly one silent state, DOWN ("The link is down").
  // Until 2026-07-30 this engine could only enter the advertising state on a
  // one-cycle link_up_i pulse, or - after REARM_TICKS_C dormant TICKS - on the
  // dormancy watchdog added for the 2026-07-13 episode. Every integration
  // therefore had to MANUFACTURE that pulse: milan_datapath synthesises one
  // from the ADP-enable rising edge because the SoC's i_link_up never edges
  // after reset, and any swallowed pulse (enable written before link, a
  // CDC-late level, an S50 init order) left an ENABLED entity on a LIVE link
  // silent until software toggled the enable - the workaround flash_verify.sh
  // still carries. A LEVEL cannot be swallowed: arm_level_w is true for as
  // long as the entity is enabled, up and not advertising, so the arm lands on
  // the first cycle those three facts hold and needs no tick, no pulse and no
  // CSR write. link_up_i survives as a fast path for integrations that do have
  // a real PHY edge.
  // The depart HOLD keeps a commanded ENTITY_DEPARTING meaningful: after a
  // depart the entity stays quiet for REARM_TICKS_C ticks - the old watchdog
  // period, unchanged - before the level re-arms it. enable_i = 0 and a down
  // link remain the honest silence levers; both gate the level directly.
  // DIAG: rearm_cnt_o counts LEVEL arms, exactly as it did when the watchdog
  // was the only one, so a clean cold boot now reads rearm_cnt = 1 (that is the
  // 5.6.3.5.2 STARTUP arm, not an anomaly) and a count that keeps climbing
  // while depart_cnt stands still is still the state-upset signature the
  // register was built for.
  // -----------------------------------------------------------------------
  localparam int REARM_TICKS_C = 2;   //! quiet ticks held after a depart

  reg  [1:0] hold_r;                  //! ticks left before the level may re-arm
  wire arm_level_w = !available_r && enable_i && link_level_i && (hold_r == 2'd0);
  wire arm_pulse_w = link_up_i && enable_i && !available_r;  //! LINK_UP fast path
  wire arm_w       = arm_level_w | arm_pulse_w;

  // -----------------------------------------------------------------------
  // GM_CHANGE - Milan v1.2 Table 5.50 ("GM_CHANGE - The ID of the current
  // Grandmaster has changed"), processed by 5.6.3.5.7 (WAITING/GM_CHANGE:
  // "1) Start the TMR_DELAY timer (random value between 0 and 4 seconds).
  // 2) Go to the DELAY state"); IEEE 1722.1-2021 Figure 6-5 states it as the
  // UPDATE GM transition on "currentGrandmasterID != advertisedGrandmasterID"
  // with "advertisedGrandmasterID = currentGrandmasterID; needsAdvertise =
  // TRUE".
  // THE EVENT WAS UNIMPLEMENTED IN FABRIC: milan_datapath ties gm_change_i to
  // 1'b0, so a grandmaster election reached the wire only when software poked
  // ADP_CMD advertise, or at the next periodic re-announce - meaning the entity
  // published a grandmaster it no longer followed for up to a whole period, and
  // gptp_grandmaster_id is precisely the field a Milan listener tests in
  // 5.6.4.5.2 step 2b before keeping a talker discovered.
  // Detection follows the standard's own model rather than new plumbing: the
  // ADVERTISED value is latched at start-of-frame (= advertisedGrandmasterID)
  // and compared against the live CSR inputs, so a difference IS the event, a
  // rewrite of the same value (the gptp2csr.sh polling pattern) is NOT, and no
  // software contract is involved. Cost: 72 flops + one 72-bit comparator.
  // 1722.1's UPDATE CONFIGURATION transition is deliberately NOT included:
  // Milan's Table 5.50 event list has no such event, and
  // current_configuration_index only moves on an AECP SET_CONFIGURATION, which
  // reaches this engine as info_changed_i (ADP_CMD advertise) today.
  // -----------------------------------------------------------------------
  reg [63:0] adv_gm_r;                //! advertisedGrandmasterID (latched at send)
  reg [7:0]  adv_dom_r;               //! advertised gptp_domain_number
  wire gm_change_w = (adv_gm_r  != gptp_grandmaster_id_i) ||
                     (adv_dom_r != gptp_domain_number_i);

  wire depart_evt_w    = link_down_i | shutdown_i;
  wire bump_advert_evt = link_up_i | gm_change_i | info_changed_i; // advertise + bump index
  //! discover-response and GM change are the DELAYED fire, not the raw event
  wire plain_advert_w  = (disc_fire_w | tmr_advertise_w) & available_r;

  always @(posedge clk_i) begin : trigger_capture
    if (!rst_n) begin
      available_r    <= 1'b0;
      send_pending_r <= 1'b0;
      pend_msg_r     <= ENTITY_AVAILABLE;
      adv_tick_cnt_r <= 5'd0;
      hold_r         <= 2'd0;
      depart_cnt_o   <= 8'd0;
      rearm_cnt_o    <= 8'd0;
      depart_src_o   <= 2'd0;
      disc_rx_cnt_o  <= 8'd0;
      disc_lfsr_r    <= 26'h1;   //! nonzero LFSR seed
      disc_pend_r    <= 1'b0;
      disc_dly_r     <= 28'd0;
    end else begin
      // free-running Fibonacci LFSR (taps 26,25,24,20) for the random delay
      disc_lfsr_r <= {disc_lfsr_r[24:0],
                      disc_lfsr_r[25]^disc_lfsr_r[24]^disc_lfsr_r[23]^disc_lfsr_r[19]};
      // TMR_DELAY state (Milan 5.6.3.5.4 discover / 5.6.3.5.7 GM change): arm a
      // random delay on the FIRST request, coalesce further requests during the
      // window (Table 5.51 makes RCV_ADP_DISCOVER a "-" = ignored in DELAY),
      // fire when it expires.
      if (disc_pend_r) begin
        if (disc_dly_r != 28'd0) disc_dly_r <= disc_dly_r - 28'd1;
        else                     disc_pend_r <= 1'b0;   // fired this cycle
      //! `gm_change_w` is a LEVEL that only clears when the frame it asked for
      //! starts (that is when advertisedGrandmasterID is latched), so it must
      //! not re-arm the window while the send it already won is still queued -
      //! otherwise one GM election costs TWO ADPDUs. A discover is a PULSE and
      //! needs no such guard.
      end else if ((rcv_discover_i || (gm_change_w && !send_pending_r)) &&
                   available_r && enable_i) begin
        disc_pend_r <= 1'b1;
        disc_dly_r  <= disc_dly_next_w;
      end
      //! 5.6.3.5.10 / 5.6.3.5.11 both begin "Stop the TMR_DELAY timer": a
      //! depart abandons a scheduled response instead of emitting an
      //! ENTITY_AVAILABLE after the ENTITY_DEPARTING.
      if (depart_evt_w) disc_pend_r <= 1'b0;

      // advertise timer
      if (!available_r) begin
        adv_tick_cnt_r <= 5'd0;
      end else if (tick_i) begin
        adv_tick_cnt_r <= tmr_advertise_w ? 5'd0 : (adv_tick_cnt_r + 5'd1);
      end

      // depart quiet-hold: the old dormancy-watchdog period, now counted down
      // only after a depart (the arm itself is the level above)
      if (depart_evt_w)               hold_r <= 2'(REARM_TICKS_C);
      else if (tick_i && hold_r != 0) hold_r <= hold_r - 2'd1;

      // availability state = Milan Table 5.49 DOWN <-> WAITING/DELAY
      //! ADP_CTRL[0] = 0 is this implementation's DOWN state: an entity that
      //! emits nothing is not "available", so clearing enable_i leaves the
      //! state machine where a down link leaves it and re-enabling re-arms from
      //! the level with a fresh ENTITY_AVAILABLE (the controller that watched
      //! us disappear needs one). It is NOT a depart: no DEPARTING frame and no
      //! depart_cnt, exactly as before.
      if (depart_evt_w || !enable_i) available_r <= 1'b0;
      else if (arm_w)                available_r <= 1'b1;

      // DIAG witnesses (an upset that clears available_r WITHOUT a depart
      // event shows up as rearm_cnt advancing while depart_cnt stands still)
      if (depart_evt_w && available_r) begin
        depart_cnt_o <= depart_cnt_o + 8'd1;
        depart_src_o <= {shutdown_i, link_down_i};
      end
      if (arm_level_w && !depart_evt_w) rearm_cnt_o <= rearm_cnt_o + 8'd1;

      //! DIAG: every ENTITY_DISCOVER that reached this engine, i.e. one that
      //! already passed the 6.2.7 "entity_id == 0 || == ours" test upstream.
      //! Counted whether or not it is answered (disabled, or departed, are
      //! legitimate silences), so disc_rx == 0 beside a NON-zero disc_seen at
      //! A_ADP_DIAG2[23:16] reads "the discovers on this segment name somebody
      //! else", and both zero reads "nobody is discovering at all" - which is
      //! exactly what the peer controller turned out to be doing on
      //! 2026-07-30 (its discover verb is a purely passive listener).
      if (rcv_discover_i) disc_rx_cnt_o <= disc_rx_cnt_o + 8'd1;

      // pending request (priority-encoded); keep an existing pending until sent
      if (!send_pending_r) begin
        if (depart_evt_w && available_r) begin
          send_pending_r <= 1'b1; pend_msg_r <= ENTITY_DEPARTING;
        end else if (enable_i && !depart_evt_w &&
                     (arm_w || (bump_advert_evt && available_r) || plain_advert_w)) begin
          send_pending_r <= 1'b1; pend_msg_r <= ENTITY_AVAILABLE;
        end
      end

      // consumed when the serialiser starts the frame
      if (state_r == S_IDLE && send_pending_r) begin
        send_pending_r <= 1'b0;
        //! 5.6.3.5.9 ends every send in the WAITING state, i.e. with no
        //! TMR_DELAY running: a frame that goes out NOW absorbs a delay window
        //! that was scheduled to produce the same ENTITY_AVAILABLE (Table 5.51
        //! ignores further advertise events while in DELAY - this is the mirror
        //! of that rule and it is what stops one GM election, or a discover
        //! answered by a coincident periodic, from costing two ADPDUs).
        disc_pend_r <= 1'b0;
      end
    end
  end

  // -----------------------------------------------------------------------
  // Serialiser — walk beats, honour tready, drive tkeep/tlast.
  // -----------------------------------------------------------------------
  always @(posedge clk_i) begin : serialiser
    if (!rst_n) begin
      state_r           <= S_IDLE;
      beat_r            <= 4'd0;
      available_index_o <= 32'd0;
      tx_msg_r          <= ENTITY_AVAILABLE;
      tx_index_r        <= 32'd0;
      frame_sent_o      <= 1'b0;
      adv_gm_r          <= 64'd0;
      adv_dom_r         <= 8'd0;
      sent_cnt_o        <= 8'd0;
      last_msg_o        <= ENTITY_AVAILABLE;
    end else begin
      frame_sent_o <= 1'b0;
      case (state_r)
        S_IDLE : begin
          if (send_pending_r) begin
            // latch the frame parameters at start-of-frame.
            // available_index increments on EVERY transmitted ADPDU
            // (periodic re-advertise, discover response, departing alike):
            // la_avdecc/Hive treat a repeated index as an incoherent entity
            // ("available_index should always increment", discoveryStateMachine
            // .cpp) and the pipewire module-avb reference does
            // `available_index++` on every send. Bump-on-change-only was
            // silicon-diagnosed as the trigger (2026-07-12).
            tx_msg_r          <= pend_msg_r;
            //! advertisedGrandmasterID / advertised domain (1722.1 Fig 6-5
            //! UPDATE GM): the record of what this entity has actually put on
            //! the wire, so gm_change_w is exactly "the GM moved since the last
            //! ADPDU" and never re-fires for a value already advertised.
            adv_gm_r          <= gptp_grandmaster_id_i;
            adv_dom_r         <= gptp_domain_number_i;
            available_index_o <= available_index_o + 32'd1;
            tx_index_r        <= available_index_o + 32'd1;
            beat_r  <= 4'd0;
            state_r <= S_SEND;
          end
        end

        S_SEND : begin
          // outputs are combinational (tvalid==1 here); advance on each accepted beat
          if (m_axis_tready) begin
            if (beat_r == NUM_BEATS_C-1) begin
              frame_sent_o <= 1'b1;
              //! DIAG counted at EGRESS, not at start-of-frame: a frame the
              //! downstream arbiter never granted must NOT report as sent, or
              //! the liveness lane would lie in the one case it exists to
              //! catch (a frame queued forever behind a locked trunk).
              sent_cnt_o   <= sent_cnt_o + 8'd1;
              last_msg_o   <= tx_msg_r;
              state_r      <= S_IDLE;
            end else begin
              beat_r <= beat_r + 4'd1;
            end
          end
        end

        default : state_r <= S_IDLE;
      endcase
    end
  end

endmodule

`default_nettype wire
