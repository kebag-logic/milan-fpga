/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_usbnet_rx_copy.sv
  Description : The receive half of the USB network path (#1011): a COPY of
                the frames the device receives, filtered by
                KL_usbnet_pkg::rx_rule, toward the bus thread that carries
                them to the computer.
                PURE OBSERVER of the device's reception. The input is the
                accepted beat of the device's own receive stream (valid AND
                ready, sampled where the datapath takes it), so the device
                receives exactly what it received before, and a frame the
                computer cannot take is dropped here and counted, never
                pushed back.
                ONE PASS. Each beat, registered once on arrival, is written into a block-RAM
                frame buffer at a speculative pointer. On the frame's last
                beat the rule decides: a copied frame commits (its length
                enters the descriptor FIFO and the pointer advances), any
                other frame rolls back. A frame that meets a full buffer or a
                full descriptor FIFO is dropped whole (verdict RXV_FULL).
                THE BUS SIDE: a 16-bit stream, one record per frame: a header
                length word, then REC_FRAME_C, then the frame's octets
                two per word, the first octet in bits 7:0, the last word
                padded with zero when the length is odd. last is set on the
                record's final word, so a slave-FIFO master can end the USB
                transfer there (docs/design/USB_NET_PATH.md).
  Spec refs   : #1011 (receive filter); IEEE 1722-2016 Table 6; IEEE
                802.1Q-2018 8.6.3; docs/design/USB_NET_PATH.md
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//
`default_nettype none

module KL_usbnet_rx_copy
  import KL_usbnet_pkg::*;
#(
  parameter int unsigned DEPTH_P   = 512,   //! 64-bit words of frame buffer
  parameter int unsigned DESC_P    = 16,    //! frames the buffer can hold
  parameter int unsigned MAX_LEN_P = 1514   //! FX3 to_host record limit, octets
)(
  input  wire              clk_i,   //! the system clock, the MAC wrapper's
  input  wire              rst_ni,   //! synchronous reset, active low
  //! the device's receive stream, one accepted beat per valid
  input  wire              s_valid_i,
  input  wire [63:0]       s_data_i,
  input  wire [7:0]        s_keep_i,
  input  wire              s_last_i,
  //! the computer's address (KL_usbnet_tx_inject's station record)
  input  wire [47:0]       host_mac_i,
  input  wire              host_ok_i,
  //! toward the computer
  output logic             m_valid_o,
  input  wire              m_ready_i,
  output logic [15:0]      m_data_o,
  output logic             m_last_o,
  //! one verdict per received frame
  output logic             verdict_valid_o,
  output rx_verdict_e      verdict_o,
  output logic [15:0]      copied_o,        //! saturating
  output logic [15:0]      dropped_full_o   //! saturating
);
  //! TIMING: the observed beat is registered once before the rules read it, so
  //! the classification starts from a flop rather than from the MAC's FIFO
  //! memory. A copy has no latency to keep; one clock is free.
  logic        s_valid_q, s_last_q;
  logic [63:0] s_data_q;
  logic [7:0]  s_keep_q;
  always_ff @(posedge clk_i) begin : in_reg
    if (!rst_ni) s_valid_q <= 1'b0;
    else         s_valid_q <= s_valid_i;
    s_data_q <= s_data_i;
    s_keep_q <= s_keep_i;
    s_last_q <= s_last_i;
  end : in_reg

  localparam int unsigned AW_C = $clog2(DEPTH_P);
  localparam int unsigned DW_C = $clog2(DESC_P);

  if (MAX_LEN_P > 4095 || (MAX_LEN_P + 7) / 8 > DEPTH_P) begin : g_refuse
    $error("KL_usbnet_rx_copy: MAX_LEN_P=%0d must fit 12 bits and the buffer", MAX_LEN_P);
  end

  (* ram_style = "block" *) logic [63:0] ram_r [DEPTH_P];
  logic [AW_C:0] wr_ptr_r, wr_cur_r, rd_ptr_r;
  logic          in_frame_r, spoil_r, long_r;
  logic [11:0]   len_r;
  logic [1:0]    beat_r;
  logic [63:0]   b0_r, b1_r, b2_r;

  //! the descriptor FIFO: one length per committed frame
  logic [11:0]   desc_r [DESC_P];
  logic [DW_C:0] dwr_r, drd_r;
  wire           desc_full_w  = (dwr_r - drd_r) == (DW_C+1)'(DESC_P);
  wire           desc_empty_w = dwr_r == drd_r;

  function automatic logic [3:0] keep_octets(input logic [7:0] k);
    logic [3:0] n = '0;
    for (int i = 0; i < 8; i++) n += 4'(k[i]);
    return n;
  endfunction

  //! the header beats as they stand after this beat
  wire [63:0] b0_w = (s_valid_q && !in_frame_r)               ? s_data_q : b0_r;
  wire [63:0] b1_w = (s_valid_q && in_frame_r && beat_r == 1) ? s_data_q : b1_r;
  wire [63:0] b2_w = (s_valid_q && in_frame_r && beat_r == 2) ? s_data_q : b2_r;
  wire [191:0] hb_w = {b2_w, b1_w, b0_w};   //! octet n at bits 8n+7:8n

  function automatic hdr_t parse(input logic [191:0] o);
    hdr_t h;
    for (int i = 0; i < 6; i++) begin
      h.dst[47-8*i -: 8] = o[8*i     +: 8];
      h.src[47-8*i -: 8] = o[8*(6+i) +: 8];
    end
    h.etype = {o[8*12 +: 8], o[8*13 +: 8]};
    h.o14   = o[8*14 +: 8];
    h.o15   = o[8*15 +: 8];
    h.itype = {o[8*16 +: 8], o[8*17 +: 8]};
    h.o18   = o[8*18 +: 8];
    return h;
  endfunction

  wire [11:0]  base_w  = in_frame_r ? len_r : 12'd0;
  wire [12:0]  len_w   = {1'b0, base_w} + 13'(keep_octets(s_last_q ? s_keep_q : 8'hFF));
  wire         long_w  = len_w > 13'(MAX_LEN_P);
  //! ROLLBACK: a frame always starts at the committed pointer, so a frame
  //! that is not copied leaves nothing behind
  wire [AW_C:0] start_w = in_frame_r ? wr_cur_r : wr_ptr_r;
  wire         room_w  = (start_w - rd_ptr_r) != (AW_C+1)'(DEPTH_P);
  wire         spoil_w = (in_frame_r && spoil_r) || long_w || !room_w;
  rx_verdict_e rule_w;
  assign rule_w = rx_rule(parse(hb_w), len_w[11:0], host_mac_i, host_ok_i);
  wire         copy_w  = (rule_w == RXV_HOST) || (rule_w == RXV_GROUP);
  wire         fits_w  = !spoil_w && !desc_full_w;
  wire         too_long_w = (in_frame_r && long_r) || long_w;
  wire         commit_w = s_valid_q && s_last_q && copy_w && fits_w;

  always_ff @(posedge clk_i) begin : wr_desc
    if (commit_w) desc_r[dwr_r[DW_C-1:0]] <= len_w[11:0];
  end : wr_desc

  always_ff @(posedge clk_i) begin : wr_ram
    if (s_valid_q && !spoil_w) ram_r[start_w[AW_C-1:0]] <= s_data_q;
  end : wr_ram

  always_ff @(posedge clk_i) begin : wr_side
    if (!rst_ni) begin
      wr_ptr_r        <= '0;
      wr_cur_r        <= '0;
      in_frame_r      <= 1'b0;
      spoil_r         <= 1'b0;
      long_r          <= 1'b0;
      len_r           <= '0;
      beat_r          <= '0;
      b0_r            <= '0;
      b1_r            <= '0;
      b2_r            <= '0;
      dwr_r           <= '0;
      verdict_valid_o <= 1'b0;
      verdict_o       <= RXV_OFF;
      copied_o        <= '0;
      dropped_full_o  <= '0;
    end else begin
      verdict_valid_o <= 1'b0;
      if (s_valid_q) begin
        b0_r <= b0_w;
        b1_r <= b1_w;
        b2_r <= b2_w;
        if (s_last_q) begin
          in_frame_r      <= 1'b0;
          spoil_r         <= 1'b0;
          long_r          <= 1'b0;
          beat_r          <= '0;
          verdict_valid_o <= 1'b1;
          if (commit_w) begin
            verdict_o           <= rule_w;
            dwr_r               <= dwr_r + 1'b1;
            wr_ptr_r            <= start_w + 1'b1;
            wr_cur_r            <= start_w + 1'b1;
            if (copied_o != '1) copied_o <= copied_o + 1'b1;
          end else begin
            //! a frame longer than the limit is a shape the path does not
            //! carry, not a lack of room
            verdict_o <= !copy_w ? rule_w : too_long_w ? RXV_SHAPE : RXV_FULL;
            if (copy_w && !too_long_w && dropped_full_o != '1)
              dropped_full_o <= dropped_full_o + 1'b1;
          end
        end else begin
          in_frame_r <= 1'b1;
          spoil_r    <= spoil_w;
          long_r     <= too_long_w;
          len_r      <= long_w ? 12'(MAX_LEN_P + 1) : len_w[11:0];
          if (beat_r != 2'd3) beat_r <= beat_r + 1'b1;
          if (!spoil_w) wr_cur_r <= start_w + 1'b1;
        end
      end
    end
  end : wr_side

  // --------------------------------------------------------------------------
  //  The bus side
  // --------------------------------------------------------------------------
  typedef enum logic [1:0] {O_IDLE, O_HDR, O_KIND, O_DATA} ostate_e;
  ostate_e     ost_r;
  logic [10:0] words_r;          //! 16-bit words of the record still to send
  logic [1:0]  lane_r;
  logic [11:0] olen_r;
  logic [63:0] q_r;
  logic        q_ok_r;
  wire         take_w = m_valid_o && m_ready_i;
  wire         adv_w  = (ost_r == O_DATA) && take_w && (lane_r == 2'd3 || words_r == 11'd1);

  always_ff @(posedge clk_i) begin : rd_ram
    q_r <= ram_r[rd_ptr_r[AW_C-1:0]];
  end : rd_ram

  always_comb begin : bus_out
    m_valid_o = 1'b0;
    m_data_o  = 16'h0000;
    m_last_o  = 1'b0;
    case (ost_r)
      O_HDR: begin
        m_valid_o = 1'b1;
        m_data_o  = {4'b0, olen_r};
      end
      O_KIND: begin
        m_valid_o = 1'b1;
        m_data_o  = REC_FRAME_C;
      end
      O_DATA: begin
        m_valid_o = q_ok_r;
        m_data_o  = q_r[16*lane_r +: 16];
        //! the odd octet's partner is zero, never a stale octet
        if (words_r == 11'd1 && olen_r[0]) m_data_o[15:8] = 8'h00;
        m_last_o  = words_r == 11'd1;
      end
      default: ;
    endcase
  end : bus_out

  always_ff @(posedge clk_i) begin : rd_side
    if (!rst_ni) begin
      ost_r   <= O_IDLE;
      rd_ptr_r<= '0;
      drd_r   <= '0;
      words_r <= '0;
      lane_r  <= '0;
      olen_r  <= '0;
      q_ok_r  <= 1'b0;
    end else begin
      //! q_r holds rd_ptr_r's word one clock after the pointer last moved
      q_ok_r <= !adv_w;
      case (ost_r)
        O_IDLE: if (!desc_empty_w) begin
          olen_r  <= desc_r[drd_r[DW_C-1:0]];
          words_r <= 11'((desc_r[drd_r[DW_C-1:0]] + 12'd1) >> 1);
          lane_r  <= '0;
          ost_r   <= O_HDR;
        end
        O_HDR: if (take_w) ost_r <= O_KIND;
        O_KIND: if (take_w) ost_r <= O_DATA;
        O_DATA: if (take_w) begin
          lane_r  <= lane_r + 1'b1;
          words_r <= words_r - 1'b1;
          if (adv_w) rd_ptr_r <= rd_ptr_r + 1'b1;
          if (words_r == 11'd1) begin
            drd_r <= drd_r + 1'b1;
            ost_r <= O_IDLE;
          end
        end
        default: ost_r <= O_IDLE;
      endcase
    end
  end : rd_side

endmodule

`default_nettype wire
