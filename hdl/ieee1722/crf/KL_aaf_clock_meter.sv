/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_aaf_clock_meter.sv
  Description : The AAF clock meter: measures the media clock of ONE selected
                AAF Stream Input from its presentation timestamps, in the
                units KL_mmcm_drp_servo already takes from KL_crf_rx (gPTP ns
                per 512 ms window), so the servo follows an AAF talker
                through the same path it follows a CRF talker
                (docs/design/MEDIA_CLOCK_FOLLOWING.md, #629; decisions D2,
                D8 and the lost-PDU rule (b)).

                WHAT IT READS. The parser bundle KL_crf_rx taps: the match
                pulse and listener index, subtype, tv, the COMMON-header tu
                (byte o+3 bit 0 - not the tv net KL_crf_rx takes for the CRF
                header), mr, sequence_num, the 32-bit avtp_timestamp and the
                AAF format-specific header. An AAF talker's media clock is in
                its presentation times (IEEE 1722-2016 4.3.2).

                THE SUPPORTED FORMAT (Milan v1.2 6.2's 48 kHz Base format):
                subtype AAF, tv set (a clear tv means the timestamp is to be
                ignored, IEEE 1722-2016 4.4.4.5), format INT_32BIT, nsr
                48 kHz, sp clear (normal mode: a timestamp in every PDU,
                7.2.4), and 6 samples per PDU. AAF carries no samples-per-PDU
                field, so the count is derived from the PDU's own fields:
                stream_data_length = 6 x 4 x channels_per_frame octets, with
                channels_per_frame nonzero (7.3.3, 7.3.5). Any other PDU is
                not consumed: a stream of it never locks the meter, so the
                servo holds over rather than following a guess.

                THE PICK. One value per group of 16 PDUs, the PDUs whose
                sequence_num modulo 16 runs 0..15: 96 samples, the CRF
                timestamp_interval, 2 ms nominal. 16 divides 256, so groups
                stay aligned across the 8-bit wrap (4.4.4.6). The kept value
                is the group MEAN,
                  pick = ts_0 + floor(sum_i (ts_i - ts_0 - i*125000) / 16),
                exact modulo 2^32 like KL_crf_rx's ring arithmetic. Each PDU
                is compared with PDU 0 as it arrives: a deviation above the
                4096 ns jump bound restarts the history at once.

                THE RATE (D8 = E8). A two-point difference over 8 x 256
                picks, 4.096 s:
                  rate = (P_now - P_8_snapshots_ago - 8 * 512,000,000) >>> 3,
                from an 8-entry snapshot ring written every 256 group
                intervals (read-old, write-new at one address). Valid once
                2048 group intervals have passed since the history last
                restarted; it updates every 512 ms and holds between.

                LOST PDUs, rule (b). A sequence gap voids the group it falls
                in and restarts nothing; the deviation check runs up to the
                gap. The next valid pick is compared with the last one across
                k group intervals, k from the two groups' sequence_num[7:4]
                modulo 16: k = 1 is the adjacent check (2 ms +/- 4096 ns),
                k = 2 (one voided group between) is 4 ms +/- 5120 ns, and
                every other k restarts the history (k = 0 is 16 intervals).
                A loss-voided snapshot group is filled with the midpoint of
                its two neighbours, so snapshots stay on the group grid.

                HISTORY RESTARTS. Data: a tu edge, a deviation void, a pick
                spacing outside its bound (counted in status_o[15:8], the
                bench's measurement of a talker's regularity). Era: the
                followed input's bind edge, 100 ms without a consumed PDU, a
                change of the followed listener, entry into AAF following.

                LOCK, ERA, mr. 8 clean consecutive consumed PDUs lock, 100 ms
                without one unlocks (the AAF media-lock contract KL_crf_rx
                mirrors); a sequence gap breaks the settle run before lock
                and does not drop a lock already held. ONLY the meter's own
                100 ms timeout is a disruption and pulses disrupt_p_o. A
                change of the followed listener, entry into and exit from
                AAF following clear the lock in one cycle and pulse nothing:
                the source change itself is the restart KL_media_clock_
                restart declares, so a switch raises exactly one request.
                The received-mr reference is seeded silently by an era's
                first consumed PDU. While en_i is low the meter holds its
                era reset: no lock, no rate, no pulse.

                TIMING. The parser fires at most once per frame, and an
                Ethernet frame is at least 64 octets, so two parse pulses are
                at least 64/(TDATA_WIDTH/8) cycles apart; the per-PDU pipeline
                below is three stages and the group-end sequence six, both
                inside that spacing (an accept that lands while the group-end
                sequence still runs is consumed for lock and mr but leaves its
                group voided, a structurally safe outcome the spacing never
                reaches).

  Spec refs   : IEEE 1722-2016 4.3.2, 4.4.4.3, 4.4.4.5, 4.4.4.6, 4.4.4.7,
                7.2.4, 7.3.3, 7.3.5, 10.6, 10.8 Equation (15); Milan v1.2
                6.2, 7.3.2; docs/design/MEDIA_CLOCK_FOLLOWING.md
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

module KL_aaf_clock_meter
  import avtp_subtype_pkg::*;
#(
  //! clk_i frequency in Hz: the 100 ms lock timeout is derived from it
  parameter int unsigned CLK_FREQ_HZ_P = 50_000_000,
  //! AAF listeners the parser's match index can name
  parameter int unsigned N_LISTENERS_P = 1,
  localparam int unsigned IDXW_P = (N_LISTENERS_P <= 1) ? 1 : $clog2(N_LISTENERS_P)
)(
  //! the meter's one clock (milan_datapath axis_clk); every port below is
  //! synchronous to it, and no input crosses a clock domain
  input  wire                     clk_i,
  //! synchronous active-low reset: every register clears (unlocked, no rate,
  //! no history, no pulse, the status counters at zero)
  input  wire                     rst_n,

  //! the ONE selection gate: AAF following is selected (milan_datapath
  //! aaf_clk_selected_r). Low holds the meter's era reset.
  input  wire                     en_i,
  //! the followed AAF listener (milan_datapath aaf_follow_idx_r)
  input  wire [IDXW_P-1:0]        follow_idx_i,
  //! per-listener not-bound -> bound edge (KL_stream_table bind_rise_o)
  input  wire [N_LISTENERS_P-1:0] bind_rise_i,
  //! per-listener Milan v1.2 5.3.8.7 stopped state: a stopped input's PDUs
  //! are not consumed, so it is silent to this meter
  input  wire [N_LISTENERS_P-1:0] stopped_i,

  //! parser bundle (avtp_stream_parser, the tap KL_crf_rx uses)
  input  wire                     match_p_i,    //! matched stream frame
  input  wire [IDXW_P-1:0]        match_idx_i,  //! matched listener
  //! AVTP subtype (o+0); only AAF is consumed
  input  wire [7:0]               subtype_i,
  input  wire                     tv_i,         //! timestamp valid (o+1 bit 0)
  input  wire                     tu_i,         //! common-header tu (o+3 bit 0)
  input  wire                     mr_i,         //! media clock restart (o+1 bit 3)
  input  wire [7:0]               seq_i,        //! sequence_num
  input  wire [31:0]              ts_ns_i,      //! avtp_timestamp (gPTP ns)
  //! AAF format-specific header as received, octet o+16 in [63:56] down to
  //! octet o+23 in [7:0] (IEEE 1722-2016 Figure 26)
  input  wire [63:0]              fsh_i,

  //! 8 consumed PDUs in, 100 ms without one out
  output logic                    locked_o,
  //! the talker's rate in KL_crf_rx rate_o units: signed gPTP ns of the
  //! talker's 512 ms of media time, minus 512 ms (a 4.096 s mean)
  output logic signed [31:0]      rate_ns_o,
  output wire                     rate_valid_o,
  //! one-cycle pulse: the meter's own 100 ms timeout dropped its lock
  output logic                    disrupt_p_o,
  //! one-cycle pulse: the followed stream's received mr level toggled
  output logic                    mr_toggle_p_o,
  //! the largest |deviation| of a consumed PDU from its group's PDU 0 in
  //! this era, in ns, saturating at 65535; a level, cleared by an era start
  //! (AAFM_STAT[31:16])
  output wire  [15:0]             max_dev_ns_o,
  //! {data-caused history restarts [15:8] (wrapping), followed listener
  //!  [7:4], 1'b0, en [2], rate valid [1], locked [0]}: levels
  //!  (AAFM_STAT[15:0])
  output wire  [15:0]             status_o
);

  // ---------------------------------------------------------------------- //
  //  Format and grid constants, derived from the clauses that fix them     //
  // ---------------------------------------------------------------------- //
  //! IEEE 1722-2016 Table 9 (AAF format) INT_32BIT, Table 11 (nsr) 48 kHz
  localparam logic [7:0] AAF_FMT_INT32_C = 8'h02;
  localparam logic [3:0] AAF_NSR_48K_C   = 4'h5;
  //! Milan v1.2 6.2: 6 samples per PDU at 48 kHz, 4 octets per INT_32BIT
  //! sample
  localparam int unsigned FS_HZ_C          = 48_000;
  localparam int unsigned SMP_PER_PDU_C    = 6;
  localparam int unsigned SAMPLE_OCTETS_C  = 4;
  localparam int unsigned PDU_OCTETS_PER_CH_C = SMP_PER_PDU_C * SAMPLE_OCTETS_C;
  //! one PDU's 6 samples at 48 kHz, exactly (64-bit: 6e9 overflows 32)
  localparam longint unsigned SMP_NS_X_FS_C = 64'(SMP_PER_PDU_C) * 64'd1_000_000_000;
  localparam int unsigned PDU_NS_C = 32'(SMP_NS_X_FS_C / 64'(FS_HZ_C));
  //! 16 PDUs = 96 samples = the CRF timestamp_interval (Milan v1.2 7.3.2)
  localparam int unsigned GRP_LOG2_C = 4;
  localparam int unsigned GRP_NS_C   = PDU_NS_C << GRP_LOG2_C;
  //! snapshots every 256 group intervals (512 ms, the servo's window), 8 of
  //! them in the ring: the E8 span is 4.096 s
  localparam int unsigned SNAP_LOG2_C = 8;
  localparam int unsigned RING_LOG2_C = 3;
  localparam logic [31:0] NOM_SNAP_NS_C = 32'(GRP_NS_C) << SNAP_LOG2_C;
  localparam logic [31:0] NOM_SPAN_NS_C = NOM_SNAP_NS_C << RING_LOG2_C;
  //! the jump bound (design, The jump bound): two picks each up to the
  //! design point off the grid, plus the rate term over one group at
  //! 300 ppm (200 ppm PHC trim and a 100 ppm oscillator margin, the
  //! KL_crf_rx derivation), rounded up to a power of two. The design point
  //! is IEEE 1722-2016 10.8 Equation (15)'s 5 % of a sample period, plus
  //! the 384 ns KL_crf_rx assumes for the CRF timing points.
  localparam int unsigned EQ15_NS_C   = (1_000_000_000 / FS_HZ_C + 19) / 20;
  localparam int unsigned TS_ERR_NS_C = EQ15_NS_C + 384;
  localparam int unsigned DRIFT_NS_C  =
    (GRP_NS_C * (200 + 100) + (1_000_000 - 100) - 1) / (1_000_000 - 100);
  localparam int unsigned JUMP_NS_C   =
    1 << $clog2(2 * TS_ERR_NS_C + DRIFT_NS_C);
  //! the check across ONE voided group (k = 2): the design's ruled 5120 ns,
  //! inside the window that admits the design point and still catches a
  //! half-sample step (guarded below)
  localparam int unsigned GAP_NS_C    = 5120;
  localparam int unsigned HALF_SMP_NS_C = 1_000_000_000 / FS_HZ_C / 2;
  //! lock: 8 clean consecutive PDUs in, 100 ms of silence out
  localparam int unsigned SETTLE_C    = 8;
  localparam int unsigned TOUT_CYC_C  = CLK_FREQ_HZ_P / 10;
  localparam int unsigned TOUTW_C     = $clog2(TOUT_CYC_C + 1);

  if (64'(PDU_NS_C) * 64'(FS_HZ_C) != SMP_NS_X_FS_C) begin : g_pdu_exact
    $error("KL_aaf_clock_meter: 6 samples at 48 kHz must be an exact whole number of ns per PDU.");
  end : g_pdu_exact
  if (!(2 * TS_ERR_NS_C + 2 * DRIFT_NS_C <= GAP_NS_C &&
        GAP_NS_C + 2 * TS_ERR_NS_C + 2 * DRIFT_NS_C < HALF_SMP_NS_C)) begin : g_gap_window
    $error("KL_aaf_clock_meter: GAP_NS_C=%0d is outside the k = 2 window [2J + 2d, half sample - 2J - 2d) = [%0d, %0d).",
           GAP_NS_C, 2 * TS_ERR_NS_C + 2 * DRIFT_NS_C,
           HALF_SMP_NS_C - 2 * TS_ERR_NS_C - 2 * DRIFT_NS_C);
  end : g_gap_window
  if (JUMP_NS_C >= HALF_SMP_NS_C) begin : g_jump_bound
    $error("KL_aaf_clock_meter: the jump bound %0d ns no longer catches a half-sample step.", JUMP_NS_C);
  end : g_jump_bound

  // ---------------------------------------------------------------------- //
  //  Era control                                                           //
  // ---------------------------------------------------------------------- //
  //! the one selection gate, named once: every output and every era
  //! decision below reads this
  wire               en_w = en_i;
  logic              en_q_r;
  logic [IDXW_P-1:0] idx_q_r;
  logic [TOUTW_C-1:0] tout_r;
  wire en_rise_w  = en_w && !en_q_r;
  wire en_fall_w  = !en_w && en_q_r;
  wire idx_chg_w  = en_w && en_q_r && (follow_idx_i != idx_q_r);
  //! the followed listener's bind edge and stopped level, selected without
  //! a variable bit-select (an index past N_LISTENERS_P selects nothing)
  logic bind_rise_sel_w, stopped_w;
  always_comb begin : follow_sel
    bind_rise_sel_w = 1'b0;
    stopped_w       = 1'b0;
    for (int unsigned k = 0; k < N_LISTENERS_P; k++) begin
      if (32'(follow_idx_i) == k) begin
        bind_rise_sel_w = bind_rise_i[k];
        stopped_w       = stopped_i[k];
      end
    end
  end : follow_sel
  wire bind_rise_w = en_w && bind_rise_sel_w;
  //! 100 ms without a consumed PDU while following
  wire tout_fire_w = en_w && (tout_r == TOUTW_C'(TOUT_CYC_C));
  //! the events that start a new era: the measurement no longer describes
  //! the stream now followed, or the stream went silent
  wire era_start_w = en_rise_w || idx_chg_w || bind_rise_w || tout_fire_w;
  //! ...and the ones that clear a held lock SILENTLY (no disrupt_p)
  wire lock_clr_w  = en_rise_w || en_fall_w || idx_chg_w || !en_w;

  // ---------------------------------------------------------------------- //
  //  Stage 0: qualify the parse pulse                                      //
  // ---------------------------------------------------------------------- //
  //! the stream_data_length a 6-sample PDU of `cpf` channels carries,
  //! PDU_OCTETS_PER_CH_C x cpf, summed over the constant's set bits: a
  //! constant multiply written as shift-adds, so no tool spends a DSP48 on it
  //! (Yosys does not honour the use_dsp attribute KL_media_nco uses)
  function automatic logic [15:0] sdl_for(input logic [9:0] cpf);
    logic [15:0] acc;
    acc = '0;
    for (int b = 0; b < 16; b++)
      if (PDU_OCTETS_PER_CH_C[b]) acc = acc + (16'(cpf) << b);
    return acc;
  endfunction
  wire [7:0] f_format_w = fsh_i[63:56];
  wire [3:0] f_nsr_w    = fsh_i[55:52];
  wire [9:0] f_cpf_w    = fsh_i[49:40];
  wire [15:0] f_sdl_w   = fsh_i[31:16];
  wire       f_sp_w     = fsh_i[12];
  wire fmt_ok_w = (subtype_i == 8'(AAF)) && tv_i
               && (f_format_w == AAF_FMT_INT32_C) && (f_nsr_w == AAF_NSR_48K_C)
               && !f_sp_w && (f_cpf_w != 10'd0)
               && (f_sdl_w == sdl_for(f_cpf_w));
  //! a consumed PDU: the followed, started listener's, in the supported
  //! format, outside an era-start cycle (the era start wins)
  wire acc_w = en_w && match_p_i && (match_idx_i == follow_idx_i) && !stopped_w
            && fmt_ok_w && !era_start_w;

  // ---------------------------------------------------------------------- //
  //  Per-PDU pipeline: S1 latch, S2 deviation, S3 state update             //
  // ---------------------------------------------------------------------- //
  logic        s1_v_r, s2_v_r;
  logic [7:0]  s1_seq_r, s2_seq_r;
  logic [31:0] s1_ts_r,  s2_ts_r;
  logic        s1_tu_r,  s2_tu_r;
  logic        s1_mr_r,  s2_mr_r;
  logic        s2_gap_r;
  logic signed [31:0] s2_dev_r;

  //! sequence and lock state
  logic [7:0]  last_seq_r;
  logic        have_seq_r;
  logic [2:0]  settle_r;
  //! mr and tu references, seeded by an era's first consumed PDU
  logic        prev_mr_r, mr_seeded_r;
  logic        prev_tu_r, tu_seeded_r;
  //! the open group: PDU 0's timestamp, the next PDU's nominal offset, the
  //! running deviation sum, its group id
  logic        grp_act_r;
  logic [31:0] grp_ts0_r;
  logic [20:0] grp_off_r;
  logic signed [19:0] grp_sum_r;
  logic [3:0]  grp_id_r;
  //! group-end candidate handed to the history sequence
  logic        pc_v_r;
  logic [31:0] pc_ts0_r;
  logic signed [19:0] pc_sum_r;
  logic [3:0]  pc_id_r;
  //! data-caused restart requested by the per-PDU path (tu edge, deviation)
  logic        pdu_restart_r;
  //! status
  logic [15:0] max_dev_r;
  logic [7:0]  restart_cnt_r;

  //! deviation of the S1 PDU against its group's PDU 0 (exact mod 2^32)
  wire [31:0] s1_dev_w = s1_ts_r - grp_ts0_r - 32'(grp_off_r);
  wire        s1_gap_w = have_seq_r && (s1_seq_r != last_seq_r + 8'd1);
  //! |deviation| as an unsigned magnitude (2^31 itself reads 2^31)
  wire [31:0] s2_abs_w = s2_dev_r[31] ? 32'(-s2_dev_r) : 32'(s2_dev_r);
  wire        s2_in_bound_w = (s2_dev_r <= $signed(32'(JUMP_NS_C)))
                           && (s2_dev_r >= -$signed(32'(JUMP_NS_C)));
  wire [3:0]  s2_pos_w = s2_seq_r[3:0];
  wire [3:0]  s2_gid_w = s2_seq_r[7:4];
  wire        s2_tu_edge_w = tu_seeded_r && (s2_tu_r != prev_tu_r);

  // ---------------------------------------------------------------------- //
  //  History sequence (group end): G1 pick, G2 difference, G3 spacing and   //
  //  midpoint, G4 verdict and snapshot, G5/G6 rate                          //
  // ---------------------------------------------------------------------- //
  logic        g1_v_r, g2_v_r, g3_v_r;
  //! public: the meter suite times each rate update by this stage
  logic        g5_v_r /* verilator public_flat_rd */;
  logic [31:0] g_pick_r;
  logic [3:0]  g_id_r;
  logic [3:0]  g_k_r;
  logic [31:0] g_diff_r;
  logic signed [31:0] g_sp_r;
  logic [31:0] g_mid_r;
  logic        g_first_r;      //! the pick opens a history
  logic [31:0] g_snap_val_r;   //! the snapshot written at G4 (for G5)
  logic [31:0] g_snap_old_r;   //! the entry it replaced
  logic        g_rate_go_r;    //! G4 wrote a snapshot over a full ring
  logic signed [31:0] g_rdiff_r;

  logic        have_pick_r;
  logic [31:0] last_pick_r;
  logic [3:0]  last_id_r;
  logic [11:0] hist_cnt_r;     //! group intervals since the history started
  logic [RING_LOG2_C-1:0] ring_idx_r;
  logic [RING_LOG2_C:0]   ring_fill_r;
  logic        rate_valid_r;

  //! the snapshot ring: read-old, write-new at one address, KL_crf_rx's
  //! ring discipline at 8 entries. Distributed RAM, no reset: ring_fill_r
  //! guards every read, so an entry is never read before it is written.
  logic [31:0] ring_r [0:(1 << RING_LOG2_C) - 1];

  //! G4's verdict and snapshot writes, combinational over the G3 registers
  wire        g3_k_ok_w    = (g_k_r == 4'd1) || (g_k_r == 4'd2);
  wire [31:0] g3_bound_w   = (g_k_r == 4'd2) ? 32'(GAP_NS_C) : 32'(JUMP_NS_C);
  wire        g3_sp_ok_w   = g3_k_ok_w && ($signed(g_sp_r) <= $signed(g3_bound_w))
                                       && ($signed(g_sp_r) >= -$signed(g3_bound_w));
  wire [11:0] g3_c1_w      = hist_cnt_r + 12'd1;
  wire [11:0] g3_c2_w      = hist_cnt_r + 12'd2;
  //! k = 2: the voided group's interval may be a snapshot point (midpoint
  //! fill), else the pick's own; k = 1: the pick's
  wire        g3_snap_mid_w  = (g_k_r == 4'd2) && (g3_c1_w[SNAP_LOG2_C-1:0] == '0);
  wire        g3_snap_pick_w = (g_k_r == 4'd2) ? (g3_c2_w[SNAP_LOG2_C-1:0] == '0)
                                               : (g3_c1_w[SNAP_LOG2_C-1:0] == '0);

  assign rate_valid_o = rate_valid_r && en_w;
  assign max_dev_ns_o = max_dev_r;
  assign status_o     = {restart_cnt_r, 4'(follow_idx_i), 1'b0, en_w,
                         rate_valid_o, locked_o};

  //! snapshot ring port: one write per snapshot, the old entry read in the
  //! same access (G4 below captures it combinationally before the write)
  logic        ring_we_w;
  logic [31:0] ring_wd_w;
  always_ff @(posedge clk_i) begin : ring_port
    if (ring_we_w) ring_r[ring_idx_r] <= ring_wd_w;
  end : ring_port

  always_comb begin : ring_write
    ring_we_w = 1'b0;
    ring_wd_w = g_pick_r;
    if (g3_v_r && !era_start_w && !pdu_restart_r) begin
      if (g_first_r || !g3_sp_ok_w) begin
        ring_we_w = 1'b1;              //! the first snapshot of a new history
        ring_wd_w = g_pick_r;
      end else if (g3_snap_mid_w) begin
        ring_we_w = 1'b1;
        ring_wd_w = g_mid_r;
      end else if (g3_snap_pick_w) begin
        ring_we_w = 1'b1;
        ring_wd_w = g_pick_r;
      end
    end
  end : ring_write

  always_ff @(posedge clk_i) begin : meter_engine
    if (!rst_n) begin
      en_q_r <= 1'b0; idx_q_r <= '0; tout_r <= '0;
      s1_v_r <= 1'b0; s1_seq_r <= '0; s1_ts_r <= '0; s1_tu_r <= 1'b0;
      s1_mr_r <= 1'b0;
      s2_v_r <= 1'b0; s2_seq_r <= '0; s2_ts_r <= '0; s2_tu_r <= 1'b0;
      s2_mr_r <= 1'b0; s2_gap_r <= 1'b0; s2_dev_r <= '0;
      last_seq_r <= '0; have_seq_r <= 1'b0; settle_r <= '0;
      prev_mr_r <= 1'b0; mr_seeded_r <= 1'b0;
      prev_tu_r <= 1'b0; tu_seeded_r <= 1'b0;
      grp_act_r <= 1'b0; grp_ts0_r <= '0; grp_off_r <= '0; grp_sum_r <= '0;
      grp_id_r <= '0;
      pc_v_r <= 1'b0; pc_ts0_r <= '0; pc_sum_r <= '0; pc_id_r <= '0;
      pdu_restart_r <= 1'b0;
      max_dev_r <= '0; restart_cnt_r <= '0;
      g1_v_r <= 1'b0; g2_v_r <= 1'b0; g3_v_r <= 1'b0; g5_v_r <= 1'b0;
      g_pick_r <= '0; g_id_r <= '0; g_k_r <= '0; g_diff_r <= '0;
      g_sp_r <= '0; g_mid_r <= '0; g_first_r <= 1'b0;
      g_snap_val_r <= '0; g_snap_old_r <= '0; g_rate_go_r <= 1'b0;
      g_rdiff_r <= '0;
      have_pick_r <= 1'b0; last_pick_r <= '0; last_id_r <= '0;
      hist_cnt_r <= '0; ring_idx_r <= '0; ring_fill_r <= '0;
      rate_valid_r <= 1'b0; rate_ns_o <= '0;
      locked_o <= 1'b0; disrupt_p_o <= 1'b0; mr_toggle_p_o <= 1'b0;
    end else begin
      en_q_r  <= en_w;
      idx_q_r <= follow_idx_i;
      disrupt_p_o   <= 1'b0;
      mr_toggle_p_o <= 1'b0;
      pdu_restart_r <= 1'b0;

      // ---------------- lock timeout ----------------
      if (!en_w || acc_w || era_start_w) tout_r <= '0;
      else                               tout_r <= tout_r + 1'b1;

      // ---------------- S1: latch the consumed PDU ----------------
      s1_v_r   <= acc_w;
      if (acc_w) begin
        s1_seq_r <= seq_i;
        s1_ts_r  <= ts_ns_i;
        s1_tu_r  <= tu_i;
        s1_mr_r  <= mr_i;
      end

      // ---------------- S2: gap and deviation ----------------
      s2_v_r <= s1_v_r;
      if (s1_v_r) begin
        s2_seq_r <= s1_seq_r;
        s2_ts_r  <= s1_ts_r;
        s2_tu_r  <= s1_tu_r;
        s2_mr_r  <= s1_mr_r;
        s2_gap_r <= s1_gap_w;
        //! PDU 0 is its own reference
        s2_dev_r <= (s1_seq_r[3:0] == 4'd0) ? 32'sd0 : $signed(s1_dev_w);
      end

      // ---------------- S3: per-PDU state update ----------------
      pc_v_r <= 1'b0;
      if (s2_v_r) begin
        //! lock: a gap breaks the settle run, never a held lock
        if (s2_gap_r)                              settle_r <= '0;
        else if (settle_r != 3'(SETTLE_C - 1))     settle_r <= settle_r + 3'd1;
        else if (!locked_o)                        locked_o <= 1'b1;
        last_seq_r <= s2_seq_r;
        have_seq_r <= 1'b1;
        //! the received restart, against this era's seeded reference
        if (mr_seeded_r && (s2_mr_r != prev_mr_r)) mr_toggle_p_o <= 1'b1;
        prev_mr_r   <= s2_mr_r;
        mr_seeded_r <= 1'b1;
        prev_tu_r   <= s2_tu_r;
        tu_seeded_r <= 1'b1;

        //! the group: PDU 0 opens one (a tu edge there still opens it, under
        //! the new history); a gap voids the open one; a deviation beyond
        //! the jump bound restarts the history at once
        if (s2_pos_w == 4'd0) begin
          grp_act_r <= 1'b1;
          grp_ts0_r <= s2_ts_r;
          grp_off_r <= 21'(PDU_NS_C);
          grp_sum_r <= '0;
          grp_id_r  <= s2_gid_w;
        end else if (s2_gap_r || !grp_act_r || s2_tu_edge_w) begin
          grp_act_r <= 1'b0;
        end else begin
          if (s2_abs_w > 32'd65535)            max_dev_r <= 16'hFFFF;
          else if (16'(s2_abs_w) > max_dev_r)  max_dev_r <= 16'(s2_abs_w);
          if (!s2_in_bound_w) begin
            grp_act_r     <= 1'b0;
            pdu_restart_r <= 1'b1;
          end else if (s2_pos_w == 4'd15) begin
            grp_act_r <= 1'b0;
            pc_v_r    <= 1'b1;
            pc_ts0_r  <= grp_ts0_r;
            pc_sum_r  <= grp_sum_r + 20'(s2_dev_r);
            pc_id_r   <= grp_id_r;
          end else begin
            grp_sum_r <= grp_sum_r + 20'(s2_dev_r);
            grp_off_r <= grp_off_r + 21'(PDU_NS_C);
          end
        end
        if (s2_tu_edge_w) pdu_restart_r <= 1'b1;
      end

      // ---------------- G1: the group mean ----------------
      g1_v_r <= pc_v_r;
      if (pc_v_r) begin
        g_pick_r <= pc_ts0_r + 32'(pc_sum_r >>> GRP_LOG2_C);
        g_id_r   <= pc_id_r;
      end
      // ---------------- G2: across k group intervals ----------------
      g2_v_r <= g1_v_r;
      if (g1_v_r) begin
        g_first_r <= !have_pick_r;
        g_k_r     <= g_id_r - last_id_r;
        g_diff_r  <= g_pick_r - last_pick_r;
      end
      // ---------------- G3: spacing error and the midpoint ----------------
      g3_v_r <= g2_v_r;
      if (g2_v_r) begin
        g_sp_r  <= $signed(g_diff_r
                   - ((g_k_r == 4'd2) ? 32'(2 * GRP_NS_C) : 32'(GRP_NS_C)));
        g_mid_r <= last_pick_r + {g_diff_r[31], g_diff_r[31:1]};
      end
      // ---------------- G4: verdict, history and snapshot ----------------
      g_rate_go_r <= 1'b0;
      if (g3_v_r) begin
        if (g_first_r || !g3_sp_ok_w) begin
          //! a new history: this pick is its first snapshot, at count 0. The
          //! ring runs on circularly; the fill count alone says how many of
          //! its entries belong to this history
          if (!g_first_r) restart_cnt_r <= restart_cnt_r + 8'd1;
          have_pick_r  <= 1'b1;
          hist_cnt_r   <= '0;
          ring_idx_r   <= ring_idx_r + 1'b1;
          ring_fill_r  <= (RING_LOG2_C+1)'(1);
          rate_valid_r <= 1'b0;
        end else begin
          hist_cnt_r <= (g_k_r == 4'd2) ? g3_c2_w : g3_c1_w;
          if (ring_we_w) begin
            ring_idx_r   <= ring_idx_r + 1'b1;
            g_snap_val_r <= ring_wd_w;
            g_snap_old_r <= ring_r[ring_idx_r];
            if (ring_fill_r == (RING_LOG2_C+1)'(1 << RING_LOG2_C))
              g_rate_go_r <= 1'b1;
            else
              ring_fill_r <= ring_fill_r + 1'b1;
          end
        end
        last_pick_r <= g_pick_r;
        last_id_r   <= g_id_r;
      end
      // ---------------- G5/G6: the E8 rate ----------------
      g5_v_r <= g_rate_go_r;
      if (g_rate_go_r) g_rdiff_r <= $signed(g_snap_val_r - g_snap_old_r - NOM_SPAN_NS_C);
      if (g5_v_r) begin
        rate_ns_o    <= g_rdiff_r >>> RING_LOG2_C;
        rate_valid_r <= 1'b1;
      end

      // ---------------- data-caused history restart ----------------
      //! a tu edge or a deviation void: the history restarts and the next
      //! valid pick opens a new one (counted for the bench)
      if (pdu_restart_r) begin
        restart_cnt_r <= restart_cnt_r + 8'd1;
        have_pick_r   <= 1'b0;
        rate_valid_r  <= 1'b0;
        ring_fill_r   <= '0;
        g1_v_r <= 1'b0; g2_v_r <= 1'b0; g3_v_r <= 1'b0; g5_v_r <= 1'b0;
        g_rate_go_r <= 1'b0;
      end

      // ---------------- era start and silence ----------------
      if (tout_fire_w && locked_o) begin
        disrupt_p_o <= 1'b1;               //! the ONE disruption pulse
      end
      if (era_start_w || !en_w) begin
        //! a new era: settle run, history and seeds restart in one cycle
        settle_r     <= '0;
        have_seq_r   <= 1'b0;
        mr_seeded_r  <= 1'b0;
        tu_seeded_r  <= 1'b0;
        grp_act_r    <= 1'b0;
        have_pick_r  <= 1'b0;
        rate_valid_r <= 1'b0;
        ring_fill_r  <= '0;
        s1_v_r <= 1'b0; s2_v_r <= 1'b0; pc_v_r <= 1'b0;
        g1_v_r <= 1'b0; g2_v_r <= 1'b0; g3_v_r <= 1'b0; g5_v_r <= 1'b0;
        g_rate_go_r <= 1'b0;
        pdu_restart_r <= 1'b0;
        mr_toggle_p_o <= 1'b0;
        max_dev_r     <= '0;
      end
      if (tout_fire_w) locked_o <= 1'b0;
      if (lock_clr_w)  locked_o <= 1'b0;
      if (!en_w) disrupt_p_o <= 1'b0;
    end
  end : meter_engine

endmodule

`default_nettype wire
