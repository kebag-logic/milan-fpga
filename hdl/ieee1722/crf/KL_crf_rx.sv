/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_crf_rx.sv
  Description : Milan CRF Media Clock Input engine (measurement half).

                Consumes the avtp_stream_parser's per-frame pulse and
                validates Avnu Pro Audio CRF Media Clock Stream PDUs
                (Milan v1.2 7.3.2 / IEEE 1722-2016 Clause 10): subtype 4,
                type CRF_AUDIO_SAMPLE (1), pull 0, base_frequency 48000,
                timestamps_per_pdu 1 (crf_data_length 8),
                timestamp_interval 96 => 500 PDUs/s, one 64-bit gPTP-ns
                reference timestamp per PDU.

                Outputs (CSR-read, all captured per accepted PDU):
                  delta_o : crf_ts - ptp_now (signed 32) - the phase error
                            the media-clock servo daemon consumes (same
                            contract as the AAF ts_delta CSR 0x6EC).
                  rate_o  : accumulated (crf_ts[n] - crf_ts[n-256]) minus
                            nominal 256*2ms, signed ns per 512 ms window -
                            the frequency error input. Updates one clk after
                            the accepted PDU (the 256-entry ts history lives
                            in a single-port READ_FIRST BRAM ring; the read
                            lands the cycle after the accept - a fixed +1
                            clk skew, invisible to the ms-scale CSR poll).
                  locked_o: PDUs arriving AND |delta jitter| within window
                            for 8 consecutive PDUs; drops after 100 ms
                            without an accepted PDU (mirrors the AAF
                            media-lock contract) or on a validation error.
                  lock/unlock event counters: CLOCK_DOMAIN GET_COUNTERS
                            LOCKED/UNLOCKED when clock_source = CRF.

                COUNTER SEMANTICS split per Milan v1.2 Table 5.6, exactly
                (5.3.8.10 keeps the Stream Input counters "for each Stream
                Input" with no CRF exemption; KL_aecp_response_builder
                serves this engine's tallies behind the 0x0F3F mask for the
                CRF Media Clock Input, the KL_avtp_rx_monitor_ctx reading):

                * cnt_locked / cnt_unlocked are EVENT counters
                  ("incremented each time ...") - per event, as before.
                * pdu_count (FRAMES_RX), fmt_err (UNSUPPORTED_FORMAT) and
                  seq_err (SEQ_NUM_MISMATCH) are OBSERVATION-INTERVAL
                  counters: "incremented at the end of every observation
                  interval during which ..." where "the duration of the
                  observation interval is implementation-specific and shall
                  be less than or equal to 1 second". A PDU verdict only
                  SETS a seen flag; the tick derived from CLK_FREQ_HZ_P
                  (IVAL_CYC_P, default = the 1 s clause ceiling) commits +1
                  per flagged counter, so N events inside one interval move
                  a counter by AT MOST ONE. The per-frame reading is IEEE
                  1722.1-2021 Table 7-153's, not Milan's, and serving it
                  read ~500x high at the 500 PDU/s CRF cadence.

                The stream to follow is selected by sid_i/en_i (CSR pair
                today, the ACMP sink-1 SM once it exists - the remaining
                CRF work is the sink-1 bind chain, see
                docs/MILAN_COMPLIANCE_GAPS.md).

  Spec refs   : Milan v1.2 7.3.2-7.3.4; IEEE 1722-2016 Clause 10
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

