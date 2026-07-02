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
//                See docs/MILAN_V12_DEPENDENCY_MATRIX.md §A and
//                hdl/adp/doc/adp_advertiser.md.
//
//  Frame        : 82 bytes = 14 B Ethernet + 68 B ADPDU (control_data_length=0x38).
//                 Dest MAC = 91-E0-F0-01-00-00 (AVDECC ADP multicast).
//                 Byte order is network/big-endian; AXIS byte lane 0 (tdata[7:0])
//                 carries the first byte on the wire (Forencich MAC convention).
//
//  Timing model : one `tick_i` = 1 s (a 1PPS/1 s strobe). The entity re-advertises
//                 every `valid_time_i` seconds (ADP validity = 2*valid_time s, so
//                 re-advertising each valid_time s keeps the entry fresh).
//                 available_index is bumped ONLY on a real change (link-up /
//                 info-change / GM-change) — NOT on periodic re-advertise or on a
//                 discover response — so controllers do not see spurious changes.
//---------------------------------------------------------------------------//

`default_nettype none

import adp_pkg::*;

module adp_advertiser (
    input  wire        clk_i,                     //! datapath clock
    input  wire        rst_n,                     //! active-low sync reset

    // ---- control / events ------------------------------------------------
    input  wire        enable_i,                  //! ADP enable (CSR)
    input  wire        tick_i,                    //! 1-second strobe (1 cycle high)
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
    output reg         frame_sent_o               //! 1-cycle pulse when a frame completes
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
  reg        pend_bump_r;      //! queued: bump available_index before sending

  // 1-second advertise timer
  reg [4:0]  adv_tick_cnt_r;   //! counts ticks up to valid_time
  wire       tmr_advertise_w = tick_i && available_r &&
                               (adv_tick_cnt_r + 5'd1 >= (valid_time_i == 0 ? 5'd1 : valid_time_i));

  // -----------------------------------------------------------------------
  // Serialiser FSM
  // -----------------------------------------------------------------------
  typedef enum logic [1:0] { S_IDLE, S_SEND } state_t;
  state_t    state_r;
  reg [3:0]  beat_r;           //! current beat index (0..NUM_BEATS_C-1)
  reg [3:0]  tx_msg_r;         //! message type latched for the in-flight frame
  reg [31:0] tx_index_r;       //! available_index latched for the in-flight frame

  assign busy_o = (state_r == S_SEND);

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
  // advertise; a real change also bumps available_index.
  // -----------------------------------------------------------------------
  wire depart_evt_w    = link_down_i | shutdown_i;
  wire bump_advert_evt = link_up_i | gm_change_i | info_changed_i; // advertise + bump index
  wire plain_advert_w  = rcv_discover_i | tmr_advertise_w;         // advertise, no bump

  always @(posedge clk_i) begin : trigger_capture
    if (!rst_n) begin
      available_r    <= 1'b0;
      send_pending_r <= 1'b0;
      pend_msg_r     <= ENTITY_AVAILABLE;
      pend_bump_r    <= 1'b0;
      adv_tick_cnt_r <= 5'd0;
    end else begin
      // advertise timer
      if (!available_r) begin
        adv_tick_cnt_r <= 5'd0;
      end else if (tick_i) begin
        adv_tick_cnt_r <= tmr_advertise_w ? 5'd0 : (adv_tick_cnt_r + 5'd1);
      end

      // availability state
      if (depart_evt_w)      available_r <= 1'b0;
      else if (link_up_i && enable_i) available_r <= 1'b1;

      // pending request (priority-encoded); keep an existing pending until sent
      if (!send_pending_r) begin
        if (depart_evt_w && available_r) begin
          send_pending_r <= 1'b1; pend_msg_r <= ENTITY_DEPARTING; pend_bump_r <= 1'b0;
        end else if (bump_advert_evt && (available_r || link_up_i) && enable_i) begin
          send_pending_r <= 1'b1; pend_msg_r <= ENTITY_AVAILABLE; pend_bump_r <= 1'b1;
        end else if (plain_advert_w && available_r && enable_i) begin
          send_pending_r <= 1'b1; pend_msg_r <= ENTITY_AVAILABLE; pend_bump_r <= 1'b0;
        end
      end

      // consumed when the serialiser starts the frame
      if (state_r == S_IDLE && send_pending_r) send_pending_r <= 1'b0;
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
    end else begin
      frame_sent_o <= 1'b0;
      case (state_r)
        S_IDLE : begin
          if (send_pending_r) begin
            // latch the frame parameters at start-of-frame
            tx_msg_r <= pend_msg_r;
            if (pend_bump_r) begin
              available_index_o <= available_index_o + 32'd1;
              tx_index_r        <= available_index_o + 32'd1;
            end else begin
              tx_index_r        <= available_index_o;
            end
            beat_r  <= 4'd0;
            state_r <= S_SEND;
          end
        end

        S_SEND : begin
          // outputs are combinational (tvalid==1 here); advance on each accepted beat
          if (m_axis_tready) begin
            if (beat_r == NUM_BEATS_C-1) begin
              frame_sent_o <= 1'b1;
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
