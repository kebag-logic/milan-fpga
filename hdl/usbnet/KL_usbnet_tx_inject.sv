/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_usbnet_tx_inject.sv
  Description : The transmit half of the USB network path (#1011): the
                records the computer's side sends over its bus thread, the
                frames among them checked by KL_usbnet_pkg::tx_rule, and the
                passing frames handed whole, at a limited rate, to the
                best-effort injection port (KL_usbnet_tx_arb).
                THE RECORDS (docs/design/USB_NET_PATH.md). Each starts with
                one 16-bit header word {type[3:0], length in octets[11:0]}
                and carries that many octets, two per word, the first octet
                in bits 7:0. The bus has no packet boundary, so the length is
                the only framing.
                  REC_FRAME_C   an Ethernet frame without its FCS.
                  REC_HOST_C    8 octets: the computer's address (6) and a
                                16-bit USB state word, first octet first.
                                Bit 0 of the state word: configured at
                                SuperSpeed. Bit 1: the network function is
                                active. Sent at every connection and then at
                                least once a second.
                  REC_DETACH_C  0 octets: the computer left.
                Any other type, or a host or detach record of the wrong
                length, is skipped by its length and counted.
                WHOLE FRAMES ONLY. A frame header is held until the buffer
                has room for the whole frame (backpressure, never a drop),
                so a frame leaves gapless or not at all. The rule decides on
                the last word; a dropped frame rolls back.
                THE RATE LIMIT. A token bucket in octets on the wire (the
                frame, at least 60 octets, plus 24 octets of preamble, FCS
                and interframe gap) refilled at RATE_BPS_P and capped at
                BURST_OCTETS_P. A frame waits until the bucket holds its
                cost; nothing is dropped for rate.
  Spec refs   : #1011 (transmit inject); IEEE 802.3-2022 4.4.2 (Table 4-2,
                interframe gap); IEEE 802.1Q-2018 8.6.6, Table 8-5;
                docs/design/USB_NET_PATH.md
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//
`default_nettype none

module KL_usbnet_tx_inject
  import KL_usbnet_pkg::*;
#(
  parameter int unsigned  CLK_HZ_P        = 80_000_000,
  parameter longint unsigned RATE_BPS_P   = 64'd10_000_000,   //! wire bits per second
  parameter int unsigned  BURST_OCTETS_P  = 3200,
  parameter int unsigned  DEPTH_P         = 512,          //! 64-bit words of frame buffer
  parameter int unsigned  DESC_P          = 16,
  parameter int unsigned  MAX_LEN_P       = 1518,         //! a tagged frame without its FCS
  parameter int unsigned  HOST_TIMEOUT_MS_P = 3000
)(
  input  wire              clk_i,
  input  wire              rst_ni,
  //! from the computer's side
  input  wire              s_valid_i,
  output logic             s_ready_o,
  input  wire [15:0]       s_data_i,
  //! toward the injection port
  output logic             m_valid_o,
  input  wire              m_ready_i,
  output logic [63:0]      m_data_o,
  output logic [7:0]       m_keep_o,
  output logic             m_last_o,
  //! the host record
  output logic [47:0]      host_mac_o,
  output logic             host_ok_o,      //! an address is held
  output logic [15:0]      host_state_o,   //! the last USB state word
  output logic             host_fresh_o,   //! a host record arrived within the timeout
  //! one verdict per frame record
  output logic             verdict_valid_o,
  output tx_verdict_e      verdict_o,
  output logic [15:0]      passed_o,
  output logic [15:0]      dropped_o,
  output logic [15:0]      skipped_o       //! records of an unknown type or length
);
  localparam int unsigned AW_C = $clog2(DEPTH_P);
  localparam int unsigned DW_C = $clog2(DESC_P);
  localparam int unsigned FRAC_C = 16;
  //! octets on the wire per clock, Q.16
  localparam longint unsigned INC_C =
      (RATE_BPS_P * (longint'(1) << FRAC_C) + 4 * longint'(CLK_HZ_P)) / (8 * longint'(CLK_HZ_P));
  localparam int unsigned TOK_W_C = $clog2(BURST_OCTETS_P + 1) + FRAC_C + 1;
  localparam logic [TOK_W_C-1:0] CAP_C = TOK_W_C'(longint'(BURST_OCTETS_P) << FRAC_C);
  localparam int unsigned MS_CYC_C = CLK_HZ_P / 1000;

  if (BURST_OCTETS_P < MAX_LEN_P + 24 || INC_C == 0 || MAX_LEN_P > 4095
      || (MAX_LEN_P + 7) / 8 > DEPTH_P) begin : g_refuse
    $error("KL_usbnet_tx_inject: the burst must hold one longest frame, the rate must be nonzero");
  end

  (* ram_style = "block" *) logic [63:0] ram_r [DEPTH_P];
  logic [AW_C:0] wr_ptr_r, wr_cur_r, rd_ptr_r;
  logic [11:0]   desc_r [DESC_P];
  logic [DW_C:0] dwr_r, drd_r;
  wire           desc_full_w  = (dwr_r - drd_r) == (DW_C+1)'(DESC_P);
  wire           desc_empty_w = dwr_r == drd_r;

  // --------------------------------------------------------------------------
  //  The record parser
  // --------------------------------------------------------------------------
  typedef enum logic [2:0] {P_HDR, P_ROOM, P_DATA, P_HOST, P_SKIP} pstate_e;
  pstate_e     pst_r;
  logic [11:0] len_r;
  logic [10:0] left_r;        //! words of the record still to take
  logic [10:0] widx_r;        //! word index inside the record
  logic [63:0] beat_r;
  logic [7:0]  hb_r [HDR_OCTETS_C + 1];   //! octets 0 to 19
  logic [47:0] mac_r;
  logic [15:0] ms_r;
  logic [$clog2(MS_CYC_C)-1:0] div_r;

  wire        take_w  = s_valid_i && s_ready_o;
  wire [3:0]  rtype_w = s_data_i[15:12];
  wire [11:0] rlen_w  = s_data_i[11:0];
  wire [10:0] rwords_w = 11'((rlen_w + 12'd1) >> 1);
  wire        last_w  = left_r == 11'd1;
  wire [AW_C:0] used_w = wr_cur_r - rd_ptr_r;
  wire [AW_C:0] need_w = (AW_C+1)'((len_r + 12'd7) >> 3);
  wire        room_w  = ((AW_C+1)'(DEPTH_P) - used_w) >= need_w && !desc_full_w;

  //! the header octets with this word in place
  logic [7:0] hn_w [HDR_OCTETS_C + 1];
  always_comb begin : hdr_next
    for (int i = 0; i <= HDR_OCTETS_C; i++) hn_w[i] = hb_r[i];
    if (pst_r == P_DATA && take_w && widx_r < 11'd10) begin
      hn_w[2*widx_r]     = s_data_i[7:0];
      hn_w[2*widx_r + 1] = s_data_i[15:8];
    end
  end : hdr_next

  hdr_t hdr_w;
  always_comb begin : hdr_parse
    for (int i = 0; i < 6; i++) begin
      hdr_w.dst[47-8*i -: 8] = hn_w[i];
      hdr_w.src[47-8*i -: 8] = hn_w[6+i];
    end
    hdr_w.etype = {hn_w[12], hn_w[13]};
    hdr_w.o14   = hn_w[14];
    hdr_w.o15   = hn_w[15];
    hdr_w.itype = {hn_w[16], hn_w[17]};
    hdr_w.o18   = hn_w[18];
  end : hdr_parse

  tx_verdict_e rule_w;
  assign rule_w = tx_rule(hdr_w, len_r, host_mac_o, host_ok_o);

  //! the beat with this word in its lane
  wire [1:0]  lane_w = widx_r[1:0];
  logic [63:0] bn_w;
  always_comb begin : beat_next
    bn_w = beat_r;
    bn_w[16*lane_w +: 16] = s_data_i;
    //! an odd length: the pad octet is not frame data
    if (last_w && len_r[0]) bn_w[16*lane_w + 8 +: 8] = 8'h00;
  end : beat_next
  wire wr_beat_w = (pst_r == P_DATA) && take_w && (lane_w == 2'd3 || last_w);
  wire commit_w  = (pst_r == P_DATA) && take_w && last_w && (rule_w == TXV_PASS);

  always_ff @(posedge clk_i) begin : wr_ram
    if (wr_beat_w) ram_r[wr_cur_r[AW_C-1:0]] <= bn_w;
  end : wr_ram

  always_ff @(posedge clk_i) begin : wr_desc
    if (commit_w) desc_r[dwr_r[DW_C-1:0]] <= len_r;
  end : wr_desc

  always_comb begin : ready
    case (pst_r)
      P_HDR, P_DATA, P_HOST, P_SKIP: s_ready_o = 1'b1;
      default:                       s_ready_o = 1'b0;   //! P_ROOM
    endcase
  end : ready

  always_ff @(posedge clk_i) begin : parser
    if (!rst_ni) begin
      pst_r           <= P_HDR;
      len_r           <= '0;
      left_r          <= '0;
      widx_r          <= '0;
      beat_r          <= '0;
      for (int i = 0; i <= HDR_OCTETS_C; i++) hb_r[i] <= '0;
      mac_r           <= '0;
      wr_ptr_r        <= '0;
      wr_cur_r        <= '0;
      dwr_r           <= '0;
      host_mac_o      <= '0;
      host_ok_o       <= 1'b0;
      host_state_o    <= '0;
      ms_r            <= 16'hFFFF;
      div_r           <= '0;
      verdict_valid_o <= 1'b0;
      verdict_o       <= TXV_PASS;
      passed_o        <= '0;
      dropped_o       <= '0;
      skipped_o       <= '0;
    end else begin
      verdict_valid_o <= 1'b0;
      //! milliseconds since the last host record, saturating
      if (div_r == ($clog2(MS_CYC_C))'(MS_CYC_C - 1)) begin
        div_r <= '0;
        if (ms_r != 16'hFFFF) ms_r <= ms_r + 1'b1;
      end else begin
        div_r <= div_r + 1'b1;
      end
      case (pst_r)
        P_HDR: if (take_w) begin
          len_r  <= rlen_w;
          left_r <= rwords_w;
          widx_r <= '0;
          unique case (1'b1)
            rtype_w == REC_FRAME_C: begin
              if (rlen_w < 12'd14 || rlen_w > 12'(MAX_LEN_P)) begin
                verdict_valid_o <= 1'b1;
                verdict_o       <= TXV_LENGTH;
                if (dropped_o != '1) dropped_o <= dropped_o + 1'b1;
                pst_r <= (rlen_w == 12'd0) ? P_HDR : P_SKIP;
              end else begin
                pst_r <= P_ROOM;
              end
            end
            rtype_w == REC_HOST_C && rlen_w == 12'd8: pst_r <= P_HOST;
            rtype_w == REC_DETACH_C && rlen_w == 12'd0: begin
              host_ok_o    <= 1'b0;
              host_mac_o   <= '0;
              host_state_o <= '0;
              ms_r         <= 16'hFFFF;
            end
            default: begin
              if (skipped_o != '1) skipped_o <= skipped_o + 1'b1;
              pst_r <= (rlen_w == 12'd0) ? P_HDR : P_SKIP;
            end
          endcase
        end
        P_ROOM: if (room_w) begin
          pst_r    <= P_DATA;
          wr_cur_r <= wr_ptr_r;
          beat_r   <= '0;
        end
        P_DATA: if (take_w) begin
          for (int i = 0; i <= HDR_OCTETS_C; i++) hb_r[i] <= hn_w[i];
          beat_r <= (lane_w == 2'd3) ? 64'd0 : bn_w;
          widx_r <= widx_r + 1'b1;
          left_r <= left_r - 1'b1;
          if (wr_beat_w) wr_cur_r <= wr_cur_r + 1'b1;
          if (last_w) begin
            pst_r           <= P_HDR;
            verdict_valid_o <= 1'b1;
            verdict_o       <= rule_w;
            if (commit_w) begin
              dwr_r    <= dwr_r + 1'b1;
              wr_ptr_r <= wr_cur_r + 1'b1;
              if (passed_o != '1) passed_o <= passed_o + 1'b1;
            end else begin
              wr_cur_r <= wr_ptr_r;
              if (dropped_o != '1) dropped_o <= dropped_o + 1'b1;
            end
          end
        end
        P_HOST: if (take_w) begin
          widx_r <= widx_r + 1'b1;
          left_r <= left_r - 1'b1;
          case (widx_r[1:0])
            2'd0: mac_r[47:32] <= {s_data_i[7:0], s_data_i[15:8]};
            2'd1: mac_r[31:16] <= {s_data_i[7:0], s_data_i[15:8]};
            2'd2: mac_r[15:0]  <= {s_data_i[7:0], s_data_i[15:8]};
            default: begin
              pst_r <= P_HDR;
              if (host_mac_ok(mac_r)) begin
                host_mac_o   <= mac_r;
                host_ok_o    <= 1'b1;
                //! the state word: its first octet is its low byte
                host_state_o <= s_data_i;
                ms_r         <= '0;
              end else begin
                //! an unusable address detaches the computer: no stale one is kept
                host_ok_o    <= 1'b0;
                host_mac_o   <= '0;
                host_state_o <= '0;
                ms_r         <= 16'hFFFF;
                if (skipped_o != '1) skipped_o <= skipped_o + 1'b1;
              end
            end
          endcase
        end
        P_SKIP: if (take_w) begin
          left_r <= left_r - 1'b1;
          if (last_w) pst_r <= P_HDR;
        end
        default: pst_r <= P_HDR;
      endcase
    end
  end : parser

  assign host_fresh_o = host_ok_o && (ms_r < 16'(HOST_TIMEOUT_MS_P));

  // --------------------------------------------------------------------------
  //  The injection side
  // --------------------------------------------------------------------------
  logic [TOK_W_C-1:0] tok_r;
  logic               send_r;
  logic [2:0]         olen_r;   //! the length's octets past the last whole beat
  logic [8:0]         beats_r;    //! 64-bit beats still to send
  logic [63:0]        q_r;
  wire [11:0]         dlen_w  = desc_r[drd_r[DW_C-1:0]];
  wire [11:0]         wire_w  = ((dlen_w < 12'd60) ? 12'd60 : dlen_w) + 12'd24;
  wire [TOK_W_C-1:0]  cost_w  = TOK_W_C'(longint'(wire_w) << FRAC_C);
  wire                start_w = !send_r && !desc_empty_w && tok_r >= cost_w;
  wire                beat_w  = m_valid_o && m_ready_i;
  wire [2:0]          tail_w  = olen_r[2:0];
  //! GAPLESS: the read looks one word ahead, so q_r always holds the word at
  //! rd_ptr_r and a frame leaves one beat per clock, as the MAC core's
  //! transmit side requires (it has no underrun handling inside a frame)
  wire [AW_C:0]       rd_next_w = beat_w ? rd_ptr_r + 1'b1 : rd_ptr_r;

  always_ff @(posedge clk_i) begin : rd_ram
    q_r <= ram_r[rd_next_w[AW_C-1:0]];
  end : rd_ram

  assign m_valid_o = send_r;
  assign m_data_o  = q_r;
  assign m_last_o  = beats_r == 9'd1;
  assign m_keep_o  = (m_last_o && tail_w != 3'd0) ? 8'((9'd1 << tail_w) - 9'd1) : 8'hFF;

  always_ff @(posedge clk_i) begin : injector
    if (!rst_ni) begin
      tok_r    <= CAP_C;
      send_r   <= 1'b0;
      olen_r   <= '0;
      beats_r  <= '0;
      rd_ptr_r <= '0;
      drd_r    <= '0;
    end else begin
      if (start_w) begin
        tok_r   <= tok_r - cost_w;
        send_r  <= 1'b1;
        olen_r  <= dlen_w[2:0];
        beats_r <= 9'((dlen_w + 12'd7) >> 3);
      end else if (tok_r < CAP_C) begin
        tok_r <= (CAP_C - tok_r < TOK_W_C'(INC_C)) ? CAP_C : tok_r + TOK_W_C'(INC_C);
      end
      if (beat_w) begin
        rd_ptr_r <= rd_ptr_r + 1'b1;
        beats_r  <= beats_r - 1'b1;
        if (m_last_o) begin
          send_r <= 1'b0;
          drd_r  <= drd_r + 1'b1;
        end
      end
    end
  end : injector

endmodule

`default_nettype wire
