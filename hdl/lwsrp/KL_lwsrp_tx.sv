/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_lwsrp_tx.sv
//  Project     : Milan lwSRP  (IEEE 802.1Q MSRP/MVRP, AVnu Milan v1.2 §5.6)
//
//  Description : lwSRP applicant transmit engine — template MRPDU serialiser
//                (the adp_advertiser recipe: combinational frame-byte array,
//                registered beat walker, 64-bit little-lane AXIS master into
//                the low-rate control merge).
//
//                Always-declare applicant subset (docs/LWSRP_FPGA_ARCHITECTURE
//                .md §1): every JoinTime tick it emits one MSRP MRPDU (Domain,
//                plus TalkerAdvertise while the talker is enabled) followed by
//                one MVRP MRPDU (the SR VID). Single-value vectors only
//                (NumberOfValues = 1), like the pipewire reference.
//
//                Event selection per attribute (reference lifecycle,
//                mrp.c applicant FSM):
//                  NEW     first TX after the attribute becomes declared
//                          (enable / talker-enable rising edge),
//                  JOININ  every refresh after that (and the re-declare
//                          after a received LeaveAll),
//                  LV      the final TX when the attribute is withdrawn
//                          (talker disable -> TalkerAdvertise only;
//                           engine disable -> everything, then silence).
//
//                LeaveAll: our own LeaveAllTime turn (leaveall_tick_i) sets
//                the LeaveAllEvent field in BOTH next PDUs' vector headers
//                (the reference's global lva_tx_pending). A received LeaveAll
//                (rx_leaveall_i, from the walker) re-declares promptly.
//
//                Frames are zero-padded to 60 bytes in fabric — the MRPDU
//                message-list EndMark terminates parsing, so trailing zeros
//                are inert — because the low-rate merge path has never
//                carried a sub-60-byte frame (ADP is 82 B) and MAC min-frame
//                padding is not a property we have silicon-proven.
//---------------------------------------------------------------------------//