module KL_crf_rx #(
  parameter int CLK_FREQ_HZ_P = 50_000_000,
  //! Milan v1.2 Table 5.6 observation interval in clk_i cycles,
  //! "implementation-specific and shall be less than or equal to 1 second" -
  //! the default DERIVES the 1 s ceiling from the clock parameter (never a
  //! mirrored cycle constant); TBs shrink it so a case sees interval
  //! boundaries
  parameter int unsigned IVAL_CYC_P = CLK_FREQ_HZ_P
)(
  input  wire         clk_i,
  input  wire         rst_n,

  //! per-frame capture from avtp_stream_parser (any AVTP stream frame)
  input  wire         frame_p_i,      //! parse pulse (all stream subtypes)
  input  wire [7:0]   subtype_i,
  input  wire [7:0]   seq_i,
  input  wire [63:0]  sid_frame_i,    //! frame's stream_id
  input  wire [31:0]  pullbase_i,     //! CRF: pull[31:29] | base_frequency
  input  wire [63:0]  fsh_i,          //! CRF: {dlen16, interval16, ts_hi32}
  input  wire [63:0]  fsh2_i,         //! CRF: {ts_lo32, -}
  input  wire [7:0]   type_i,         //! CRF type field (frame byte o+3)

  input  wire [63:0]  ptp_now_i,      //! gPTP-synced time (ns)

  //! CRF sink selection (CSR-provisioned; ACMP sink-1 SM later)
  input  wire         en_i,
  input  wire [63:0]  sid_i,

  //! measurement outputs (CSR)
  output logic signed [31:0] delta_o,     //! crf_ts - ptp_now @ last PDU
  output logic signed [31:0] rate_o,      //! ns error per 256-PDU window
  output logic [15:0] pdu_count_o,        //! FRAMES_RX: intervals with >= 1 accepted PDU (wraps)
  output logic [7:0]  fmt_err_o,          //! UNSUPPORTED_FORMAT: intervals with >= 1 profile reject
  output logic [7:0]  seq_err_o,          //! SEQ_NUM_MISMATCH: intervals with >= 1 discontinuity
  output logic        locked_o,
  output logic [31:0] cnt_locked_o,       //! lock events (CLOCK_DOMAIN ctr)
  output logic [31:0] cnt_unlocked_o      //! unlock events
);

  //! Milan 7.3.2 constants
  localparam [7:0]  CRF_SUBTYPE_C  = 8'h04;
  localparam [7:0]  CRF_TYPE_AS_C  = 8'h01;   // CRF_AUDIO_SAMPLE
  localparam [28:0] CRF_BASEHZ_C   = 29'd48000;
  localparam [15:0] CRF_DLEN_C     = 16'd8;   // 1 timestamp per PDU
  localparam [15:0] CRF_IVAL_C     = 16'd96;

  //! nominal spacing: interval/base = 96/48000 s = 2 ms
  localparam logic [31:0] NOM_PDU_NS_C  = 32'd2_000_000;
  localparam int unsigned RATE_LOG2_C   = 8;   // 256-PDU rate window
  localparam logic [63:0] NOM_WIN_NS_C  = 64'(NOM_PDU_NS_C) << RATE_LOG2_C;

  //! lock: 8 clean consecutive PDUs in, 100 ms silence out (AAF contract)
  localparam int unsigned SETTLE_C   = 8;
  localparam int unsigned TOUT_CYC_C = CLK_FREQ_HZ_P / 10;

  wire w_hit = frame_p_i && en_i && (subtype_i == CRF_SUBTYPE_C)
             && (sid_frame_i == sid_i);

  wire w_fmt_ok = (type_i == CRF_TYPE_AS_C)
               && (pullbase_i[31:29] == 3'd0)
               && (pullbase_i[28:0]  == CRF_BASEHZ_C)
               && (fsh_i[63:48] == CRF_DLEN_C)
               && (fsh_i[47:32] == CRF_IVAL_C);

  wire [63:0] w_crf_ts = {fsh_i[31:0], fsh2_i[63:32]};

  //! ring of accepted ts (the 512 ms frequency-error window) in ONE
  //! single-port READ_FIRST block RAM - never a multi-read-port LUTRAM
  //! replica structure (the 0x4B read-port-divergence rule). The only
  //! access the algorithm needs is read-old + write-new at hidx_r on an
  //! accepted PDU; same-port READ_FIRST returns the pre-write content, so
  //! both happen in one well-defined access. Entries keep ts[31:0] only:
  //! rate_o is a 32-bit truncation and subtraction is congruent mod 2^32,
  //! so the high half can never influence the result (bit-exact vs 64-bit
  //! storage for all inputs; the flop-file original was pruned the same
  //! way by synthesis).
  (* ram_style = "block" *)
  logic [31:0] ts_hist_r [0:(1<<RATE_LOG2_C)-1];
  logic [31:0] hist_old_r;   //! sync read data: ts[31:0] from 256 PDUs ago
  logic [31:0] ts_new_r;     //! accepted ts[31:0], aligned with hist_old_r
  logic        rate_pend_r;  //! rate math scheduled (ring full on accept)
  logic [RATE_LOG2_C-1:0] hidx_r;
  logic [8:0]  hfill_r;                           //! saturates at 256
  logic [7:0]  exp_seq_r;
  logic        have_seq_r;
  logic [2:0]  settle_r;
  logic [$clog2(TOUT_CYC_C+1)-1:0] tout_r;

  wire w_acc = w_hit && w_fmt_ok;

  //! this cycle's Table 5.6 interval-flag events. The engine keeps settle /
  //! lock / delta / rate per-PDU (measurement is not a counter); only the
  //! three interval counters' increments move to the tick commit. FRX = the
  //! accepted PDU itself (w_acc), UF = a matched-but-rejected PDU, SM = an
  //! accepted PDU with a non-sequential sequence_num.
  wire w_ev_uf_w = w_hit && !w_fmt_ok;
  wire w_ev_sm_w = w_acc && have_seq_r && (seq_i != exp_seq_r);

  // ==========================================================================
  //  Table 5.6 observation-interval tick (free-running; the clause fixes
  //  only an upper bound on the interval, not its phase)
  // ==========================================================================
  localparam int unsigned IVALW_C = (IVAL_CYC_P <= 2) ? 1
                                                      : $clog2(IVAL_CYC_P);
  logic [IVALW_C-1:0] iv_div_r;
  logic               iv_tick_r;
  logic               iv_frx_r, iv_uf_r, iv_sm_r;  //! interval seen flags

  always_ff @(posedge clk_i or negedge rst_n) begin : iv_tick_gen
    if (!rst_n) begin
      iv_div_r  <= '0;
      iv_tick_r <= 1'b0;
    end else if (32'(iv_div_r) >= IVAL_CYC_P - 1) begin
      iv_div_r  <= '0;
      iv_tick_r <= 1'b1;
    end else begin
      iv_div_r  <= iv_div_r + 1'b1;
      iv_tick_r <= 1'b0;
    end
  end : iv_tick_gen

  //! the BRAM port: no reset (BRAM), enabled once per accepted PDU
  always_ff @(posedge clk_i) begin : ts_hist_port
    if (w_acc) begin
      ts_hist_r[hidx_r] <= w_crf_ts[31:0];
      hist_old_r        <= ts_hist_r[hidx_r];
    end
  end : ts_hist_port

  always_ff @(posedge clk_i or negedge rst_n) begin : engine
    if (!rst_n) begin
      delta_o <= '0; rate_o <= '0;
      pdu_count_o <= '0; fmt_err_o <= '0; seq_err_o <= '0;
      locked_o <= 1'b0; cnt_locked_o <= '0; cnt_unlocked_o <= '0;
      hidx_r <= '0; hfill_r <= '0;
      exp_seq_r <= '0; have_seq_r <= 1'b0;
      settle_r <= '0; tout_r <= '0;
      ts_new_r <= '0; rate_pend_r <= 1'b0;
      iv_frx_r <= 1'b0; iv_uf_r <= 1'b0; iv_sm_r <= 1'b0;
    end else begin
      //! Table 5.6 interval commit: +1 per flagged counter at the tick,
      //! then the flags restart clean. An event landing in the tick cycle
      //! itself is harvested INTO the closing interval (the
      //! KL_avtp_rx_monitor_ctx boundary rule) - counted once, never lost,
      //! never doubled.
      if (iv_tick_r) begin
        if (iv_frx_r || w_acc)
          pdu_count_o <= pdu_count_o + 16'd1;
        if (iv_uf_r || w_ev_uf_w)
          fmt_err_o <= (&fmt_err_o) ? fmt_err_o : fmt_err_o + 8'd1;
        if (iv_sm_r || w_ev_sm_w)
          seq_err_o <= (&seq_err_o) ? seq_err_o : seq_err_o + 8'd1;
        iv_frx_r <= 1'b0;
        iv_uf_r  <= 1'b0;
        iv_sm_r  <= 1'b0;
      end else begin
        iv_frx_r <= iv_frx_r | w_acc;
        iv_uf_r  <= iv_uf_r  | w_ev_uf_w;
        iv_sm_r  <= iv_sm_r  | w_ev_sm_w;
      end

      //! retimed rate math: one clk after the accepted PDU, when the BRAM
      //! read (hist_old_r) is valid. ts_new_r - hist_old_r is congruent
      //! mod 2^32 with the 64-bit timestamp difference. Placed before the
      //! hit block so a same-cycle new accept re-arms rate_pend_r.
      if (rate_pend_r) begin
        rate_o      <= 32'(signed'(ts_new_r - hist_old_r
                                   - NOM_WIN_NS_C[31:0]));
        rate_pend_r <= 1'b0;
      end

      //! lock timeout: 100 ms without an accepted PDU
      if (w_acc) begin
        tout_r <= '0;
      end else if (tout_r == TOUT_CYC_C[$clog2(TOUT_CYC_C+1)-1:0]) begin
        if (locked_o) begin
          locked_o       <= 1'b0;
          cnt_unlocked_o <= cnt_unlocked_o + 32'd1;
        end
        settle_r <= '0;
        have_seq_r <= 1'b0;
        hfill_r  <= '0;
      end else begin
        tout_r <= tout_r + 1'b1;
      end

      if (w_hit) begin
        if (!w_fmt_ok) begin
          //! a malformed PDU breaks the settle run; the UNSUPPORTED_FORMAT
          //! count itself commits at the interval tick (w_ev_uf_w above)
          settle_r  <= '0;
        end else begin
          //! FRAMES_RX / SEQ_NUM_MISMATCH commit at the interval tick
          //! (w_acc / w_ev_sm_w above); a discontinuity still breaks the
          //! settle run per-PDU
          if (have_seq_r && (seq_i != exp_seq_r)) begin
            settle_r  <= '0;
          end else if (settle_r != 3'(SETTLE_C - 1)) begin
            settle_r <= settle_r + 3'd1;
          end else if (!locked_o) begin
            locked_o     <= 1'b1;
            cnt_locked_o <= cnt_locked_o + 32'd1;
          end
          exp_seq_r  <= seq_i + 8'd1;
          have_seq_r <= 1'b1;

          delta_o <= 32'(signed'(w_crf_ts - ptp_now_i));

          //! frequency error across the 256-PDU ring (512 ms): the BRAM
          //! port (ts_hist_port) reads old + writes new this cycle; the
          //! subtraction is retimed to next cycle via rate_pend_r
          ts_new_r    <= w_crf_ts[31:0];
          rate_pend_r <= (hfill_r == 9'(1 << RATE_LOG2_C));
          if (hfill_r != 9'(1 << RATE_LOG2_C)) begin
            hfill_r <= hfill_r + 9'd1;
          end
          hidx_r <= hidx_r + 1'b1;
        end
      end
    end
  end : engine

endmodule

`default_nettype wire
