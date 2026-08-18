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
                Input" with no CRF exemption, and 5.4.2.25 Table 5.16
                makes ALL TEN mandatory "for each Stream Input" - so the
                0x0F3F mask KL_aecp_response_builder serves for the CRF
                Media Clock Input stays whole and every bit in it has to
                be a MEASUREMENT, never a constant):

                * cnt_locked / cnt_unlocked / cnt_intr (STREAM_INTERRUPTED)
                  are EVENT counters ("incremented each time ...") - per
                  event.
                * pdu_count (FRAMES_RX), fmt_err (UNSUPPORTED_FORMAT),
                  seq_err (SEQ_NUM_MISMATCH), mr_cnt (MEDIA_RESET), tu_cnt
                  (TIMESTAMP_UNCERTAIN), late_cnt (LATE_TIMESTAMP) and
                  early_cnt (EARLY_TIMESTAMP) are OBSERVATION-INTERVAL
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

                THE CRF READING of the five counters that used to be
                advertised-but-constant (traceability AVTP-5t):

                * STREAM_INTERRUPTED "each time the stream playback is
                  interrupted for any reason other than a Controller Unbind
                  operation ... this can include the loss of several
                  AVTPDUs". The CRF sink's "playback" is media-clock
                  recovery and the clause's own example is the trigger: an
                  accepted PDU whose sequence_num shows >= 2 lost PDUs
                  (INTR_MIN_LOST_C, the KL_avtp_rx_monitor law verbatim).
                  A Controller Unbind drops en_i, so no PDU is accepted and
                  the counter cannot move - the clause's exclusion holds
                  structurally.
                * MEDIA_RESET "the 'mr' bit was toggled in any of the
                  received Stream Data AVTPDUs" - the RECEIVED bit of the
                  CRF PDU (mr_i, frame byte O+1 bit 3; IEEE 1722-2016
                  10.4.3 gives CRF the same mr as 4.4.4.3 and holds it >= 8
                  PDUs), so only the EDGE counts. The era's first accepted
                  PDU SEEDS the reference without counting; a bind edge or
                  a 100 ms silence re-seeds, so a new talker's mr level is
                  never scored as this stream's toggle (the 4d31ecfb rule).
                  THE SAME EDGE LEAVES THIS MODULE as mr_toggle_p_o: 10.4.3
                  gives the received bit a SECOND duty beyond the counter -
                  "toggle the mr bit in any outgoing media streams that are
                  deriving timestamps from the CRF stream" - and a counter
                  cannot serve it (the interval fold collapses N toggles to
                  one increment and delays it up to a second). See that
                  port's own note (gh #62 H2a).
                * TIMESTAMP_UNCERTAIN "the 'tu' bit was set in any of the
                  received Stream Data AVTPDUs" - tu_i. NOTE the CRF
                  ALTERNATIVE header (1722-2016 10.4.5) carries tu at byte
                  O+1 bit 0, where the common stream header carries tv;
                  byte O+3 is the CRF `type` field, so the common-header tu
                  extraction reads a CRF PDU's type LSB and would report
                  tu=1 on every conformant CRF_AUDIO_SAMPLE PDU.
                * LATE_TIMESTAMP / EARLY_TIMESTAMP "an AVTP timestamp field
                  that was in the past" / "too far in the future to
                  process", applied to the CRF reference timestamp - the
                  only timestamp a CRF PDU carries, and the one 1722-2016
                  10.6 says the Listener "can simply compare to the local
                  gPTP clock". 10.7 sets T_CRF = source + Max Transit Time,
                  so the delta is nominally POSITIVE and bounded by TTmax;
                  10.6 says an UNRESERVED CRF stream can deliver a
                  timestamp already in the past, and Milan 7.3.3 mandates a
                  Class A reservation - so a past timestamp is exactly the
                  fault LATE_TIMESTAMP names, and further ahead than
                  MAXTT_NS_P + EARLY_MARGIN_NS_P is "too far in the future"
                  (the KL_avtp_rx_monitor pres_ofs + margin shape,
                  EARLY_MARGIN_NS_P).

                No Table 5.16 bit is dropped: the clause exempts nothing,
                and every one of the ten now moves off a measured event.

                THE ERA RULE (5.3.8.10, the sentence that closes Table 5.6):
                "The PAAD-AE shall reset all of these counters to zero each
                time the Stream Input changes its state from not bound to
                bound", and expressly NOT the other way - "the PAAD-AE does
                not reset these counters when the Stream Input changes its
                state from bound to not bound". en_i IS that bound state
                (milan_datapath: ACMP sink-1 bind | bench CSR lever), so its
                RISING edge wipes all ten tallies, the interval seen flags
                and locked_o. locked_o falls WITHOUT scoring an unlock:
                MEDIA_LOCKED = MEDIA_UNLOCKED = 0 is Table 5.6's own reading
                of "not synchronized", and a +1 into a zeroed MEDIA_UNLOCKED
                would strand the sink at UNLOCKED = LOCKED + 1, which is
                neither of the two states the clause allows.

                The stream to follow is selected by sid_i/en_i (CSR pair
                today, the ACMP sink-1 SM once it exists - the remaining
                CRF integration gaps are recorded in
                docs/testing/MILAN_V12_AUDIT_2026-08-16.md B3 and B4).

  Spec refs   : Milan v1.2 7.3.2-7.3.4, 5.3.8.10 Table 5.6, 5.4.2.25
                Table 5.16; IEEE 1722-2016 Clause 10 (10.4.3 mr, 10.4.5 tu,
                10.6/10.7 CRF timestamp placement)
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
  parameter int unsigned IVAL_CYC_P = CLK_FREQ_HZ_P,
  //! Max Transit Time the CRF talker added to its source timestamp (IEEE
  //! 1722-2016 10.7, Equation 14). Milan 7.3.3 mandates a Class A
  //! reservation for the media clock stream, whose worst case is 2 ms over
  //! 7 hops - the bound above which a CRF reference timestamp is "too far
  //! in the future to process" (Table 5.6 EARLY_TIMESTAMP)
  parameter int unsigned MAXTT_NS_P = 2_000_000,
  //! slack above that Max Transit Time before a CRF reference timestamp is
  //! called EARLY - the same margin, in the same role, that the AAF
  //! instrument (KL_avtp_rx_monitor) allows above its presentation offset
  parameter int unsigned EARLY_MARGIN_NS_P = 10_000_000
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
  //! mr (media clock restart), IEEE 1722-2016 10.4.3: a LEVEL the CRF
  //! talker TOGGLES on a media-clock source change and holds >= 8 PDUs.
  //! Table 5.6 MEDIA_RESET counts the TOGGLE, so this engine keeps the
  //! previous value; this port is the raw bit (frame byte o+1 bit 3)
  input  wire         mr_i,
  //! tu (timing uncertain), IEEE 1722-2016 10.4.5 - the CRF ALTERNATIVE
  //! header carries it at frame byte o+1 bit 0 (where the common stream
  //! header carries tv); byte o+3 is `type` here, so the common-header tu
  //! net is NOT this bit
  input  wire         tu_i,

  input  wire [63:0]  ptp_now_i,      //! gPTP-synced time (ns)

  //! CRF sink selection (CSR-provisioned; ACMP sink-1 SM later)
  input  wire         en_i,
  input  wire [63:0]  sid_i,

  //! Milan v1.2 5.3.8.7 stopped state for this Stream Input (bound and not
  //! started). OBSERVATION IS NOT GATED by it: a stopped sink still matches,
  //! validates and counts every Table 5.6 event, because 5.3.8.10 defines
  //! the counters on AVTPDUs "received on this Stream Input" and the
  //! clause's verb is discard, not ignore. What stops is CONSUMPTION: the
  //! settle/lock machinery treats the stream as silent (locked_o falls
  //! through the ordinary 100 ms timeout and stays down) and the 10.4.3
  //! restart echo (mr_toggle_p_o) never pulses, so stopped timing data can
  //! neither reach clock recovery nor restart an outgoing stream.
  input  wire         stop_i,

  //! measurement outputs (CSR)
  output logic signed [31:0] delta_o,     //! crf_ts - ptp_now @ last PDU
  output logic signed [31:0] rate_o,      //! ns error per 256-PDU window
  //! the seven Table 5.6 tallies below are 32-bit WRAPPING counters
  //! (gh #61 G1). The old backing had TWO deviations from Milan 5.3.8.10's
  //! "wraps back to zero": fmt_err/seq_err SATURATED at 255 (a saturating
  //! counter is a frozen instrument after ~4 min 15 s of persistent fault -
  //! the same defect class as the advertised-valid-never-moves purge) and
  //! the 16-bit five wrapped at the 65536 s = 18 h 12 min soak mark. The
  //! CSR ABI is untouched: CRF_STATUS 0x74C serves documented TRUNCATED
  //! slices ({pdu[15:0], fmt[7:0], seq[7:0]}), the AECP wire serves the
  //! full width.
  output logic [31:0] pdu_count_o,        //! FRAMES_RX: intervals with >= 1 accepted PDU
  output logic [31:0] fmt_err_o,          //! UNSUPPORTED_FORMAT: intervals with >= 1 profile reject
  output logic [31:0] seq_err_o,          //! SEQ_NUM_MISMATCH: intervals with >= 1 discontinuity
  //! MEDIA_RESET / TIMESTAMP_UNCERTAIN / LATE_TIMESTAMP / EARLY_TIMESTAMP:
  //! intervals with >= 1 such PDU
  output logic [31:0] mr_cnt_o,
  output logic [31:0] tu_cnt_o,
  output logic [31:0] late_cnt_o,
  output logic [31:0] early_cnt_o,
  output logic        locked_o,
  output logic [31:0] cnt_locked_o,       //! lock events (CLOCK_DOMAIN ctr)
  output logic [31:0] cnt_unlocked_o,     //! unlock events
  output logic [31:0] cnt_intr_o,         //! STREAM_INTERRUPTED events
  //! one-cycle "a counter a controller should hear about moved" pulse -
  //! the Table 5.22 push source for the CRF Media Clock Input's
  //! GET_COUNTERS row (gh #60 F2). Fires on: a lock/unlock event, a
  //! STREAM_INTERRUPTED event, any of the SIX anomaly interval commits
  //! (UF/SM/MR/TU/LT/ET), and the bind-rise wipe (the zeroed tallies are
  //! themselves a wire-visible change). NEVER on a healthy FRAMES_RX
  //! interval - the task-21 exclusion, verbatim: a healthy stream closes
  //! an interval every second forever and must not push forever.
  output logic        dirty_p_o,
  //! one-cycle pulse: the RECEIVED mr level TOGGLED on an accepted PDU of
  //! the followed stream (the same w_ev_mr_w event MEDIA_RESET counts,
  //! registered). This is the 4.4.4.3 trigger the counter alone cannot
  //! serve - "any streams deriving timestamps from the CRF stream shall
  //! toggle the mr bit ... if the mr bit in the CRF stream has been
  //! toggled" - exported for KL_media_clock_restart's restart_p_i.
  //! milan_datapath gates it with clock_source == CRF, which is 10.4.3's
  //! own scoping: "only the mr bit from the stream being used by the
  //! Listener for recovering the media clock is valid". The seeding rules
  //! keep it honest structurally: the era's first accepted PDU SEEDS the
  //! reference silently (bind rise and the 100 ms silence re-seed), and a
  //! REJECTED PDU is never accepted - so a new talker's level, a resuming
  //! stream, or a malformed flip can never fire a phantom restart (gh #62
  //! H2a)
  output logic        mr_toggle_p_o
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

  //! Table 5.6 STREAM_INTERRUPTED "the loss of several AVTPDUs" - the same
  //! threshold KL_avtp_rx_monitor applies to the AAF sinks
  localparam int unsigned INTR_MIN_LOST_C = 2;
  //! "too far in the future to process": past the transit time the talker
  //! added (10.7) plus the instrument's slack. DERIVED from the two named
  //! quantities - never a folded constant
  localparam logic [31:0] EARLY_LIMIT_C = 32'(MAXTT_NS_P)
                                        + 32'(EARLY_MARGIN_NS_P);

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
  //! mr reference for the CURRENT binding era (Table 5.6 MEDIA_RESET counts
  //! toggles): SEEDED, not counted, by the era's first accepted PDU
  logic        prev_mr_r;
  logic        mr_seeded_r;
  logic        en_q;                              //! bind-edge detect

  wire w_acc = w_hit && w_fmt_ok;
  //! the CONSUMED accept: only a started sink's accepts feed the lock
  //! machinery; every counter and measurement above stays on w_acc
  wire w_acc_run_w = w_acc && !stop_i;

  //! the CRF phase error, computed ONCE: delta_o publishes it and the
  //! Table 5.6 late/early verdicts read the same expression
  wire signed [31:0] w_tsd = 32'(signed'(w_crf_ts - ptp_now_i));
  //! LATE  = the reference instant already passed at arrival (1722-2016
  //!         10.6: only an UNRESERVED CRF stream should ever do this, and
  //!         Milan 7.3.3 reserves it Class A);
  //! EARLY = further ahead than the Max Transit Time the talker added
  //!         (10.7) plus the margin
  wire w_late_w  = w_tsd < 0;
  wire w_early_w = !w_late_w && (unsigned'(w_tsd) > EARLY_LIMIT_C);
  //! PDUs lost before this one (mod-256, the KL_avtp_rx_monitor form)
  wire [7:0] w_lost_w = seq_i - exp_seq_r;

  //! this cycle's Table 5.6 interval-flag events. The engine keeps settle /
  //! lock / delta / rate per-PDU (measurement is not a counter); only the
  //! three interval counters' increments move to the tick commit. FRX = the
  //! accepted PDU itself (w_acc), UF = a matched-but-rejected PDU, SM = an
  //! accepted PDU with a non-sequential sequence_num.
  wire w_ev_uf_w = w_hit && !w_fmt_ok;
  wire w_ev_sm_w = w_acc && have_seq_r && (seq_i != exp_seq_r);
  //! MR = the received mr bit TOGGLING vs this era's seeded reference;
  //! TU/LT/ET = the accepted PDU's own tu bit / late / early verdict. All
  //! four are gated by w_acc: a REJECTED PDU counts UNSUPPORTED_FORMAT and
  //! nothing else (the reference early-returns)
  wire w_ev_mr_w = w_acc && mr_seeded_r && (mr_i != prev_mr_r);
  wire w_ev_tu_w = w_acc && tu_i;
  wire w_ev_lt_w = w_acc && w_late_w;
  wire w_ev_et_w = w_acc && w_early_w;
  //! STREAM_INTERRUPTED is PER-EVENT (no interval flag): an accepted PDU
  //! whose sequence_num shows >= INTR_MIN_LOST_C lost AVTPDUs
  wire w_ev_si_w = w_ev_sm_w && (w_lost_w >= 8'(INTR_MIN_LOST_C));
  //! not-bound -> bound: the mr level belongs to the PREVIOUS era
  wire w_bind_rise_w = en_i && !en_q;

  // ==========================================================================
  //  Table 5.6 observation-interval tick (free-running; the clause fixes
  //  only an upper bound on the interval, not its phase)
  // ==========================================================================
  localparam int unsigned IVALW_C = (IVAL_CYC_P <= 2) ? 1
                                                      : $clog2(IVAL_CYC_P);
  logic [IVALW_C-1:0] iv_div_r;
  logic               iv_tick_r;
  //! interval seen flags, one per Table 5.6 observation-interval counter
  logic               iv_frx_r, iv_uf_r, iv_sm_r;
  logic               iv_mr_r, iv_tu_r, iv_lt_r, iv_et_r;

  always_ff @(posedge clk_i) begin : iv_tick_gen
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

  always_ff @(posedge clk_i) begin : engine
    if (!rst_n) begin
      delta_o <= '0; rate_o <= '0;
      pdu_count_o <= '0; fmt_err_o <= '0; seq_err_o <= '0;
      mr_cnt_o <= '0; tu_cnt_o <= '0; late_cnt_o <= '0; early_cnt_o <= '0;
      locked_o <= 1'b0; cnt_locked_o <= '0; cnt_unlocked_o <= '0;
      cnt_intr_o <= '0;
      dirty_p_o <= 1'b0;
      mr_toggle_p_o <= 1'b0;
      hidx_r <= '0; hfill_r <= '0;
      exp_seq_r <= '0; have_seq_r <= 1'b0;
      settle_r <= '0; tout_r <= '0;
      ts_new_r <= '0; rate_pend_r <= 1'b0;
      prev_mr_r <= 1'b0; mr_seeded_r <= 1'b0; en_q <= 1'b0;
      iv_frx_r <= 1'b0; iv_uf_r <= 1'b0; iv_sm_r <= 1'b0;
      iv_mr_r <= 1'b0; iv_tu_r <= 1'b0; iv_lt_r <= 1'b0; iv_et_r <= 1'b0;
    end else begin
      en_q <= en_i;
      dirty_p_o <= 1'b0;
      //! the 10.4.3 restart EDGE, registered, one cycle wide. Exactly the
      //! event MEDIA_RESET folds into its interval - same term, no second
      //! detector to drift from the first. The bind rise is excluded for the
      //! reason the wipe below states: the previous era's mr level may not be
      //! scored against the new binding, and that includes not restarting an
      //! outgoing stream over it.
      //! ...and a STOPPED sink's toggle is counted but never echoed: the
      //! restart of an outgoing stream is a media effect, and 5.3.8.7's
      //! discard rule ends this frame's influence at the counters.
      mr_toggle_p_o <= w_ev_mr_w & ~w_bind_rise_w & ~stop_i;
      //! Table 5.6 interval commit: +1 per flagged counter at the tick,
      //! then the flags restart clean. An event landing in the tick cycle
      //! itself is harvested INTO the closing interval (the
      //! KL_avtp_rx_monitor_ctx boundary rule) - counted once, never lost,
      //! never doubled. All seven wrap at 32 bits (gh #61 G1: saturation
      //! itself violates 5.3.8.10's "wraps back to zero" - the old
      //! fmt_err/seq_err peg at 255 froze the instrument after 4 min 15 s
      //! of persistent fault).
      if (iv_tick_r) begin
        if (iv_frx_r || w_acc)
          pdu_count_o <= pdu_count_o + 32'd1;
        if (iv_uf_r || w_ev_uf_w)
          fmt_err_o <= fmt_err_o + 32'd1;
        if (iv_sm_r || w_ev_sm_w)
          seq_err_o <= seq_err_o + 32'd1;
        if (iv_mr_r || w_ev_mr_w) mr_cnt_o    <= mr_cnt_o    + 32'd1;
        if (iv_tu_r || w_ev_tu_w) tu_cnt_o    <= tu_cnt_o    + 32'd1;
        if (iv_lt_r || w_ev_lt_w) late_cnt_o  <= late_cnt_o  + 32'd1;
        if (iv_et_r || w_ev_et_w) early_cnt_o <= early_cnt_o + 32'd1;
        //! the SIX anomaly commits arm the Table 5.22 push; a healthy
        //! FRAMES_RX interval (iv_frx alone) never does (task-21 rule)
        if ((iv_uf_r || w_ev_uf_w) || (iv_sm_r || w_ev_sm_w) ||
            (iv_mr_r || w_ev_mr_w) || (iv_tu_r || w_ev_tu_w) ||
            (iv_lt_r || w_ev_lt_w) || (iv_et_r || w_ev_et_w))
          dirty_p_o <= 1'b1;
        iv_frx_r <= 1'b0;
        iv_uf_r  <= 1'b0;
        iv_sm_r  <= 1'b0;
        iv_mr_r  <= 1'b0;
        iv_tu_r  <= 1'b0;
        iv_lt_r  <= 1'b0;
        iv_et_r  <= 1'b0;
      end else begin
        iv_frx_r <= iv_frx_r | w_acc;
        iv_uf_r  <= iv_uf_r  | w_ev_uf_w;
        iv_sm_r  <= iv_sm_r  | w_ev_sm_w;
        iv_mr_r  <= iv_mr_r  | w_ev_mr_w;
        iv_tu_r  <= iv_tu_r  | w_ev_tu_w;
        iv_lt_r  <= iv_lt_r  | w_ev_lt_w;
        iv_et_r  <= iv_et_r  | w_ev_et_w;
      end

      //! STREAM_INTERRUPTED: PER-EVENT, so it lands the cycle of the PDU
      //! (never folded into an interval) - "incremented each time"
      if (w_ev_si_w) begin
        cnt_intr_o <= cnt_intr_o + 32'd1;
        dirty_p_o  <= 1'b1;
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

      //! lock timeout: 100 ms without a CONSUMED accepted PDU - a stopped
      //! sink is silent to the lock machinery however much it observes
      if (w_acc_run_w) begin
        tout_r <= '0;
      end else if (tout_r == TOUT_CYC_C[$clog2(TOUT_CYC_C+1)-1:0]) begin
        if (locked_o) begin
          locked_o       <= 1'b0;
          cnt_unlocked_o <= cnt_unlocked_o + 32'd1;
          dirty_p_o      <= 1'b1;
        end
        settle_r <= '0;
        //! the silence reset SPLITS on the stopped state. Stopped, the
        //! frames may still be arriving and being counted, so the sequence
        //! cursor, the ring fill and the mr reference stay live - resetting
        //! them would fake a SEQ_NUM_MISMATCH and a MEDIA_RESET on restart.
        //! Started, this is true silence and the full reset applies: the mr
        //! LEVEL belongs to the stream that went silent, so a resuming (or
        //! brand new) talker's first PDU is never scored as THIS stream's
        //! toggle.
        if (!stop_i) begin
          have_seq_r <= 1'b0;
          hfill_r  <= '0;
          mr_seeded_r <= 1'b0;
        end
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
          end else if (stop_i) begin
            //! a stopped sink's accepts advance nothing toward lock; the
            //! settle run resumes from wherever the timeout left it once
            //! the sink is started again
          end else if (settle_r != 3'(SETTLE_C - 1)) begin
            settle_r <= settle_r + 3'd1;
          end else if (!locked_o) begin
            locked_o     <= 1'b1;
            cnt_locked_o <= cnt_locked_o + 32'd1;
            dirty_p_o    <= 1'b1;
          end
          exp_seq_r  <= seq_i + 8'd1;
          have_seq_r <= 1'b1;
          //! Table 5.6 MEDIA_RESET: the toggle counted above (w_ev_mr_w);
          //! here the level becomes this era's reference, seeded once
          prev_mr_r   <= mr_i;
          mr_seeded_r <= 1'b1;

          delta_o <= w_tsd;

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

      //! not-bound -> bound (Milan 5.3.8.10's era edge): nothing the
      //! PREVIOUS binding left behind may be scored against the new one -
      //! not its mr level (a phantom MEDIA_RESET) and not its sequence
      //! cursor (a phantom SEQ_NUM_MISMATCH, and with it the very
      //! STREAM_INTERRUPTED that Table 5.6 excludes for "a Controller
      //! Unbind operation"). WINS over the accept branch above: a bind and
      //! a PDU cannot land in the same cycle in practice, but the ordering
      //! is stated, not left to luck
      if (w_bind_rise_w) begin
        mr_seeded_r <= 1'b0;
        have_seq_r  <= 1'b0;
        settle_r    <= '0;
        //! ... and the TALLIES themselves. Milan v1.2 5.3.8.10, the sentence
        //! that closes Table 5.6: "The PAAD-AE shall reset all of these
        //! counters to zero each time the Stream Input changes its state
        //! from not bound to bound." The CRF Media Clock Input is a Stream
        //! Input (5.4.2.25 Table 5.16 claims all ten for it), and en_i IS
        //! that bound state - milan_datapath drives it from the ACMP sink-1
        //! bind ORed with the bench CSR lever. Carrying a previous era's
        //! totals into a new binding is the same defect class the five
        //! constant zeros were: a number a controller cannot interpret.
        //! Note the clause's asymmetry - the wipe is on the RISING edge
        //! only ("the PAAD-AE does not reset these counters when the Stream
        //! Input changes its state from bound to not bound"), which is why
        //! this keys on w_bind_rise_w and not on !en_i.
        pdu_count_o    <= '0;
        fmt_err_o      <= '0;
        seq_err_o      <= '0;
        mr_cnt_o       <= '0;
        tu_cnt_o       <= '0;
        late_cnt_o     <= '0;
        early_cnt_o    <= '0;
        cnt_locked_o   <= '0;
        cnt_unlocked_o <= '0;
        cnt_intr_o     <= '0;
        //! the interval SEEN flags belong to the dead era too: a flag raised
        //! before the bind would commit +1 into a just-zeroed counter at the
        //! next tick and hand the new binding a phantom event
        iv_frx_r <= 1'b0;
        iv_uf_r  <= 1'b0;
        iv_sm_r  <= 1'b0;
        iv_mr_r  <= 1'b0;
        iv_tu_r  <= 1'b0;
        iv_lt_r  <= 1'b0;
        iv_et_r  <= 1'b0;
        //! MEDIA_LOCKED and MEDIA_UNLOCKED are zeroed above, and Table 5.6
        //! reads that pair as state: "either MEDIA_LOCKED=MEDIA_UNLOCKED (in
        //! this case, the input stream is not synchronized on the media
        //! clock), or MEDIA_LOCKED=MEDIA_UNLOCKED+1". 0 == 0 says NOT
        //! synchronized, so the lock flag has to fall with them - and fall
        //! WITHOUT scoring the unlock, which would strand the sink at
        //! UNLOCKED = LOCKED + 1, a state the clause does not allow. This
        //! assignment is the last writer in the block, so it also overrides
        //! a timeout unlock landing in the same cycle (the 4d31ecfb
        //! sil_pend/servo_pend rule, in a flat engine's spelling)
        locked_o <= 1'b0;
        //! the wipe is itself a wire-visible counter change (ten tallies
        //! fell to zero): the era's first push carries the fresh slate
        dirty_p_o <= 1'b1;
      end
    end
  end : engine

endmodule

`default_nettype wire
