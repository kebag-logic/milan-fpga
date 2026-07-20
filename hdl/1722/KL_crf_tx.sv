/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_crf_tx.sv
  Description : Milan CRF Media Clock Output engine (talker half).

                Emits the Avnu Pro Audio CRF Media Clock Stream (Milan v1.2
                7.3.1 / IEEE 1722-2016 Clause 10): subtype 4, type
                CRF_AUDIO_SAMPLE (1), pull 0, base_frequency 48000,
                crf_data_length 8 (one 64-bit timestamp per PDU),
                timestamp_interval 96 => one PDU per 96 media-clock events
                = 500 PDUs/s.

                The timestamp grid is the REAL media clock: a self-contained
                /512 divider of clk_audio_i (24.576 MHz MMCM => 48.000 kHz
                sample ticks, the same derivation as the I2S front-ends)
                counts 96 sample events, and each 96th event crosses into
                cd_milan (cdc_pulse) where ptp_ns_i is latched as that
                event's gPTP time. The stream therefore carries the actual
                audio-MMCM rate as seen by the PHC - a listener's KL_crf_rx
                measures the true media-clock/gPTP ratio, not a synthetic
                2 ms accumulator.

                Milan applies the stream PRESENTATION TIME OFFSET to CRF
                timestamps exactly as it does to media streams (USER
                2026-07-20; Milan 7.3.2 profiles [AVTP Clause 10]): each
                emitted timestamp = event gPTP time + transit_ns_i, so the
                listener steers its 48 kHz recovery clock against
                future-dated targets in the same ts_delta regime as AAF.
                transit_ns_i is the SAME offset source as the AAF framer
                (SET_STREAM_INFO MSRP_ACC_LAT / MTT 0x4C-0x4D; reset 2 ms).

                An event that lands while the previous frame still waits on
                the AXIS master is skipped whole: the NEXT emitted PDU still
                carries a real event time, so the receiver's rate window
                (ts-field derived) stays truthful; only the PDU cadence
                stretches. sequence_num increments per EMITTED PDU (no rx
                seq_err on a skip).

                Frames leave untagged on the low-rate control lane (60 B,
                zero-padded): the CRF stream has no MSRP Talker declaration
                yet, and an SR-tagged unregistered stream is pruned to zero
                ports by an AVB bridge, while untagged multicast floods -
                honest best-effort until the 2nd lwSRP talker attr lands.

  Spec refs   : Milan v1.2 7.3.1; IEEE 1722-2016 Clause 10
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

