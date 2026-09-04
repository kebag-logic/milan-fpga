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
                emitted timestamp = event gPTP time + the Max Transit Time
                offset, so the listener steers its 48 kHz recovery clock
                against future-dated targets in the same ts_delta regime as
                AAF. transit_ns_i is the SAME offset source as the AAF framer
                (SET_STREAM_INFO MSRP_ACC_LAT / MTT 0x4C-0x4D; reset 2 ms) -
                but unlike AAF it is not stamped raw: 10.7 Equation 14 rounds
                it UP to a whole number of media clock periods first (see the
                Equation 14 block below).

                An event that lands while the previous frame still waits on
                the AXIS master is skipped whole: the NEXT emitted PDU still
                carries a real event time, so the receiver's rate window
                (ts-field derived) stays truthful; only the PDU cadence
                stretches. sequence_num increments per EMITTED PDU (no rx
                seq_err on a skip).

                THE mr BIT (IEEE 1722-2016 10.4.3). mr is a LEVEL a CRF
                Talker toggles when the source of the media clock providing
                the samples changes, and it "shall remain in its new state
                for a minimum of eight (8) CRF AVTPDUs for a given continuous
                stream". Neither the toggle policy nor the hold lives here:
                one engine (KL_media_clock_restart) owns the whole 4.4.4.3 /
                10.4.3 family for every Stream Output this device has, CRF
                included, because the hold is per stream but the TARGET is
                per media clock - two talkers on one clock must never end up
                on opposite levels. This module's contract is only the two
                halves that are wire facts: mr_i is stamped into the
                alternative header, latched at launch so a level change
                cannot splice a frame, and mr_last_o reports the level the
                last COMPLETED PDU carried, which is the only thing the
                eight-PDU hold may count (2026-08-08, gh #62 H2b).

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

                vlan_en_i is LATCHED at frame launch beside ts_r/tu_r/mr_r: a
                mid-frame layout change would emit a spliced frame.

  Spec refs   : Milan v1.2 7.3.1; IEEE 1722-2016 Clause 10 (10.4.3 mr,
                10.4.5 tu, 10.7 Equation 14 + PICS Table F.16 CRF-3/5/19);
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
  //! the Max Transit Time (10.7 TTmax) this stream's timestamps are offset
  //! by. NOT stamped raw - Equation 14 rounds it up to a whole number of
  //! media clock periods first, in the sequential converter below, which is
  //! why this port may change at any time and the frame path never waits.
  input  wire [31:0]  transit_ns_i,

  input  wire [63:0]  ptp_ns_i,          //! live PHC nanoseconds (cd_milan)
  //! AVTP "tu" (timing uncertain), IEEE 1722-2016 10.4.5 - "behaves the same
  //! way as the tu field from the common stream header (4.4.4.7) except that
  //! it applies to the timestamps contained in the crf_data field". Our CRF
  //! timestamps come from the same PHC as AAF's, so they carry the same
  //! verdict. Latched at frame launch; drive 0 for the legacy wire bytes.
  input  wire         ts_uncertain_i,

  //! ---- mr (media clock restart), IEEE 1722-2016 10.4.3 ------------------
  //! the LEVEL to stamp: "toggled by the Talker each time a media clock
  //! restart is needed, and it stays at its new value until a new media
  //! clock restart is needed". The toggle policy AND the >= 8 PDU hold live
  //! in KL_media_clock_restart (one engine for every Stream Output, so two
  //! talkers on one media clock can never sit on opposite levels); this port
  //! is the level that engine currently grants THIS stream. Latched at frame
  //! launch beside ts_r/tu_r/vln_r - a flip mid-frame would emit a header
  //! byte the rest of the PDU does not belong to.
  input  wire         mr_i,
  //! tu from the last completed PDU. The diagnostic counter must sample the
  //! bit latched at launch, not ts_uncertain_i after the frame has departed.
  output logic        tu_last_o,
  //! ... and the level the last COMPLETED PDU carried, back to that engine.
  //! 10.4.3's hold counts CRF AVTPDUs THAT WENT OUT, and a frame already
  //! launched when the level flips still carries the old value: counting it
  //! toward the new value would put the new state on the wire for seven PDUs
  //! where the clause says eight. It is also the wire truth the Milan
  //! Table 5.4 MEDIA_RESET counter for this Stream Output scores.
  output logic        mr_last_o,

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

  output logic [31:0] tx_count_o         //! CRF PDUs completed on the wire side
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

  // =========================================================================
  //  IEEE 1722-2016 10.7, Equation (14): the Max Transit Time offset
  //
  //    T_CRF = T_S + ceil(TTmax / P) * P + T_C
  //
  //  P is the where-list's "nominal period of the clock source" - the MEDIA
  //  clock, NOT the 2 ms PDU spacing (reading it as the spacing would add up
  //  to 2 ms of gratuitous latency to the one stream whose whole job is a
  //  tight recovery target). T_C = 0 here: a CRF PDU carries a captured
  //  clock EVENT, nothing accumulates in a transmit buffer.
  //
  //  P IS NOT AN INTEGER NUMBER OF NANOSECONDS. At base_frequency 48 kHz it
  //  is 1e9/48000 = 62500/3 = 20833.333... ns, so the clause's arithmetic is
  //  exact-rational and an implementation has to round it exactly once, at
  //  the end, and round it UP - the clause states its own reason: "rounding
  //  up so that the Max Transit Time is not violated".
  //
  //    periods   = ceil(TTmax / P)   = ceil(TTmax * DEN / NUM)
  //    offset_ns = ceil(periods * P) = ceil(periods * NUM / DEN)
  //
  //  THE SUB-NANOSECOND CEILING BIAS, stated rather than hidden: offset_ns
  //  sits at most 1 ns (mean 2/3 ns at DEN = 3) above the exact real-valued
  //  periods * P. 10.8 bounds the alignment between a CRF timing point and
  //  the media-stream timestamps derived from it at +/- 5% of the media
  //  sample period = +/- 1041 ns here, so the bias is five orders of
  //  magnitude below the wander budget it could ever enter. Rounding the
  //  other way would place the timestamp BELOW the Max Transit Time, which
  //  is the one direction 10.7 forbids.
  //
  //  At the shipping default TTmax = 2 ms this is byte-identical to the raw
  //  offset the module used to stamp: 2000000 ns is exactly 96 periods, and
  //  96 periods is exactly 2000000 ns.
  // =========================================================================
  localparam int unsigned NS_PER_S_C = 1_000_000_000;
  //! P as an EXACT rational MCLK_NUM_C / MCLK_DEN_C nanoseconds, reduced
  //! from NS_PER_S_C / CRF_BASEHZ_C by a common factor. The factor is
  //! CHECKED rather than trusted - a reduction by something that does not
  //! divide BOTH exactly would silently change the period, and a period that
  //! is silently wrong is a stream that is silently late.
  localparam int unsigned MCLK_RED_C = 16_000;
  localparam int unsigned MCLK_NUM_C = NS_PER_S_C / MCLK_RED_C;            //! 62500
  localparam int unsigned MCLK_DEN_C = 32'(CRF_BASEHZ_C) / MCLK_RED_C;     //! 3

  if ((NS_PER_S_C % MCLK_RED_C) != 0 || (32'(CRF_BASEHZ_C) % MCLK_RED_C) != 0)
    begin : g_mclk_rational
      $error("KL_crf_tx: MCLK_RED_C=%0d does not divide BOTH 1e9 and base_frequency=%0d exactly, so MCLK_NUM_C/MCLK_DEN_C would not be the 10.7 media clock period.",
             MCLK_RED_C, CRF_BASEHZ_C);
    end : g_mclk_rational

  //! divider sizing, DERIVED from the two passes' worst-case numerators (a
  //! 64-bit elaboration computes them; nothing here is a written-down width)
  localparam longint unsigned TT_MAX_C   = 64'hFFFF_FFFF;
  localparam longint unsigned NUM1_MAX_C = TT_MAX_C * 64'(MCLK_DEN_C)
                                         + 64'(MCLK_NUM_C) - 64'd1;
  localparam longint unsigned PER_MAX_C  = NUM1_MAX_C / 64'(MCLK_NUM_C);
  localparam longint unsigned NUM2_MAX_C = PER_MAX_C * 64'(MCLK_NUM_C)
                                         + 64'(MCLK_DEN_C) - 64'd1;
  localparam int unsigned DIVW_C  = $clog2(((NUM1_MAX_C > NUM2_MAX_C)
                                             ? NUM1_MAX_C : NUM2_MAX_C) + 64'd1);
  localparam int unsigned PERW_C  = $clog2(PER_MAX_C + 64'd1);
  //! the partial remainder holds at most 2*divisor-1 (shift a bit in, then
  //! conditionally subtract); the larger of the two divisors is MCLK_NUM_C
  localparam int unsigned REMW_C  = $clog2(MCLK_NUM_C + 1) + 1;
  localparam int unsigned STEPW_C = $clog2(DIVW_C + 1);

  //! NOTE the offset is DIVW_C wide, not 32: rounding a 32-bit TTmax UP can
  //! land above 2^32-1 (the ceiling adds up to one media clock period). A
  //! 32-bit result would wrap and move the timestamp 4.29 s backwards, so
  //! the extra bits are kept and the 64-bit add below stays exact.
  logic [DIVW_C-1:0]  mtt_ofs_r;    //! ceil(periods * P) ns - what launches stamp
  logic [31:0]        mtt_seen_r;   //! the transit_ns_i this offset belongs to
  logic               mtt_valid_r;  //! at least one conversion has completed

  //! restoring shift-subtract divider, run twice per conversion
  logic [DIVW_C-1:0]  dv_num_r;
  logic [DIVW_C-1:0]  dv_quot_r;
  logic [REMW_C-1:0]  dv_rem_r;
  logic [REMW_C-1:0]  dv_div_r;
  logic [STEPW_C-1:0] dv_step_r;
  logic               dv_busy_r;
  logic               dv_pass2_r;   //! 0 = TTmax -> periods, 1 = periods -> ns

  //! one restoring step, computed OUTSIDE the always_ff (house rule: no
  //! automatic temporaries in a clocked block)
  wire [REMW_C-1:0] dv_rsh_w = {dv_rem_r[REMW_C-2:0], dv_num_r[DIVW_C-1]};
  wire              dv_ge_w  = (dv_rsh_w >= dv_div_r);

  //! same reset FORM as the serialiser below (async, active low): rst_n is
  //! already an asynchronous reset for this clock domain in this module, and
  //! flopping one net both ways is a reset-recovery hazard, not a style
  //! preference
  always_ff @(posedge clk_i or negedge rst_n) begin : mtt_round
    if (!rst_n) begin
      mtt_ofs_r   <= '0;
      mtt_seen_r  <= '0;
      mtt_valid_r <= 1'b0;
      dv_num_r    <= '0;
      dv_quot_r   <= '0;
      dv_rem_r    <= '0;
      dv_div_r    <= '0;
      dv_step_r   <= '0;
      dv_busy_r   <= 1'b0;
      dv_pass2_r  <= 1'b0;
    end
    else if (!dv_busy_r) begin
      //! a NEW Max Transit Time - or the first one after reset. This is a
      //! REGISTER-RATE event (SET_STREAM_INFO / the CSR file), not a
      //! per-frame one, so the conversion runs once per change and the frame
      //! path stays a single 64-bit add.
      //! The !mtt_valid_r term is the POWER-ON conversion: mtt_ofs_r resets
      //! to 0, so until it completes a launch would stamp no transit offset
      //! at all. It cannot: the conversion is ~2*DIVW_C cycles and the first
      //! event is one whole 2 ms media-clock grid interval away (96 sample
      //! events of a 48 kHz grid), which is three orders of magnitude longer
      //! on any clk_i this module is built for.
      if (!mtt_valid_r || (transit_ns_i != mtt_seen_r)) begin
        mtt_seen_r <= transit_ns_i;
        dv_num_r   <= DIVW_C'(transit_ns_i) * DIVW_C'(MCLK_DEN_C)
                    + DIVW_C'(MCLK_NUM_C - 1);
        dv_div_r   <= REMW_C'(MCLK_NUM_C);
        dv_quot_r  <= '0;
        dv_rem_r   <= '0;
        dv_step_r  <= STEPW_C'(DIVW_C);
        dv_pass2_r <= 1'b0;
        dv_busy_r  <= 1'b1;
      end
    end
    else if (dv_step_r != '0) begin
      //! shift the next numerator bit into the partial remainder, subtract
      //! the divisor if it fits, shift the verdict into the quotient
      dv_rem_r  <= dv_ge_w ? (dv_rsh_w - dv_div_r) : dv_rsh_w;
      dv_quot_r <= {dv_quot_r[DIVW_C-2:0], dv_ge_w};
      dv_num_r  <= {dv_num_r[DIVW_C-2:0], 1'b0};
      dv_step_r <= dv_step_r - 1'b1;
    end
    else if (!dv_pass2_r) begin
      //! pass 1 answered ceil(TTmax / P) - the Equation 14 period count.
      //! Pass 2 turns it back into nanoseconds, rounded up again.
      dv_num_r   <= DIVW_C'(dv_quot_r[PERW_C-1:0]) * DIVW_C'(MCLK_NUM_C)
                  + DIVW_C'(MCLK_DEN_C - 1);
      dv_div_r   <= REMW_C'(MCLK_DEN_C);
      dv_quot_r  <= '0;
      dv_rem_r   <= '0;
      dv_step_r  <= STEPW_C'(DIVW_C);
      dv_pass2_r <= 1'b1;
    end
    else begin
      //! ... and only NOW does the launch path see the new number. Until
      //! this cycle every frame kept stamping the PREVIOUS rounded offset:
      //! a half-converted quotient is not a transit time, and a stream that
      //! stutters its offset for 70 cycles is worse than one that adopts it
      //! one PDU later.
      mtt_ofs_r   <= dv_quot_r;
      mtt_valid_r <= 1'b1;
      dv_busy_r   <= 1'b0;
    end
  end : mtt_round

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
  logic [63:0] ts_r;
  logic [7:0]  seq_r;
  logic        frame_pend_r;
  logic        tu_r;      //! tu frozen for the whole frame (latched with ts_r)
  //! ... and so is the 10.4.3 mr level: the engine may grant a new one at any
  //! cycle, and a frame whose header byte disagrees with the PDU it belongs
  //! to would corrupt both the listener's restart verdict and the hold count
  logic        mr_r;
  //! tag shape frozen for the whole frame too - the tag moves every byte
  //! after offset 12, so a mid-frame change would splice two layouts
  logic        vln_r;
  logic [2:0]  vpcp_r;
  logic [11:0] vvid_r;

  //! CRF AVTPDU (IEEE 1722-2016 clause 10) - assembled ONCE, then placed at
  //! the offset the chosen Ethernet header ends at.
  logic [7:0] pdu [0:CRF_PDU_C-1];
  always_comb begin : crf_pdu_bytes
    pdu[0]=8'h04;                       // subtype CRF
    //! alternative header byte 1: sv=1, version=0, mr (10.4.3), fs=0 (10.4.4
    //! is zero for CRF_AUDIO_SAMPLE), reserved, tu (10.4.5)
    pdu[1]={1'b1, 3'd0, mr_r, 2'b00, tu_r};
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
  logic [3:0] beat_r;
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
      //! reset mr = 0 is the wire's own reset state, and mr_last_o starts
      //! there too: no PDU has gone out, so nothing has been carried
      mr_r <= 1'b0; tu_last_o <= 1'b0; mr_last_o <= 1'b0;
      tx_count_o <= '0;
    end
    else begin
      if (evt_milan_w && enable_i && !frame_pend_r && (st_r == IDLE_S)) begin
        //! Equation 14: the ROUNDED offset, never the raw transit_ns_i. If a
        //! conversion is in flight this is still the previous whole answer.
        ts_r         <= ptp_ns_i + 64'(mtt_ofs_r);
        tu_r         <= ts_uncertain_i;   //! same PHC, same verdict
        mr_r         <= mr_i;             //! 10.4.3 level frozen for this PDU
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
            //! the PDU is on the wire: THIS is the level 10.4.3's eight-PDU
            //! hold may count, published with the same edge as tx_count_o so
            //! the integration's PDU strobe and the bit it announces agree
            tu_last_o <= tu_r;
            mr_last_o <= mr_r;
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