`default_nettype none

import lwsrp_pkg::*;

module KL_lwsrp_tx (
    input  wire         clk_i,
    input  wire         rst_n,

    // ---- control -------------------------------------------------------
    input  wire         enable_i,          //! lwSRP engine enable (CSR)
    input  wire         talker_en_i,       //! declare TalkerAdvertise (CSR)
    input  wire         join_tick_i,       //! JoinTime strobe (KL_lwsrp_timers)
    input  wire         leaveall_tick_i,   //! our LeaveAll turn
    input  wire         rx_leaveall_i,     //! LeaveAll registered (walker)

    // ---- listener declaration (ACMP listener SM hooks) -------------------
    input  wire         lstn_declare_i,    //! declare the Listener attribute
    input  wire         lstn_ready_i,      //! 1 = Ready, 0 = AskingFailed
    input  wire [63:0]  lstn_sid_i,        //! bound stream_id

    // ---- identity / stream table row 0 (CSR group) ----------------------
    input  wire [47:0]  station_mac_i,     //! [47:40] = first wire byte
    input  wire [15:0]  unique_id_i,       //! stream_id = {station_mac, uid}
    input  wire [47:0]  dest_mac_i,        //! stream DMAC (CSR until MAAP)
    input  wire [11:0]  vid_i,             //! SR VID (Domain + DataFrameParams + MVRP)
    input  wire [15:0]  max_frame_i,       //! TSpec MaxFrameSize
    input  wire [15:0]  interval_frames_i, //! TSpec MaxIntervalFrames
    input  wire [31:0]  latency_i,         //! AccumulatedLatency (ns)

    // ---- AXI4-Stream master (little lane; -> low-rate TX merge) ---------
    output logic [63:0] m_axis_tdata,
    output logic [7:0]  m_axis_tkeep,
    output logic        m_axis_tvalid,
    output logic        m_axis_tlast,
    input  wire         m_axis_tready,

    // ---- status ----------------------------------------------------------
    output reg          talker_declared_o, //! TalkerAdvertise currently on the wire
    output reg          lstn_declared_o,   //! Listener attribute on the wire
    output reg  [15:0]  tx_count_o         //! MRPDUs sent
);

  // -----------------------------------------------------------------------
  // Frame geometry. MSRP message sizes: Domain 13 B, TalkerAdvertise 34 B,
  // Listener 18 B (+ 15 B header/version + 2 B message-list EndMark):
  //   Domain only            30 B -> pad 60, 8 beats
  //   Domain+TalkerAdv       64 B -> 8 beats
  //   Domain+Listener        48 B -> pad 60, 8 beats
  //   Domain+TalkerAdv+Lstn  82 B -> 11 beats (last keep 2)
  // MVRP is 26 B -> pad 60. Short frames are zero-padded in fabric (the
  // MRPDU EndMark makes trailing zeros inert; MAC min-frame padding is not
  // a property we have silicon-proven).
  // -----------------------------------------------------------------------
  localparam int NUM_BEATS_C     = 8;    //! all frames except the 3-message MSRP
  localparam int MAX_BEATS_C     = 11;
  localparam int PAD_FRAME_LEN_C = 60;   //! padded short-frame length
  localparam int FULL_FRAME_LEN_C= 64;   //! MSRP Domain+TalkerAdvertise

  typedef enum logic [0:0] { FK_MSRP_E, FK_MVRP_E } frame_kind_t;

  // -----------------------------------------------------------------------
  // Trigger capture
  // -----------------------------------------------------------------------
  reg enable_q, talker_q;

  wire enable_rise_w = enable_i & ~enable_q;
  wire enable_fall_w = ~enable_i & enable_q;
  wire talker_rise_w = enable_i & talker_en_i & ~talker_q;
  wire talker_fall_w = enable_i & ~talker_en_i & talker_q;

  reg msrp_pend_r, mvrp_pend_r;      //! normal declare pair queued
  reg [2:0] jdiv_r;                  //! join-tick /5 divider (1 s refresh)
  reg talker_lv_pend_r;              //! withdraw TalkerAdvertise only
  reg lstn_lv_pend_r;                //! withdraw the Listener attribute only
  reg engine_lv_pend_r;              //! withdraw everything (engine disable)
  reg lva_pend_r;                    //! set LeaveAllEvent in the next pair
  reg fresh_domain_r, fresh_vid_r, fresh_talker_r, fresh_lstn_r; //! NEW next TX
  reg lstn_q, lstn_ready_q;

  // -----------------------------------------------------------------------
  // Serialiser state — frame parameters latched at start-of-frame
  // -----------------------------------------------------------------------
  typedef enum logic [1:0] { S_IDLE, S_SEND, S_GAP } state_t;
  state_t      state_r;
  //! inter-frame gap after every frame we emit: the MVRP (second of the
  //! MSRP+MVRP pair) died in the arty's MAC egress whenever it entered
  //! within one frame-serialization time of the MSRP (100 Mbit MII drains
  //! ~6 us/frame; the GbE AX never hit it; the full-datapath sim passes the
  //! pair - the eater is MAC-side, dp TB lwsrp-egress 2026-07-19). 1024
  //! cycles (20 us @50 MHz) clears a worst-case 100 Mbit frame; protocol-
  //! irrelevant. Real fix owed: MilanMAC back-to-back TB.
  localparam int GAP_CYCLES_C = 1024;
  reg [10:0]   gap_r;
  reg [3:0]    beat_r;
  frame_kind_t kind_r;
  reg          talker_incl_r;        //! MSRP frame carries TalkerAdvertise
  reg          lstn_incl_r;          //! MSRP frame carries the Listener attr
  reg          lva_r;                //! LeaveAllEvent in this frame's vectors
  reg [2:0]    domain_evt_r, talker_evt_r, vid_evt_r, lstn_evt_r;

  wire is_full_w  = (kind_r == FK_MSRP_E) && talker_incl_r;
  wire is_full3_w = is_full_w && lstn_incl_r;   //! 82-byte 3-message MSRP
  wire [3:0] frame_beats_w = is_full3_w ? 4'(MAX_BEATS_C) : 4'(NUM_BEATS_C);
  wire [3:0] last_keep_w = is_full3_w ? 4'd2
                         : is_full_w  ? 4'd8
                         : 4'(PAD_FRAME_LEN_C - (NUM_BEATS_C-1)*8);  // = 4

  // -----------------------------------------------------------------------
  // Frame byte assembly (combinational over latched params).
  // fb[0] = first byte on the wire (little lane: tdata[7:0]).
  // -----------------------------------------------------------------------
  //! single-value ThreePackedEvents octet: e0*36 (e1 = e2 = 0)
  function automatic [7:0] pack3(input [2:0] e);
    pack3 = 8'(e) * 8'd36;
  endfunction

  //! vector header: {LeaveAllEvent[15:13], NumberOfValues[12:0]} = 1 value
  function automatic [15:0] vech(input lva);
    vech = {lva ? 3'b001 : 3'b000, 13'd1};
  endfunction

  //! single-value FourPackedEvents octet: p0*64
  function automatic [7:0] pack4(input [1:0] p);
    pack4 = {p, 6'b000000};
  endfunction

  logic [7:0] fb [0:MAX_BEATS_C*8-1];
  always_comb begin
    logic [15:0] vh;
    int lb;   //! Listener message base (after Domain [+TalkerAdvertise])
    for (int k = 0; k < MAX_BEATS_C*8; k++) fb[k] = 8'h00;   //! default pad
    vh = vech(lva_r);
    lb = talker_incl_r ? 62 : 28;

    // ---- Ethernet header (14 B) ----
    if (kind_r == FK_MSRP_E) begin
      fb[0]=MSRP_MCAST_MAC_C[47:40]; fb[1]=MSRP_MCAST_MAC_C[39:32];
      fb[2]=MSRP_MCAST_MAC_C[31:24]; fb[3]=MSRP_MCAST_MAC_C[23:16];
      fb[4]=MSRP_MCAST_MAC_C[15:8];  fb[5]=MSRP_MCAST_MAC_C[7:0];
    end else begin
      fb[0]=MVRP_MCAST_MAC_C[47:40]; fb[1]=MVRP_MCAST_MAC_C[39:32];
      fb[2]=MVRP_MCAST_MAC_C[31:24]; fb[3]=MVRP_MCAST_MAC_C[23:16];
      fb[4]=MVRP_MCAST_MAC_C[15:8];  fb[5]=MVRP_MCAST_MAC_C[7:0];
    end
    fb[6]=station_mac_i[47:40]; fb[7]=station_mac_i[39:32];
    fb[8]=station_mac_i[31:24]; fb[9]=station_mac_i[23:16];
    fb[10]=station_mac_i[15:8]; fb[11]=station_mac_i[7:0];

    if (kind_r == FK_MSRP_E) begin
      fb[12]=MSRP_ETHERTYPE_C[15:8]; fb[13]=MSRP_ETHERTYPE_C[7:0];
      fb[14]=MRP_PROTO_VER_C;
      // ---- Message 1: Domain (type 4, len 4, listlen 9) ----
      fb[15]=MSRP_ATTR_DOMAIN_C;
      fb[16]=MSRP_LEN_DOMAIN_C;
      fb[17]=MSRP_ALL_DOMAIN_C[15:8];  fb[18]=MSRP_ALL_DOMAIN_C[7:0];
      fb[19]=vh[15:8]; fb[20]=vh[7:0];
      fb[21]=SR_CLASS_A_ID_C;
      fb[22]=SR_CLASS_A_PRIO_C;
      fb[23]={4'h0, vid_i[11:8]}; fb[24]=vid_i[7:0];
      fb[25]=pack3(domain_evt_r);
      // fb[26..27] vector EndMark = 0
      if (talker_incl_r) begin
        // ---- Message 2: TalkerAdvertise (type 1, len 25, listlen 30) ----
        fb[28]=MSRP_ATTR_TALKER_ADV_C;
        fb[29]=MSRP_LEN_TALKER_ADV_C;
        fb[30]=MSRP_ALL_TALKER_ADV_C[15:8]; fb[31]=MSRP_ALL_TALKER_ADV_C[7:0];
        fb[32]=vh[15:8]; fb[33]=vh[7:0];
        // StreamID = {station MAC, unique_id} — byte-identical to the AVTP
        // header + ACMP responses ({mac,uid} formula, stream_id bug 07-14)
        fb[34]=station_mac_i[47:40]; fb[35]=station_mac_i[39:32];
        fb[36]=station_mac_i[31:24]; fb[37]=station_mac_i[23:16];
        fb[38]=station_mac_i[15:8];  fb[39]=station_mac_i[7:0];
        fb[40]=unique_id_i[15:8];    fb[41]=unique_id_i[7:0];
        // DataFrameParameters { dest MAC, VID }
        fb[42]=dest_mac_i[47:40]; fb[43]=dest_mac_i[39:32];
        fb[44]=dest_mac_i[31:24]; fb[45]=dest_mac_i[23:16];
        fb[46]=dest_mac_i[15:8];  fb[47]=dest_mac_i[7:0];
        fb[48]={4'h0, vid_i[11:8]}; fb[49]=vid_i[7:0];
        // TSpec
        fb[50]=max_frame_i[15:8];       fb[51]=max_frame_i[7:0];
        fb[52]=interval_frames_i[15:8]; fb[53]=interval_frames_i[7:0];
        fb[54]=SR_PRIO_RANK_C;
        fb[55]=latency_i[31:24]; fb[56]=latency_i[23:16];
        fb[57]=latency_i[15:8];  fb[58]=latency_i[7:0];
        fb[59]=pack3(talker_evt_r);
        // fb[60..61] vector EndMark; message list continues at fb[62]
      end
      if (lstn_incl_r) begin
        // ---- Listener message (type 3, len 8, listlen 14) at lb ----
        fb[lb+0]=MSRP_ATTR_LISTENER_C;
        fb[lb+1]=MSRP_LEN_LISTENER_C;
        fb[lb+2]=MSRP_ALL_LISTENER_C[15:8]; fb[lb+3]=MSRP_ALL_LISTENER_C[7:0];
        fb[lb+4]=vh[15:8]; fb[lb+5]=vh[7:0];
        for (int k = 0; k < 8; k++) fb[lb+6+k]=lstn_sid_i[8*(7-k) +: 8];
        fb[lb+14]=pack3(lstn_evt_r);
        //! FourPacked declaration: Ready while the TalkerAdvertise is
        //! registered, AskingFailed otherwise (pipewire acmp_periodic rule)
        fb[lb+15]=pack4(lstn_ready_i ? LSTN_DECL_READY_C
                                     : LSTN_DECL_ASKING_FAIL_C);
        // fb[lb+16..17] vector EndMark; message-list EndMark after = 0
      end
      // (remaining bytes stay 0 = message-list EndMark + pad)
    end else begin
      // ---- MVRP: VID (type 1, len 2 — NO AttributeListLength) ----
      fb[12]=MVRP_ETHERTYPE_C[15:8]; fb[13]=MVRP_ETHERTYPE_C[7:0];
      fb[14]=MRP_PROTO_VER_C;
      fb[15]=MVRP_ATTR_VID_C;
      fb[16]=MVRP_LEN_VID_C;
      fb[17]=vh[15:8]; fb[18]=vh[7:0];
      fb[19]={4'h0, vid_i[11:8]}; fb[20]=vid_i[7:0];
      fb[21]=pack3(vid_evt_r);
      // fb[22..23] vector EndMark, fb[24..25] message-list EndMark = 0
    end
  end

  //! current beat, byte lane 0 = earliest on the wire
  logic [63:0] beat_data_w;
  always_comb begin
    for (int l = 0; l < 8; l++)
      beat_data_w[8*l +: 8] = fb[{beat_r, 3'b000} + 7'(l)];
  end

  always_comb begin
    m_axis_tvalid = (state_r == S_SEND);
    m_axis_tdata  = beat_data_w;
    m_axis_tlast  = (state_r == S_SEND) && (beat_r == frame_beats_w - 4'd1);
    if ((state_r == S_SEND) && (beat_r == frame_beats_w - 4'd1))
      m_axis_tkeep = 8'((16'd1 << last_keep_w) - 16'd1);
    else if (state_r == S_SEND)
      m_axis_tkeep = 8'hFF;
    else
      m_axis_tkeep = 8'h00;
  end

  // -----------------------------------------------------------------------
  // Trigger capture + serialiser
  // -----------------------------------------------------------------------
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      enable_q <= 1'b0; talker_q <= 1'b0; lstn_q <= 1'b0; lstn_ready_q <= 1'b0;
      msrp_pend_r <= 1'b0; mvrp_pend_r <= 1'b0; jdiv_r <= '0;
      talker_lv_pend_r <= 1'b0; lstn_lv_pend_r <= 1'b0;
      engine_lv_pend_r <= 1'b0; lva_pend_r <= 1'b0;
      fresh_domain_r <= 1'b0; fresh_vid_r <= 1'b0; fresh_talker_r <= 1'b0;
      fresh_lstn_r <= 1'b0;
      state_r <= S_IDLE; beat_r <= '0; gap_r <= '0;
      kind_r <= FK_MSRP_E; talker_incl_r <= 1'b0; lstn_incl_r <= 1'b0;
      lva_r <= 1'b0;
      domain_evt_r <= MRP_EVT_JOININ_C; talker_evt_r <= MRP_EVT_JOININ_C;
      vid_evt_r <= MRP_EVT_JOININ_C; lstn_evt_r <= MRP_EVT_JOININ_C;
      talker_declared_o <= 1'b0; lstn_declared_o <= 1'b0; tx_count_o <= 16'd0;
    end else begin
      enable_q <= enable_i;
      talker_q <= enable_i & talker_en_i;
      lstn_q   <= enable_i & lstn_declare_i;
      lstn_ready_q <= lstn_ready_i;

      // ---- triggers -> pending flags ----
      //! MRP quiescence: a healthy applicant re-declares on LeaveAll turns
      //! and state changes, not every JoinTime tick (the wire showed a
      //! constant 5.4 Hz re-declare spam). Keep a slow 1 s refresh (every
      //! 5th join tick) for lossy-link robustness.
      if (enable_i && join_tick_i)
        jdiv_r <= (jdiv_r == 3'd4) ? 3'd0 : jdiv_r + 3'd1;
      if (enable_rise_w) begin
        jdiv_r <= 3'd1;      //! prompt pair covers this period; refresh in 1 s
        lva_pend_r <= 1'b1;  //! fast state acquisition from the bridge
        fresh_domain_r <= 1'b1; fresh_vid_r <= 1'b1;
        if (talker_en_i) fresh_talker_r <= 1'b1;
        if (lstn_declare_i) fresh_lstn_r <= 1'b1;
        msrp_pend_r <= 1'b1; mvrp_pend_r <= 1'b1;   // declare promptly
      end
      if (talker_rise_w) begin
        fresh_talker_r <= 1'b1;
        msrp_pend_r <= 1'b1;
      end
      if (enable_i && lstn_declare_i && !lstn_q) begin
        fresh_lstn_r <= 1'b1;
        msrp_pend_r  <= 1'b1;
        //! fast join (2026-07-19): a NEW binding must learn the bridge's
        //! steady-state registrations (its TalkerAdvertise) NOW - only a
        //! LeaveAll forces an MRP applicant to re-declare, and waiting for
        //! the ~10 s timers made connect->reservation take 10-20 s. This
        //! turns it into ~one join-time.
        lva_pend_r   <= 1'b1;
        mvrp_pend_r  <= 1'b1;
      end
      // Ready <-> AskingFailed change re-declares promptly (the reference
      // re-joins the Listener attribute from acmp_periodic on param change)
      if (enable_i && lstn_declared_o && (lstn_ready_i ^ lstn_ready_q))
        msrp_pend_r <= 1'b1;
      if (enable_i && ((join_tick_i && jdiv_r == 3'd0) || rx_leaveall_i)) begin
        msrp_pend_r <= 1'b1; mvrp_pend_r <= 1'b1;
      end
      if (enable_i && leaveall_tick_i) begin
        lva_pend_r  <= 1'b1;
        msrp_pend_r <= 1'b1; mvrp_pend_r <= 1'b1;   // our LeaveAll turn
      end
      if (talker_fall_w && talker_declared_o) talker_lv_pend_r <= 1'b1;
      if (enable_i && !lstn_declare_i && lstn_q && lstn_declared_o)
        lstn_lv_pend_r <= 1'b1;
      if (enable_fall_w) begin
        engine_lv_pend_r <= 1'b1;
        // a stale declare pair must not fire after the withdraw
        msrp_pend_r <= 1'b0; mvrp_pend_r <= 1'b0; lva_pend_r <= 1'b0;
        fresh_domain_r <= 1'b0; fresh_vid_r <= 1'b0; fresh_talker_r <= 1'b0;
        fresh_lstn_r <= 1'b0;
      end

      // ---- serialiser ----
      case (state_r)
        S_IDLE: begin
          if (engine_lv_pend_r) begin
            // withdraw everything: MSRP LV (+talker/listener LV if declared)
            // then MVRP LV
            kind_r        <= FK_MSRP_E;
            talker_incl_r <= talker_declared_o;
            lstn_incl_r   <= lstn_declared_o;
            lva_r         <= 1'b0;
            domain_evt_r  <= MRP_EVT_LV_C;
            talker_evt_r  <= MRP_EVT_LV_C;
            lstn_evt_r    <= MRP_EVT_LV_C;
            engine_lv_pend_r <= 1'b0;
            mvrp_pend_r   <= 1'b1;             // follow with the MVRP LV
            vid_evt_r     <= MRP_EVT_LV_C;
            talker_declared_o <= 1'b0;
            lstn_declared_o   <= 1'b0;
            beat_r <= '0; state_r <= S_SEND;
          end else if (talker_lv_pend_r) begin
            kind_r        <= FK_MSRP_E;
            talker_incl_r <= 1'b1;
            lstn_incl_r   <= 1'b0;
            lva_r         <= 1'b0;
            domain_evt_r  <= MRP_EVT_JOININ_C; // domain stays declared
            talker_evt_r  <= MRP_EVT_LV_C;
            talker_lv_pend_r  <= 1'b0;
            talker_declared_o <= 1'b0;
            beat_r <= '0; state_r <= S_SEND;
          end else if (lstn_lv_pend_r) begin
            kind_r        <= FK_MSRP_E;
            talker_incl_r <= 1'b0;
            lstn_incl_r   <= 1'b1;
            lva_r         <= 1'b0;
            domain_evt_r  <= MRP_EVT_JOININ_C;
            lstn_evt_r    <= MRP_EVT_LV_C;
            lstn_lv_pend_r  <= 1'b0;
            lstn_declared_o <= 1'b0;
            beat_r <= '0; state_r <= S_SEND;
          end else if (msrp_pend_r) begin
            kind_r        <= FK_MSRP_E;
            talker_incl_r <= enable_i & talker_en_i;
            lstn_incl_r   <= enable_i & lstn_declare_i;
            lva_r         <= lva_pend_r;
            domain_evt_r  <= fresh_domain_r ? MRP_EVT_NEW_C : MRP_EVT_JOININ_C;
            talker_evt_r  <= fresh_talker_r ? MRP_EVT_NEW_C : MRP_EVT_JOININ_C;
            lstn_evt_r    <= fresh_lstn_r   ? MRP_EVT_NEW_C : MRP_EVT_JOININ_C;
            fresh_domain_r <= 1'b0;
            if (enable_i & talker_en_i) begin
              fresh_talker_r    <= 1'b0;
              talker_declared_o <= 1'b1;
            end
            if (enable_i & lstn_declare_i) begin
              fresh_lstn_r    <= 1'b0;
              lstn_declared_o <= 1'b1;
            end
            msrp_pend_r   <= 1'b0;
            beat_r <= '0; state_r <= S_SEND;
          end else if (mvrp_pend_r) begin
            kind_r        <= FK_MVRP_E;
            talker_incl_r <= 1'b0;
            lva_r         <= lva_pend_r;
            if (vid_evt_r != MRP_EVT_LV_C)     // engine-LV latched it already
              vid_evt_r   <= fresh_vid_r ? MRP_EVT_NEW_C : MRP_EVT_JOININ_C;
            fresh_vid_r   <= 1'b0;
            mvrp_pend_r   <= 1'b0;
            lva_pend_r    <= 1'b0;             // consumed by the pair's last frame
            beat_r <= '0; state_r <= S_SEND;
          end
        end

        S_SEND: begin
          if (m_axis_tready) begin
            if (beat_r == frame_beats_w - 4'd1) begin
              tx_count_o <= tx_count_o + 16'd1;
              if (kind_r == FK_MVRP_E) vid_evt_r <= MRP_EVT_JOININ_C;
              gap_r      <= 11'(GAP_CYCLES_C - 1);
              state_r    <= S_GAP;
            end else begin
              beat_r <= beat_r + 4'd1;
            end
          end
        end

        S_GAP: begin
          gap_r <= gap_r - 11'd1;
          if (gap_r == '0) state_r <= S_IDLE;
        end

        default: state_r <= S_IDLE;
      endcase
    end
  end

endmodule

`default_nettype wire