module KL_crf_tx (
  input  wire         clk_i,             //! cd_milan datapath clock
  input  wire         rst_n,
  input  wire         clk_audio_i,       //! clean MMCM audio clock (24.576 MHz)

  //! control (CSR 0x750 group)
  input  wire         enable_i,
  input  wire [63:0]  sid_i,             //! stream_id {MAC, uid} (CSR)
  input  wire [47:0]  dest_mac_i,        //! MAAP-range multicast DMAC (CSR)
  input  wire [47:0]  station_mac_i,     //! src MAC ([47:40] first on wire)
  input  wire [31:0]  transit_ns_i,      //! presentation time offset added to every timestamp (Milan: PTO applies to CRF like any stream)

  input  wire [63:0]  ptp_ns_i,          //! live PHC nanoseconds (cd_milan)

  //! CRF frames out (64b AXIS little lane, low-rate control merge)
  output logic [63:0] m_axis_tdata,
  output logic [7:0]  m_axis_tkeep,
  output logic        m_axis_tvalid,
  output logic        m_axis_tlast,
  input  wire         m_axis_tready,

  output reg  [31:0]  tx_count_o         //! CRF PDUs completed on the wire side
);

  //! Milan 7.3.1 constants (mirror KL_crf_rx)
  localparam [28:0] CRF_BASEHZ_C = 29'd48000;
  localparam [15:0] CRF_DLEN_C   = 16'd8;
  localparam [15:0] CRF_IVAL_C   = 16'd96;

  localparam int FRAME_BYTES = 14 + 28 + 18;            //! eth + CRF PDU + pad = 60
  localparam int NUM_BEATS   = (FRAME_BYTES + 7) / 8;   //! 8
  localparam int LAST_KEEP   = FRAME_BYTES - (NUM_BEATS-1)*8;  //! 4

  // -----------------------------------------------------------------------
  // Audio-domain event grid: /512 sample tick (48 kHz), /96 event pulse
  // (2 ms). Independent divider, same clock as the I2S front-ends: equal
  // long-term rate, arbitrary (constant) phase vs LRCK - CRF conveys the
  // media CLOCK, media anchoring stays with the AAF presentation ts.
  // -----------------------------------------------------------------------
  logic [1:0] arst_n_r;                 //! audio-domain reset sync
  always_ff @(posedge clk_audio_i) begin : a_rst
    arst_n_r <= {arst_n_r[0], rst_n};
  end : a_rst

  logic [8:0] adiv_r;                   //! /512 -> 48 kHz sample grid
  logic [6:0] aevt_cnt_r;               //! 0..95 sample events per CRF PDU
  logic       aevt_p_r;                 //! 1-cycle pulse per 96th event
  always_ff @(posedge clk_audio_i) begin : a_evt
    if (!arst_n_r[1]) begin
      adiv_r <= '0; aevt_cnt_r <= '0; aevt_p_r <= 1'b0;
    end
    else begin
      aevt_p_r <= 1'b0;
      adiv_r   <= adiv_r + 1'b1;
      if (adiv_r == 9'h1FF) begin
        if (aevt_cnt_r == 7'(CRF_IVAL_C - 1)) begin
          aevt_cnt_r <= '0;
          aevt_p_r   <= 1'b1;
        end
        else begin
          aevt_cnt_r <= aevt_cnt_r + 1'b1;
        end
      end
    end
  end : a_evt

  //! 2 ms spacing >> synchroniser round trip: cdc_pulse contract holds
  wire evt_milan_w;
  cdc_pulse u_evt_cdc (
    .src_clk    (clk_audio_i),
    .src_rst_n  (arst_n_r[1]),
    .src_pulse  (aevt_p_r),
    .dest_clk   (clk_i),
    .dest_rst_n (rst_n),
    .dest_pulse (evt_milan_w)
  );

  // -----------------------------------------------------------------------
  // cd_milan: latch the event's gPTP time, then serialise one 60-byte PDU.
  // A busy serialiser skips the event whole (see header).
  // -----------------------------------------------------------------------
  reg [63:0] ts_r;
  reg [7:0]  seq_r;
  reg        frame_pend_r;

  logic [7:0] fb [0:NUM_BEATS*8-1];
  always_comb begin : frame_bytes
    for (int k = 0; k < NUM_BEATS*8; k++) fb[k] = 8'h00;
    // Ethernet (untagged)
    {fb[0],fb[1],fb[2],fb[3],fb[4],fb[5]} = dest_mac_i;
    {fb[6],fb[7],fb[8],fb[9],fb[10],fb[11]} = station_mac_i;
    fb[12]=8'h22; fb[13]=8'hF0;
    // CRF AVTPDU (IEEE 1722-2016 clause 10)
    fb[14]=8'h04;                       // subtype CRF
    fb[15]=8'h80;                       // sv=1, ver=0, mr=0, fs=0, tu=0
    fb[16]=seq_r;                       // sequence_num
    fb[17]=8'h01;                       // type = CRF_AUDIO_SAMPLE
    {fb[18],fb[19],fb[20],fb[21],fb[22],fb[23],fb[24],fb[25]} = sid_i;
    {fb[26],fb[27],fb[28],fb[29]} = {3'd0, CRF_BASEHZ_C};  // pull 0 | base 48k
    {fb[30],fb[31]} = CRF_DLEN_C;
    {fb[32],fb[33]} = CRF_IVAL_C;
    {fb[34],fb[35],fb[36],fb[37],fb[38],fb[39],fb[40],fb[41]} = ts_r;
    // fb[42..59] stay zero pad to the 60-byte minimum
  end : frame_bytes

  typedef enum logic [0:0] { IDLE_S, SEND_S } st_t;
  st_t st_r;
  reg [3:0] beat_r;
  logic [63:0] w_beat;
  always_comb
    for (int l = 0; l < 8; l++) w_beat[8*l +: 8] = fb[{28'd0, beat_r}*8 + l];

  assign m_axis_tdata  = w_beat;
  assign m_axis_tvalid = (st_r == SEND_S);
  assign m_axis_tlast  = (st_r == SEND_S) && (beat_r == NUM_BEATS-1);
  assign m_axis_tkeep  = (beat_r == NUM_BEATS-1) ? 8'((1 << LAST_KEEP) - 1) : 8'hFF;

  always_ff @(posedge clk_i or negedge rst_n) begin : engine
    if (!rst_n) begin
      st_r <= IDLE_S; beat_r <= '0;
      ts_r <= '0; seq_r <= '0; frame_pend_r <= 1'b0;
      tx_count_o <= '0;
    end
    else begin
      if (evt_milan_w && enable_i && !frame_pend_r && (st_r == IDLE_S)) begin
        ts_r         <= ptp_ns_i + 64'(transit_ns_i);
        frame_pend_r <= 1'b1;
      end
      if (!enable_i) begin
        frame_pend_r <= 1'b0;
      end

      case (st_r)
        IDLE_S: if (frame_pend_r) begin beat_r <= '0; st_r <= SEND_S; end
        SEND_S: if (m_axis_tready) begin
          if (beat_r == NUM_BEATS-1) begin
            st_r <= IDLE_S; frame_pend_r <= 1'b0;
            seq_r <= seq_r + 1'b1;
            tx_count_o <= tx_count_o + 1'b1;
          end
          else begin
            beat_r <= beat_r + 1'b1;
          end
        end
        default: st_r <= IDLE_S;
      endcase
    end
  end : engine

endmodule

`default_nettype wire
