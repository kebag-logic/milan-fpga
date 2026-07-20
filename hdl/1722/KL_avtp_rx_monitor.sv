/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_avtp_rx_monitor.sv
  Author      : Kebag Logic

  Date        : 2026-07-17
  Description : Milan v1.2 STREAM_INPUT diagnostic-counter engine (IEEE
                1722.1-2021 Table 7-156 / Milan §5.4.5.3 Table 5.16) for the
                bound listener sink. Consumes the per-frame pulse bundle from
                avtp_stream_parser (which already matched the bound stream_id)
                and maintains the counters GET_COUNTERS serves and the
                unsolicited push advertises.

                Contract byte-extracted from the pipewire module-avb reference
                (stream.c handle_aaf_packet + cmd-get-counters.c):
                  - UNSUPPORTED_FORMAT: per-PDU, when the AAF header fields
                    (subtype, format, nsr, bit_depth, channels_per_frame, sp)
                    differ from the Stream Input's CURRENT format (the
                    SET_STREAM_FORMAT-writable descriptor field). Such a PDU
                    counts NOTHING else (no FRAMES_RX, no lock effect).
                  - FRAMES_RX: every format-valid AVTPDU.
                  - MEDIA_LOCKED: ticks on the first valid PDU while unlocked;
                    (re)seed prev_seq and open an 8-PDU settle window
                    (AVB_STREAM_SEQ_SETTLE) that re-seeds instead of counting
                    the one-time bind/SRP-path-open sequence step.
                  - SEQ_NUM_MISMATCH: any discontinuity after settle
                    (loss, reorder or duplicate); STREAM_INTERRUPTED
                    additionally when lost = seq - expected >= 2
                    (AVB_STREAM_INTERRUPT_MIN_LOST).
                  - MEDIA_UNLOCKED: silence > 100 ms while locked
                    (MEDIA_UNLOCK_TIMEOUT_NS; the reference polls this at its
                    GET_COUNTERS cadence — fabric watches it every cycle).
                  - TIMESTAMP_UNCERTAIN: format-valid PDUs with tu=1 (the
                    reference exposes the counter as valid but never
                    increments it; the bit is on the wire, so fabric counts).
                  - Counters (and lock/settle state) reset on the
                    NOT-BOUND -> BOUND transition (Milan Table 5.6), never on
                    unbind; after unbind the parser match enable drops, so a
                    locked sink unlocks via the silence timeout, like the
                    reference.
                  - MEDIA_RESET / LATE_TIMESTAMP / EARLY_TIMESTAMP are
                    advertised valid but never tick — exactly the reference
                    (no media clock recovery in fabric yet; late/early need
                    the presentation-time compare that lands with the media
                    path).
                Deviation from the reference: the data_len-vs-frame-length
                malformed check is NOT performed (the MAC only delivers
                CRC-clean frames; a lying data_len is a payload-plane concern
                deferred to the AAF RX sink).

                dirty_p_o pulses on EVERY counter change (including the
                bind reset) — the AECP builder rate-limits pushes to 1/s per
                Milan §5.4.5, so this module does no throttling.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! Milan v1.2 STREAM_INPUT diagnostic-counter engine (IEEE 1722.1-2021
//! Table 7-156 / Milan §5.4.5.3) for the bound listener sink. Consumes the
//! per-frame pulse bundle from `avtp_stream_parser` and maintains the
//! counters served by AECP `GET_COUNTERS` and its unsolicited push:
//! MEDIA_LOCKED/UNLOCKED (first-valid-PDU lock / 100 ms silence unlock),
//! STREAM_INTERRUPTED (>= 2 PDUs lost), SEQ_NUM_MISMATCH (8-PDU settle
//! window after every (re)lock), TIMESTAMP_UNCERTAIN (tu bit),
//! UNSUPPORTED_FORMAT (per-PDU compare vs the current STREAM_INPUT format)
//! and FRAMES_RX. Counters reset on the not-bound -> bound edge (Milan
//! Table 5.6). `pdu_accept_p_o` pulses for every FRAMES_RX-counted PDU —
//! the AAF RX depacketizer's commit verdict.

`default_nettype none

module KL_avtp_rx_monitor #(
  parameter int unsigned CLK_FREQ_HZ_P = 50_000_000  //! for the 100 ms unlock timeout
)(
  input  wire         clk_i,             //! Global clock
  input  wire         rst_n,             //! Active-low synchronous reset

  //! --- per-frame pulse bundle from avtp_stream_parser (bound-sid matched) --
  input  wire         match_valid_i,     //! one-cycle pulse per matched frame
  input  wire [7:0]   subtype_i,         //! AVTP subtype of the matched PDU
  input  wire [7:0]   seq_num_i,         //! sequence_num of the matched PDU
  input  wire         ts_uncertain_i,    //! tu bit
  input  wire [31:0]  avtp_ts_i,         //! presentation time of the PDU
  input  wire [63:0]  fsh_i,             //! bytes O+16..O+23 of the PDU

  //! --- binding / expected format (AECP + ACMP listener SM) ---------------
  input  wire         bound_i,           //! listener sink 0 is bound
  input  wire [63:0]  fmt_i,             //! current STREAM_INPUT[0] format u64
  input  wire [31:0]  ptp_now_i,         //! PHC nanoseconds [31:0] (gPTP)
  input  wire [31:0]  pres_ofs_i,        //! presentation offset ns (MTT/acc-lat)
  input  wire         media_reset_p_i,   //! playback servo rail event (pulse)
  input  wire [15:0]  clk_src_i,         //! live clock_source_index (0=internal)
  input  wire         servo_conv_i,      //! playback clock converged (external
                                         //! media-lock condition - USER rule)

  //! --- Milan STREAM_INPUT counters (Table 7-156 names) --------------------
  output logic [31:0] cnt_media_locked_o,       //! MEDIA_LOCKED (bit 0)
  output logic [31:0] cnt_media_unlocked_o,     //! MEDIA_UNLOCKED (bit 1)
  output logic [31:0] cnt_stream_interrupted_o, //! STREAM_INTERRUPTED (bit 2)
  output logic [31:0] cnt_seq_mismatch_o,       //! SEQ_NUM_MISMATCH (bit 3)
  output logic [31:0] cnt_ts_uncertain_o,       //! TIMESTAMP_UNCERTAIN (bit 5)
  output logic [31:0] cnt_unsupported_fmt_o,    //! UNSUPPORTED_FORMAT (bit 8)
  output logic [31:0] cnt_frames_rx_o,          //! FRAMES_RX (bit 11)
  output logic [31:0] cnt_media_reset_o,        //! MEDIA_RESET (bit 4)
  output logic [31:0] cnt_late_ts_o,            //! LATE_TIMESTAMP (bit 9)
  output logic [31:0] cnt_early_ts_o,           //! EARLY_TIMESTAMP (bit 10)

  output logic        media_locked_o,    //! current lock state (level)
  output logic        dirty_p_o,         //! one-cycle pulse on any change
  output logic        pdu_accept_p_o,    //! one-cycle pulse: PDU counted in
                                         //! FRAMES_RX (bound + format-valid) —
                                         //! the depacketizer's commit verdict
  output logic [31:0] last_ts_o,         //! avtp_timestamp of the last
                                         //! accepted PDU (media-clock hook)
  output logic [31:0] last_tsd_o         //! signed ts_delta (avtp_ts - now)
                                         //! HW-latched at each accepted PDU:
                                         //! zero-noise error signal for
                                         //! userspace PHC discipline (07-18)
);

  //! Milan §5.4.5.3 / reference MEDIA_UNLOCK_TIMEOUT_NS = 100 ms
  localparam int unsigned UNLOCK_CYCLES_C = CLK_FREQ_HZ_P / 10;
  //! reference AVB_STREAM_SEQ_SETTLE
  localparam int unsigned SETTLE_C = 8;
  //! reference AVB_STREAM_INTERRUPT_MIN_LOST
  localparam int unsigned INTERRUPT_MIN_LOST_C = 2;
  //! EARLY bound margin beyond the presentation offset (fabric-defined:
  //! the reference never ticks LATE/EARLY; 1722.1 only names the meaning)
  localparam logic [31:0] EARLY_MARGIN_NS_C = 32'd10_000_000;

  // ---- expected AAF fields from the format u64 (H.1 quadlet layout;
  //      pipewire avb_aem_stream_format_decode) ------------------------------
  wire [7:0] f_subtype = fmt_i[63:56];
  wire [3:0] f_nsr     = fmt_i[51:48];
  wire [7:0] f_format  = fmt_i[47:40];
  wire [7:0] f_depth   = fmt_i[39:32];
  wire [9:0] f_chans   = fmt_i[31:22];

  // ---- received AAF fields from the format-specific header (wire layout;
  //      pipewire struct avb_packet_aaf) --------------------------------------
  wire [7:0] p_format  = fsh_i[63:56];   // O+16
  wire [3:0] p_nsr     = fsh_i[55:52];   // O+17 [7:4]
  wire [7:0] p_chans   = fsh_i[47:40];   // O+18
  wire [7:0] p_depth   = fsh_i[39:32];   // O+19
  wire       p_sp      = fsh_i[12];      // O+22 [4]

  //! reference aaf_pdu_format_matches: subtype, format, nsr and bit_depth
  //! strict; CHANNELS ADAPTIVE (bench rule 2026-07-20, CERT es-4.4): the
  //! listener accepts any wire channel count 1..fmt_channels - the AEM
  //! default can stay the full 8ch format while a 2ch talker connects
  //! pure-ACMP (no SET_STREAM_FORMAT needed; the depacketizer extracts by
  //! the PDU's own data_len so the media path is wire-driven anyway).
  //! sparse always NORMAL=0.
  wire fmt_ok = (subtype_i == f_subtype) &&
                (p_format  == f_format)  &&
                (p_nsr     == f_nsr)     &&
                (p_depth   == f_depth)   &&
                (p_chans   != 8'd0)      &&
                ({2'b00, p_chans} <= f_chans) &&
                (p_sp      == 1'b0);

  // ---- state ---------------------------------------------------------------
  logic        bound_q;
  logic [7:0]  prev_seq_r;
  logic [3:0]  settle_r;
  logic [31:0] silence_r;

  wire bound_rise = bound_i && !bound_q;
  //! presentation-time check (mod-2^32 signed delta, valid PDUs only):
  //! LATE  = presentation already in the past at arrival;
  //! EARLY = further ahead than the presentation offset + margin
  wire signed [31:0] ts_delta_w = avtp_ts_i - ptp_now_i;
  wire late_w  = ts_delta_w < 0;
  wire early_w = !late_w &&
                 (unsigned'(ts_delta_w) > (pres_ofs_i + EARLY_MARGIN_NS_C));
  wire [7:0] expected_w = prev_seq_r + 8'd1;
  wire [7:0] lost_w     = seq_num_i - expected_w;   // mod-256, as the reference
  wire       silence_hit = media_locked_o && (silence_r >= UNLOCK_CYCLES_C);

  always_ff @(posedge clk_i) begin : monitor_logic
    if (!rst_n) begin
      bound_q                  <= 1'b0;
      prev_seq_r               <= '0;
      settle_r                 <= '0;
      silence_r                <= '0;
      cnt_media_locked_o       <= '0;
      cnt_media_unlocked_o     <= '0;
      cnt_stream_interrupted_o <= '0;
      cnt_seq_mismatch_o       <= '0;
      cnt_ts_uncertain_o       <= '0;
      cnt_unsupported_fmt_o    <= '0;
      cnt_frames_rx_o          <= '0;
      cnt_media_reset_o        <= '0;
      cnt_late_ts_o            <= '0;
      cnt_early_ts_o           <= '0;
      media_locked_o           <= 1'b0;
      dirty_p_o                <= 1'b0;
      pdu_accept_p_o           <= 1'b0;
      last_ts_o                <= '0;
      last_tsd_o               <= '0;
    end
    else begin
      bound_q        <= bound_i;
      dirty_p_o      <= 1'b0;
      pdu_accept_p_o <= 1'b0;

      //! silence watchdog (saturating; reset by every valid frame below)
      if (media_locked_o && !(&silence_r))
        silence_r <= silence_r + 32'd1;
      if (silence_hit) begin
        cnt_media_unlocked_o <= cnt_media_unlocked_o + 32'd1;
        media_locked_o       <= 1'b0;
        silence_r            <= '0;
        dirty_p_o            <= 1'b1;
      end

      if (match_valid_i && bound_i) begin
        if (!fmt_ok) begin
          //! counts nothing else (reference early-returns)
          cnt_unsupported_fmt_o <= cnt_unsupported_fmt_o + 32'd1;
          dirty_p_o             <= 1'b1;
        end
        else begin
          cnt_frames_rx_o <= cnt_frames_rx_o + 32'd1;
          silence_r       <= '0;
          dirty_p_o       <= 1'b1;
          pdu_accept_p_o  <= 1'b1;
          last_ts_o       <= avtp_ts_i;
          last_tsd_o      <= unsigned'(ts_delta_w);
          if (late_w)  cnt_late_ts_o  <= cnt_late_ts_o  + 32'd1;
          if (early_w) cnt_early_ts_o <= cnt_early_ts_o + 32'd1;
          if (ts_uncertain_i)
            cnt_ts_uncertain_o <= cnt_ts_uncertain_o + 32'd1;

          if (!media_locked_o) begin
            //! USER rule: internal clock source locks on buffer position
            //! (first valid PDU); an EXTERNAL source locks only once the
            //! recovered clock has converged near nominal
            if (clk_src_i == 16'd0 || servo_conv_i) begin
              cnt_media_locked_o <= cnt_media_locked_o + 32'd1;
              media_locked_o     <= 1'b1;
            end
            prev_seq_r         <= seq_num_i;     // (re)lock: seed, no gap
            settle_r           <= 4'(SETTLE_C);  // grace the bind/path-open step
          end
          else if (settle_r != '0) begin
            settle_r   <= settle_r - 4'd1;       // settling: re-seed, no count
            prev_seq_r <= seq_num_i;
          end
          else begin
            if (seq_num_i != expected_w) begin
              cnt_seq_mismatch_o <= cnt_seq_mismatch_o + 32'd1;
              if (lost_w >= 8'(INTERRUPT_MIN_LOST_C))
                cnt_stream_interrupted_o <= cnt_stream_interrupted_o + 32'd1;
            end
            prev_seq_r <= seq_num_i;
          end
        end
      end

      //! external source: convergence lost while locked = unlock event
      if (media_locked_o && clk_src_i != 16'd0 && !servo_conv_i) begin
        cnt_media_unlocked_o <= cnt_media_unlocked_o + 32'd1;
        media_locked_o       <= 1'b0;
        dirty_p_o            <= 1'b1;
      end

      //! playback servo rail = a media-clock reset event
      if (media_reset_p_i && bound_i) begin
        cnt_media_reset_o <= cnt_media_reset_o + 32'd1;
        dirty_p_o         <= 1'b1;
      end

      //! Milan Table 5.6: reset on not-bound -> bound (wins over everything)
      if (bound_rise) begin
        cnt_media_locked_o       <= '0;
        cnt_media_unlocked_o     <= '0;
        cnt_stream_interrupted_o <= '0;
        cnt_seq_mismatch_o       <= '0;
        cnt_ts_uncertain_o       <= '0;
        cnt_unsupported_fmt_o    <= '0;
        cnt_frames_rx_o          <= '0;
        cnt_media_reset_o        <= '0;
        cnt_late_ts_o            <= '0;
        cnt_early_ts_o           <= '0;
        media_locked_o           <= 1'b0;
        settle_r                 <= '0;
        silence_r                <= '0;
        dirty_p_o                <= 1'b1;
      end
    end
  end : monitor_logic

endmodule

`default_nettype wire
