/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_aecp_ingress.sv
  Description : RX front-end for the AECP subsystem.

                Non-intrusive MONITOR of the MAC RX AXIS stream (Forencich
                little lane order, tdata[7:0] = first wire byte): it reads
                tvalid/tdata/tkeep/tlast and drives NOTHING back, so it can
                never backpressure or disturb the NIC RX path it taps.

                It store-and-forwards each frame into a byte buffer, then on
                tlast classifies it:

                  * AECP command for us  (ethertype 0x22F0, subtype 0xFB,
                    dst MAC == our station MAC): the frame from the EtherType
                    onward is replayed as a clean AXIS stream in BIG lane
                    order (tdata[63:56] = first byte) to the AECP validator —
                    the byte order the KL_aecp_* parser chain expects. The
                    controller's source MAC is captured for the response.

                  * ADP DISCOVER for us  (ethertype 0x22F0, subtype 0xFA,
                    message_type == ENTITY_DISCOVER, target_entity_id == 0 or
                    our entity_id): a one-cycle adp_discover_o pulse drives the
                    ADP advertiser's rcv_discover_i (no replay).

                Everything else is dropped. A second frame arriving while the
                buffer is busy is dropped (AECP is retried by controllers).

  Spec refs   : IEEE Std 1722.1-2021 §6 (ADP), §9 (AECP)
  Company     : Kebag Logic
  Project     : Milan ADP / AECP
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

import aecp_pkg::*;
import adp_pkg::*;

