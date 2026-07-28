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

                SR CLASS A TAGGING (vlan_en_i, 2026-07-28). The frame has
                TWO shapes, both exactly 60 octets before the FCS (the
                802.3 minimum, 64 on the wire) and both 8 AXIS beats - the
                tag replaces pad, it does not resize the frame:

                  vlan_en_i = 0  DA SA | 22F0 | CRF AVTPDU(28) | pad(18)
                  vlan_en_i = 1  DA SA | 8100 TCI | 22F0 | AVTPDU(28) | pad(14)

                The tagged shape is the 802.1Q C-TAG: TPID 0x8100 then the
                TCI {PCP[15:13], DEI[12], VID[11:0]}, with PCP = the SR
                class A priority (3) and VID = the SR VID that the MSRP
                Talker Advertise for this same stream declares in its
                DataFrameParameters - one wire feeds both, so the
                declaration and the frame can never disagree.

                *** vlan_en_i IS NOT A FREE SWITCH - AND THE OLD REASON
                GIVEN HERE WAS WRONG. *** This header used to say "an
                SR-tagged unregistered stream is pruned to zero ports by an
                AVB bridge". The bench measured the opposite and the repo
                already records it (docs/limitations/TROUBLESHOOTING.md,
                "Related bench fact worth knowing before blaming the
                board"): "An unregistered VLAN-2 stream DMAC is FLOODED by
                the bridge - a stream nobody registered still reaches every
                port at full rate, while a REGISTERED but listener-less
                stream is pruned." That is 802.1Q behaving as specified:
                pruning is what an MSRP registration BUYS (35.1.2 - a
                declared stream is forwarded only toward registered
                Listeners); with no registration the DMAC is just ordinary
                multicast and floods.

                So the real hazard of tagging alone is not disappearance,
                it is that the stream is moved INTO the reserved SR VLAN
                while still holding no reservation - unshaped, unaccounted,
                and now competing with real class A traffic - and it still
                floods, just to the SR VLAN's member ports. The reservation
                is what stops the flood; the tag is what makes the
                reservation apply to these frames. NEITHER HALF WORKS
                ALONE, so vlan_en_i must be derived FROM the declaration.
                milan_datapath ties it to the CRF stream's provisioned
                lwSRP talker row (crft_class_a_w), which makes the
                tagged-but-undeclared state unreachable rather than merely
                discouraged; the untagged shape stays the reset behaviour.

                vlan_en_i is LATCHED at frame launch beside ts_r/tu_r: a
                mid-frame layout change would emit a spliced frame.

  Spec refs   : Milan v1.2 7.3.1; IEEE 1722-2016 Clause 10;
                IEEE 802.1Q C-TAG format + PCP encoding; SR class A
                priority (default PCP 3)
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
  //! AVTP "tu" (timing uncertain), IEEE 1722-2016 10.4.5 - "behaves the same
  //! way as the tu field from the common stream header (4.4.4.7) except that
  //! it applies to the timestamps contained in the crf_data field". Our CRF
  //! timestamps come from the same PHC as AAF's, so they carry the same
  //! verdict. Latched at frame launch; drive 0 for the legacy wire bytes.
  input  wire         ts_uncertain_i,

  //! ---- SR class A 802.1Q C-TAG (see the header's trap note) -------------
  //! 1 = emit the tagged shape. milan_datapath drives this from the CRF
  //! stream's PROVISIONED lwSRP talker row, never from a bare CSR bit, so
  //! "tagged but undeclared" (the pruned-to-zero state) cannot be reached.
  input  wire         vlan_en_i,
  //! TCI priority_code_point (802.1Q 9.6, encoded on transmit per 6.9.3).
  //! SR class A default = 3 (802.1Q 34.5 / Table 34-1; Milan v1.2 4.2.7.2.1
  //! pins the MSRP Domain triple to {class A, priority 3, VID 2}).
  input  wire [2:0]   vlan_pcp_i,
  //! TCI VID (802.1Q 9.6). THE SAME WIRE that feeds the MSRP Talker
  //! Advertise DataFrameParameters for this stream (802.1Q 35.2.2.4), so
  //! the frame and its declaration cannot name different VLANs.
  input  wire [11:0]  vlan_vid_i,

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

  localparam int CRF_PDU_C   = 28;                      //! CRF AVTPDU octets
  localparam int ETH_HDR_C   = 14;                      //! DA + SA + EtherType
  localparam int VTAG_C      = 4;                        //! 802.1Q C-TAG (9.5)
  //! ONE frame length for BOTH shapes: the 802.3 minimum (60 + FCS = 64).
  //! The tag eats 4 octets of pad, so NUM_BEATS/LAST_KEEP/tkeep are
  //! identical tagged and untagged - the AXIS shape never moves.
  localparam int FRAME_BYTES = ETH_HDR_C + CRF_PDU_C + 18;     //! 60
  localparam int NUM_BEATS   = (FRAME_BYTES + 7) / 8;   //! 8
  localparam int LAST_KEEP   = FRAME_BYTES - (NUM_BEATS-1)*8;  //! 4
  //! The MSRP TSpec MaxFrameSize the integration must declare for this
  //! stream is FRAME_BYTES - (ETH_HDR_C + VTAG_C) = 42: the PADDED MSDU,
  //! not the 28-octet AVTPDU (802.1Q 35.2.2.4 TSpec; the engine's idleSlope
  //! adds the fixed 42 = preamble 8 + eth 14 + tag 4 + FCS 4 + IPG 12, so
  //! 42 + 42 = the 84-octet wire slot this frame really occupies).
  //! milan_datapath's CRF_SRP_MAXF_C carries that number.

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
  reg        tu_r;      //! tu frozen for the whole frame (latched with ts_r)
  //! tag shape frozen for the whole frame too - the tag moves every byte
  //! after offset 12, so a mid-frame change would splice two layouts
  reg        vln_r;
  reg [2:0]  vpcp_r;
  reg [11:0] vvid_r;

  //! CRF AVTPDU (IEEE 1722-2016 clause 10) - assembled ONCE, then placed at
  //! the offset the chosen Ethernet header ends at.
  logic [7:0] pdu [0:CRF_PDU_C-1];
  always_comb begin : crf_pdu_bytes
    pdu[0]=8'h04;                       // subtype CRF
    pdu[1]={7'h40, tu_r};               // sv=1, ver=0, mr=0, fs=0, tu (10.4.5)
    pdu[2]=seq_r;                       // sequence_num
    pdu[3]=8'h01;                       // type = CRF_AUDIO_SAMPLE (10.4.7)
    {pdu[4],pdu[5],pdu[6],pdu[7],pdu[8],pdu[9],pdu[10],pdu[11]} = sid_i;
    {pdu[12],pdu[13],pdu[14],pdu[15]} = {3'd0, CRF_BASEHZ_C}; // pull 0 | 48k
    {pdu[16],pdu[17]} = CRF_DLEN_C;     // crf_data_length (10.4.11)
    {pdu[18],pdu[19]} = CRF_IVAL_C;     // timestamp_interval (10.4.12)
    {pdu[20],pdu[21],pdu[22],pdu[23],pdu[24],pdu[25],pdu[26],pdu[27]} = ts_r;
  end : crf_pdu_bytes

  logic [7:0] fb [0:NUM_BEATS*8-1];
  always_comb begin : frame_bytes
    for (int k = 0; k < NUM_BEATS*8; k++) fb[k] = 8'h00;
    {fb[0],fb[1],fb[2],fb[3],fb[4],fb[5]} = dest_mac_i;
    {fb[6],fb[7],fb[8],fb[9],fb[10],fb[11]} = station_mac_i;
    if (vln_r) begin
      // 802.1Q C-TAG (9.5): TPID 0x8100, then the TCI (9.6) =
      // {PCP[15:13], DEI[12], VID[11:0]}. DEI 0 - an SR class A stream is
      // never drop-eligible.
      fb[12]=8'h81; fb[13]=8'h00;
      fb[14]={vpcp_r, 1'b0, vvid_r[11:8]}; fb[15]=vvid_r[7:0];
      fb[16]=8'h22; fb[17]=8'hF0;
      for (int k = 0; k < CRF_PDU_C; k++) fb[ETH_HDR_C+VTAG_C+k] = pdu[k];
      // fb[46..59] stay zero pad to the 60-byte minimum
    end
    else begin
      fb[12]=8'h22; fb[13]=8'hF0;
      for (int k = 0; k < CRF_PDU_C; k++) fb[ETH_HDR_C+k] = pdu[k];
      // fb[42..59] stay zero pad to the 60-byte minimum
    end
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
      ts_r <= '0; seq_r <= '0; frame_pend_r <= 1'b0; tu_r <= 1'b0;
      //! reset shape = UNTAGGED: a device that has not been told its
      //! reservation exists must not emit an SR-tagged stream
      vln_r <= 1'b0; vpcp_r <= 3'd0; vvid_r <= 12'd0;
      tx_count_o <= '0;
    end
    else begin
      if (evt_milan_w && enable_i && !frame_pend_r && (st_r == IDLE_S)) begin
        ts_r         <= ptp_ns_i + 64'(transit_ns_i);
        tu_r         <= ts_uncertain_i;   //! same PHC, same verdict
        vln_r        <= vlan_en_i;        //! shape frozen for this frame
        vpcp_r       <= vlan_pcp_i;
        vvid_r       <= vlan_vid_i;
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