module KL_aecp_ingress #(
  //! Largest AECP command frame we buffer. In-scope commands top out at a
  //! SET_NAME (~98 wire bytes); 128 covers it and keeps the frame buffer (and
  //! its cross-module write route from the RX FIFO) small enough to close
  //! timing at 100 MHz. Larger frames overflow-drop (controllers retry).
  parameter int unsigned MAX_FRAME_BYTES = 128
) (
  input  wire          clk_i,
  input  wire          rst_n,
  input  wire          enable_i,

  // ---- identity ------------------------------------------------------
  input  wire [47:0]   station_mac_i,   //! [47:40] = first wire byte
  input  wire [63:0]   entity_id_i,

  // ---- RX monitor tap (little lane order; inputs only) ---------------
  input  wire          rx_tvalid_i,
  input  wire [63:0]   rx_tdata_i,
  input  wire [7:0]    rx_tkeep_i,
  input  wire          rx_tlast_i,

  // ---- replayed command stream to KL_aecp_packet_validator -----------
  output logic         m_axis_tvalid,
  input  wire          m_axis_tready,
  output logic [63:0]  m_axis_tdata,
  output logic [7:0]   m_axis_tkeep,
  output logic         m_axis_tlast,

  // ---- captured requester MAC (for the response builder) -------------
  output logic [47:0]  req_src_mac_o,
  output logic         req_valid_o,
  input  wire          req_pop_i,

  // ---- ADP discover-response trigger ---------------------------------
  output logic         adp_discover_o
);

  localparam int unsigned AW = $clog2(MAX_FRAME_BYTES);

  // ------------------------------------------------------------------ //
  // Input pipeline register on the tapped RX bus. The tap is a monitor  //
  // (never drives tready), so a 1-cycle delay is transparent; it breaks //
  // the long route from the RX FIFO storage to the frame buffer so the  //
  // placer can localize the buffer writes (the 100 MHz critical path).  //
  // ------------------------------------------------------------------ //
  logic        rxv_r, rxl_r;
  logic [63:0] rxd_r;
  logic [7:0]  rxk_r;
  always_ff @(posedge clk_i) begin
    rxv_r <= rx_tvalid_i;
    rxd_r <= rx_tdata_i;
    rxk_r <= rx_tkeep_i;
    rxl_r <= rx_tlast_i;
  end

  // frame byte buffer (wire order: buf[k] = k-th byte of the frame)
  logic [7:0] fbuf [0:MAX_FRAME_BYTES-1];
  logic [AW:0] wr_cnt_r;            //! bytes captured this frame
  logic        overflow_r;

  typedef enum logic [1:0] { COLLECT_S, CLASSIFY_S, REPLAY_S, HOLD_S } st_t;
  st_t state_r;

  // replay counters
  logic [AW:0] n_bytes_r;          //! total frame bytes
  logic [AW:0] rp_r;               //! stripped byte index (0 = wire byte 12)

  // ------------------------------------------------------------------ //
  // Classification fields (valid once wr_cnt_r covers them)              //
  // ------------------------------------------------------------------ //
  wire [15:0] w_etype   = {fbuf[12], fbuf[13]};
  wire [7:0]  w_subtype = fbuf[14];
  wire [3:0]  w_msgtype = fbuf[15][3:0];
  wire [47:0] w_dst_mac = {fbuf[0], fbuf[1], fbuf[2], fbuf[3], fbuf[4], fbuf[5]};
  wire [47:0] w_src_mac = {fbuf[6], fbuf[7], fbuf[8], fbuf[9], fbuf[10], fbuf[11]};
  //! ADP/AECP target_entity_id is at wire bytes 18..25 (ADPDU eid / AECP tgt)
  wire [63:0] w_tgt_eid = {fbuf[18], fbuf[19], fbuf[20], fbuf[21],
                           fbuf[22], fbuf[23], fbuf[24], fbuf[25]};

  wire w_for_us   = (w_dst_mac == station_mac_i);
  wire w_is_avtp  = (w_etype == AVTP_ETYPE_C);
  wire w_is_aecp  = w_is_avtp && (w_subtype == AECP_SUBTYPE_C) && w_for_us;
  wire w_is_adp_d = w_is_avtp && (w_subtype == 8'hFA) &&
                    (w_msgtype == 4'd2 /*ENTITY_DISCOVER*/) &&
                    ((w_tgt_eid == 64'd0) || (w_tgt_eid == entity_id_i));

  // ------------------------------------------------------------------ //
  // Replay (big lane order) — combinational outputs                      //
  // ------------------------------------------------------------------ //
  wire [AW:0] w_strip = n_bytes_r - (AW+1)'(12);   //! payload bytes to replay
  wire [AW:0] w_rem   = w_strip - rp_r;            //! bytes left this beat

  logic [63:0] w_beat;
  always_comb begin
    w_beat = 64'd0;
    for (int l = 0; l < 8; l++) begin
      // big lane order: stripped byte (rp_r + l) -> tdata[63-8l -: 8]
      if ((AW+1)'(l) < w_rem)
        w_beat[8*(7-l) +: 8] = fbuf[(32)'(12) + (32)'(rp_r) + l];
    end
  end

  logic [7:0] w_keep;
  always_comb begin
    w_keep = 8'h00;
    for (int l = 0; l < 8; l++)
      if ((AW+1)'(l) < w_rem) w_keep[7-l] = 1'b1;   // MSB lane = first byte
  end

  assign m_axis_tvalid = (state_r == REPLAY_S);
  assign m_axis_tdata  = w_beat;
  assign m_axis_tkeep  = w_keep;
  assign m_axis_tlast  = (state_r == REPLAY_S) && (w_rem <= (AW+1)'(8));
  // ------------------------------------------------------------------ //
  // FSM                                                                  //
  // ------------------------------------------------------------------ //
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      state_r        <= COLLECT_S;
      wr_cnt_r       <= '0;
      overflow_r     <= 1'b0;
      n_bytes_r      <= '0;
      rp_r           <= '0;
      req_src_mac_o  <= 48'd0;
      req_valid_o    <= 1'b0;
      adp_discover_o <= 1'b0;
      for (int k = 0; k < MAX_FRAME_BYTES; k++) fbuf[k] <= 8'h00;
    end else begin
      adp_discover_o <= 1'b0;
      if (req_pop_i) req_valid_o <= 1'b0;

      case (state_r)
        // ---------------------------------------------------------- //
        COLLECT_S: begin
          if (rxv_r) begin
            for (int l = 0; l < 8; l++) begin
              if (rxk_r[l] && !overflow_r &&
                  (wr_cnt_r + (AW+1)'(l) < (AW+1)'(MAX_FRAME_BYTES)))
                fbuf[wr_cnt_r + (AW+1)'(l)] <= rxd_r[8*l +: 8];
            end
            if (wr_cnt_r + count_keep(rxk_r) > (AW+1)'(MAX_FRAME_BYTES))
              overflow_r <= 1'b1;
            wr_cnt_r <= wr_cnt_r + count_keep(rxk_r);
            if (rxl_r) begin
              n_bytes_r <= wr_cnt_r + count_keep(rxk_r);
              state_r   <= CLASSIFY_S;
            end
          end
        end

        // ---------------------------------------------------------- //
        CLASSIFY_S: begin
          // default: recycle the buffer for the next frame
          wr_cnt_r   <= '0;
          overflow_r <= 1'b0;
          state_r    <= COLLECT_S;

          if (!enable_i || overflow_r || n_bytes_r < (AW+1)'(28)) begin
            // too short / disabled / lost bytes — drop
          end else if (w_is_aecp && !req_valid_o) begin
            req_src_mac_o <= w_src_mac;
            rp_r          <= '0;
            state_r       <= REPLAY_S;
          end else if (w_is_adp_d) begin
            adp_discover_o <= 1'b1;   // pulse the advertiser
          end
        end

        // ---------------------------------------------------------- //
        REPLAY_S: begin
          if (m_axis_tready) begin
            if (w_rem <= (AW+1)'(8)) begin
              req_valid_o <= 1'b1;    // requester MAC now valid for the builder
              state_r     <= HOLD_S;
            end else begin
              rp_r <= rp_r + (AW+1)'(8);
            end
          end
        end

        // ---------------------------------------------------------- //
        HOLD_S: begin
          // buffer is free to collect the next frame immediately; the
          // captured src MAC is held until the builder pops it.
          state_r <= COLLECT_S;
        end

        default: state_r <= COLLECT_S;
      endcase
    end
  end

  function automatic [AW:0] count_keep(input [7:0] k);
    count_keep = '0;
    for (int l = 0; l < 8; l++) count_keep = count_keep + {{AW{1'b0}}, k[l]};
  endfunction

endmodule

`default_nettype wire
