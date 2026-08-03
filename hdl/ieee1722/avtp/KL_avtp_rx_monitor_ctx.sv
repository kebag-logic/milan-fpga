/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_avtp_rx_monitor_ctx.sv
  Author      : Kebag Logic

  Date        : 2026-07-22
  Description : Shared NxN STREAM_INPUT diagnostic-counter engine
                (docs/NXN_ARCHITECTURE.md §1.2/§1.4, phase P2): ONE monitor
                datapath, N listener contexts in a BRAM-backed context RAM
                (LCTX). Per-PDU verdict contract = KL_avtp_rx_monitor
                (the pipewire-extracted engine): lock on first valid PDU /
                8-PDU settle / mismatch detect + interrupt(lost>=2) /
                100 ms silence unlock / per-PDU format compare (a rejected
                PDU affects nothing else) / counter reset ONLY on that
                stream's not-bound->bound edge [M-5.3.8.10].

                COUNTER SEMANTICS split per Milan v1.2 Table 5.6, exactly:

                * MEDIA_LOCKED / MEDIA_UNLOCKED / STREAM_INTERRUPTED are
                  EVENT counters ("incremented each time ...") - they RMW
                  the RAM at the event, as before.
                * SEQ_NUM_MISMATCH, MEDIA_RESET, TIMESTAMP_UNCERTAIN,
                  UNSUPPORTED_FORMAT, LATE_TIMESTAMP, EARLY_TIMESTAMP and
                  FRAMES_RX are OBSERVATION-INTERVAL counters ("incremented
                  at the end of every observation interval during which
                  ..."), interval <= 1 s. A per-PDU verdict only SETS a
                  per-stream seen flag; the interval tick pends the stream
                  and the walker commits +1 per flagged counter through the
                  normal serial RMW walk. N frame events inside one
                  interval therefore move each counter by AT MOST ONE -
                  the per-frame reading is IEEE 1722.1-2021 Table 7-153's,
                  not Milan's, and serving it read 8000x high at class A.
                  The tick derives from CLK_FREQ_HZ_P (IVAL_CYC_P default =
                  one second, the clause ceiling), the same derivation as
                  the talker's KL_talker_diag_ctx tick.
                * a flag set in the tick cycle itself is harvested INTO the
                  closing interval (the talker-side boundary rule); events
                  landing between a tick and its drain ride the closing
                  commit - counted once, one interval early at worst.

                LCTX record (spec §1.4, address {s, word[4:0]}, 32 words):
                  CFG  w0 SID_LO | w1 SID_HI | w2 FMT_LO | w3 FMT_HI
                       w4 CTRL {en[0], route[2:1]} (CSR-owned, P11)
                  DYN  w8 MON_STATE {prev_seq[7:0], settle[11:8],
                       media_locked[12], bound_q[13], wire_chans[21:14],
                       prev_mr[22], mr_seeded[23]}
                       w9 LAST_TS | w10 LAST_TSD
                       w11 DEPKT_CNT {drops[31:16], pdus[15:0]}
                  CNT  w16..w25 in 1722.1-2021 Table 7-157 offset order:
                       MEDIA_LOCKED, MEDIA_UNLOCKED, STREAM_INTERRUPTED,
                       SEQ_NUM_MISMATCH, MEDIA_RESET, TIMESTAMP_UNCERTAIN,
                       UNSUPPORTED_FORMAT, LATE_TIMESTAMP, EARLY_TIMESTAMP,
                       FRAMES_RX

                Engine rules (spec §1.4 + timing-risk register T1/T2):
                  - RAM house rules: ONE sync write process, ONE explicit
                    sync read port (defect-4 lineage). The CSR-window /
                    P11 port shares the engine's ports in idle slots
                    (engine-arbitrated - the spec's "port B" role). Hold
                    rd_en until rd_valid; poll wr_rdy for writes.
                  - serial RMW walk per event; free-running timers stay
                    OUT of the RAM: the 100 ms silence watchdog is a 7-bit
                    ms counter x N flop array on the shared 1 ms tick
                    (spec timer rule).
                  - stream-0 legacy view (0x6B8 CSR group + AECP
                    GET_COUNTERS inputs) is a write-through shadow updated
                    ONLY from the RAM write port (single source of update -
                    no inferred read-port replica, defect-4 rule).
                  - stream 0's current format comes from the legacy fmt0_i
                    input (AECP SET_STREAM_FORMAT); streams > 0 read FMT
                    from LCTX w2/w3 (CSR-window-written).
                  - the external-clock lock gate (clk_src/servo_conv) is
                    the RENDER stream's (render_sel_i); other streams lock
                    internal-style on the first valid PDU.

                N=1 deltas vs KL_avtp_rx_monitor (accepted, TB-gated):
                pdu_accept_p/dirty_p/counter updates land 2-3 cycles later
                (serial walk); the silence unlock fires on the ms grid
                (100-101 ms) instead of an exact cycle count; and the seven
                Table 5.6 interval counters count INTERVALS here where the
                flat instrument counts FRAMES (the flat module keeps the
                1722.1 per-frame reading on purpose - TBs use it as a
                frame-accurate loop-integrity probe). Wire bytes and accept
                verdicts are unchanged.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! Shared NxN Milan STREAM_INPUT monitor (NXN_ARCHITECTURE §1.2/§1.4, P2):
//! one engine, N listener contexts in the LCTX RAM (CNT region in Table
//! 7-157 offset order), serial RMW walk per lock/unlock/interrupt event,
//! Milan Table 5.6 observation-interval commit for the seven interval
//! counters (seen flags -> tick -> walk), per-stream ms-tick silence
//! watchdog in flops, stream-0 legacy outputs via write-through shadows.
//! `pdu_accept_p_o`+`pdu_accept_idx_o` = the depacketizer's per-stream
//! commit verdict.

`default_nettype none

module KL_avtp_rx_monitor_ctx #(
  parameter int unsigned N_LISTENERS_P = 1,           //! listener contexts
  parameter int unsigned CLK_FREQ_HZ_P = 50_000_000,  //! for the 1 ms tick
  //! Milan Table 5.6 observation interval in clk_i cycles, "implementation-
  //! specific and shall be less than or equal to 1 second" - the default
  //! DERIVES the 1 s ceiling from the clock parameter (never a mirrored
  //! cycle constant); TBs shrink it so a case sees interval boundaries
  parameter int unsigned IVAL_CYC_P    = CLK_FREQ_HZ_P
)(
  input  wire         clk_i,             //! Global clock
  input  wire         rst_n,             //! Active-low synchronous reset

  //! --- per-frame pulse bundle from avtp_stream_parser -------------------
  input  wire         match_valid_i,     //! one-cycle pulse per matched frame
  input  wire [3:0]   match_index_i,     //! matched stream index s
  input  wire [7:0]   subtype_i,         //! AVTP subtype of the matched PDU
  input  wire [7:0]   seq_num_i,         //! sequence_num of the matched PDU
  input  wire         ts_uncertain_i,    //! tu bit
  input  wire         ts_valid_i,        //! tv bit (avtp_ts meaningful)
  //! mr bit of the matched PDU. Milan Table 5.6 MEDIA_RESET counts the
  //! intervals in which this bit was TOGGLED, so the engine keeps the
  //! previous value per context in MON_STATE[22] (seeded, not counted, on
  //! the era's first accepted PDU - MON_STATE[23]).
  input  wire         media_restart_i,   //! mr bit (IEEE 1722-2016 4.4.4.3)
  input  wire [31:0]  avtp_ts_i,         //! presentation time of the PDU
  input  wire [63:0]  fsh_i,             //! bytes O+16..O+23 of the PDU

  //! --- per-stream binding (KL_stream_table) -----------------------------
  input  wire [N_LISTENERS_P-1:0] bound_i,      //! per-stream bound level
  input  wire [N_LISTENERS_P-1:0] bind_rise_i,  //! not-bound->bound pulses

  //! --- stream-0 legacy config (no-regression aliases) -------------------
  input  wire [63:0]  sid0_i,            //! sink-0 bound sid (LCTX w0/w1)
  input  wire [63:0]  fmt0_i,            //! current STREAM_INPUT[0] format

  //! --- media-clock / render-path context --------------------------------
  input  wire [31:0]  ptp_now_i,         //! PHC nanoseconds [31:0]
  input  wire [31:0]  pres_ofs_i,        //! presentation offset ns
  input  wire [15:0]  clk_src_i,         //! live clock_source_index
  input  wire         servo_conv_i,      //! playback clock converged
  input  wire [3:0]   render_sel_i,      //! RENDER stream index (route policy)

  //! --- depacketizer per-frame attribution (LCTX w11) --------------------
  input  wire         depkt_pdu_p_i,     //! payload PDU emitted pulse
  input  wire [3:0]   depkt_pdu_idx_i,   //! its stream index
  input  wire         depkt_drop_p_i,    //! overflow-dropped frame pulse
  input  wire [3:0]   depkt_drop_idx_i,  //! its stream index

  //! --- LCTX window port (P11 CSR window / TB; engine-arbitrated) --------
  input  wire         lctx_wr_en_i,      //! write request (poll wr_rdy)
  input  wire [7:0]   lctx_wr_addr_i,    //! {s[2:0], word[4:0]}
  input  wire [31:0]  lctx_wr_data_i,
  output logic        lctx_wr_rdy_o,     //! write accepted this cycle
  input  wire         lctx_rd_en_i,      //! read request (hold until valid)
  input  wire [7:0]   lctx_rd_addr_i,
  output logic [31:0] lctx_rd_data_o,
  output logic        lctx_rd_valid_o,   //! one-cycle: rd_data is the answer

  //! --- stream-0 legacy outputs (0x6B8 group / AECP GET_COUNTERS) --------
  output logic [31:0] cnt_media_locked_o,
  output logic [31:0] cnt_media_unlocked_o,
  output logic [31:0] cnt_stream_interrupted_o,
  output logic [31:0] cnt_seq_mismatch_o,
  output logic [31:0] cnt_ts_uncertain_o,
  output logic [31:0] cnt_unsupported_fmt_o,
  output logic [31:0] cnt_frames_rx_o,
  output logic [31:0] cnt_media_reset_o,
  output logic [31:0] cnt_late_ts_o,
  output logic [31:0] cnt_early_ts_o,
  //! Milan 1.3 5.3.8.10 additions: per-frame tv-bit tallies (1722.1-2021
  //! Table 7-157 offsets 24/28, "increments on receipt" - a per-frame
  //! definition, kept per-frame). TV + TNV = total accepted PDUs; the
  //! identity TV + TNV == FRAMES_RX holds only under 1722.1's per-frame
  //! FRAMES_RX reading, NOT under Milan Table 5.6's interval reading
  //! served here (the torture campaign's tv_plus_tnv_identity() encodes
  //! exactly this split).
  output wire [31:0] cnt_ts_valid_o,
  output wire [31:0] cnt_ts_not_valid_o,
  output logic        media_locked_o,    //! stream-0 lock state (level)
  output logic        dirty_p_o,         //! stream-0 counter-change pulse
  output logic        pdu_accept_p_o,    //! per-PDU commit verdict pulse
  output logic [3:0]  pdu_accept_idx_o,  //! its stream index
  output logic [7:0]  wire_chans_o,      //! RENDER stream's wire channels
  //! chmap follow-up 3: EVERY context's wire_chans as packed 4-bit fields
  //! (the render crossbar's per-stream de-interleave truth; 0 = stream
  //! default/2ch per its contract; >15ch saturates the nibble)
  output logic [N_LISTENERS_P*4-1:0] wire_chans_all_o,

  //! --- Milan 5.4.2.25 indexed counter read (AECP GET_COUNTERS) ----------
  //! Table 5.16 makes a PAAD-AE "implement and return" the Table 5.6
  //! counters for EACH Stream Input; the stream-0 legacy outputs above
  //! serve exactly one. This port serves them all: the write-through
  //! mirror below shadows every context's twelve counter words into flops
  //! (same mechanism as the stream-0 view, all streams), and the response
  //! builder reads the descriptor_index it is serving combinationally in
  //! its const-load cycle. Before this port, sink 1 answered a FULL 0xF3F
  //! mask over constant zeros - a claimed-valid counter serving a frozen
  //! zero, the exact R5 lie - and sinks >= 2 an empty mask.
  input  wire [3:0]                  diag_idx_i,
  output logic [12*32-1:0]           diag_cnt_o,  //! C_ML..C_FRX,C_TV,C_TNV order
  output logic [31:0] last_ts_o,         //! stream-0 last accepted avtp_ts
  output logic [31:0] last_tsd_o         //! stream-0 last signed ts_delta
);

  localparam int unsigned SETTLE_C             = 8;
  localparam int unsigned INTERRUPT_MIN_LOST_C = 2;
  localparam logic [31:0] EARLY_MARGIN_NS_C    = 32'd10_000_000;
  localparam int unsigned UNLOCK_MS_C          = 100;          //! 100 ms
  localparam int unsigned MS_DIV_C             = CLK_FREQ_HZ_P / 1000;
  localparam int unsigned IDXW_C = (N_LISTENERS_P <= 1) ? 1
                                                        : $clog2(N_LISTENERS_P);
  localparam int unsigned AW_C   = IDXW_C + 5;                 //! {s, word}

  //! LCTX word indices (spec §1.4)
  localparam logic [4:0] W_SID_LO_C = 5'd0,  W_SID_HI_C = 5'd1;
  localparam logic [4:0] W_FMT_LO_C = 5'd2,  W_FMT_HI_C = 5'd3;
  localparam logic [4:0] W_MONST_C  = 5'd8,  W_LTS_C    = 5'd9;
  localparam logic [4:0] W_LTSD_C   = 5'd10, W_DEPKT_C  = 5'd11;
  localparam logic [4:0] W_CNT0_C   = 5'd16;                   //! MEDIA_LOCKED
  //! CNT-region offsets (Table 7-157 order)
  localparam logic [3:0] C_ML_C = 4'd0, C_MU_C = 4'd1, C_SI_C = 4'd2,
                         C_SM_C = 4'd3, C_MR_C = 4'd4, C_TU_C = 4'd5,
                         C_UF_C = 4'd6, C_LT_C = 4'd7, C_ET_C = 4'd8,
                         C_FRX_C = 4'd9,
                         //! Milan 1.3 tv tallies APPENDED (columns 10/11 =
                         //! LCTX words 26/27) so every existing C_* consumer
                         //! keeps its index; the response builder alone maps
                         //! them to the 1722.1 block offsets 24/28
                         C_TV_C = 4'd10, C_TNV_C = 4'd11;

  function automatic [AW_C-1:0] laddr(input [IDXW_C-1:0] s, input [4:0] w);
    laddr = {s, w};
  endfunction

  // ======================================================================
  //  Event / state declarations
  // ======================================================================
  typedef struct packed {
    logic [IDXW_C-1:0] s;
    logic [7:0]        subtype;
    logic [7:0]        seq;
    logic              tu;
    logic              tv;
    logic              mr;
    logic [31:0]       ts;
    logic [63:0]       fsh;
    logic [31:0]       tsd;
    logic              late;
    logic              early;
  } pdu_evt_t;

  typedef enum logic [3:0] {
    M_IDLE_S,      //! event pick (issues FMT_LO (s>0) / MON_STATE (s0) read)
    M_PFRD2_S,     //! PDU s>0: latch FMT_LO, FMT_HI read issued
    M_PFRD3_S,     //! PDU: latch FMT_HI (s>0), MON_STATE read issued
    M_PDEC_S,      //! PDU: verdict on MON_STATE + bundle
    M_PWR_S,       //! PDU: w8/w9/w10 writes (accepted PDUs)
    M_INC_S,       //! serial RMW loop (counters / w11 / silence / bind-zero)
    M_BRD_S,       //! BIND: MON_STATE read issued
    M_BDEC_S,      //! BIND: preserved-field w8 write + CFG words
    M_EXTRD_S      //! window read turnaround
  } mstate_t;

  mstate_t           mst_r;
  pdu_evt_t          pq_r [2];
  logic [1:0]        pq_cnt_r;
  //! Milan 1.3 5.3.8.10 tv tallies as per-context FLOPS - counted at the
  //! accept verdict with zero added walk cycles; served to the AECP mirror
  //! slices 10/11 and the window's virtual LCTX words 26/27 from here
  logic [31:0]       tv_cnt_r  [N_LISTENERS_P];
  logic [31:0]       tnv_cnt_r [N_LISTENERS_P];
  pdu_evt_t          cur_r;
  logic [IDXW_C-1:0] ev_s_r;
  logic [63:0]       fmt_r;
  logic [31:0]       monst_r;
  logic [3:0]        wrph_r;
  logic [11:0]       inc_list_r;
  logic [3:0]        zero_idx_r;
  logic              inc_rd_q_r;
  logic              bind_zero_r;
  logic              w11_mode_r;
  logic              sil_mode_r;
  logic [15:0]       dpdu_add_r, ddrop_add_r;

  logic [N_LISTENERS_P-1:0] bind_pend_r;
  logic [N_LISTENERS_P-1:0] sil_pend_r;
  logic [N_LISTENERS_P-1:0] servo_pend_r;
  logic [2:0] dpdu_pend_r   [N_LISTENERS_P];
  logic [2:0] ddrop_pend_r  [N_LISTENERS_P];

  //! Milan Table 5.6 interval machinery: per-stream seen-flag masks in
  //! CNT-column format (only the seven interval columns are ever set, so
  //! synthesis prunes the rest) + the per-stream commit-pending bit
  logic [11:0]              iv_seen_r [N_LISTENERS_P];
  logic [N_LISTENERS_P-1:0] iv_pend_r;
  //! ONE parked counter-walk remainder (see the M_INC_S yield): the
  //! depacketizer's commit verdict must land before the frame's tlast, so
  //! a counter walk in flight when a PDU arrives parks here and resumes
  //! right after the PDU walk - counts stay exact, media frames never wait
  logic [11:0]       iv_res_list_r;
  logic [IDXW_C-1:0] iv_res_s_r;

  logic [N_LISTENERS_P-1:0] locked_sh_r;     //! media_locked mirror (w8[12])
  logic [7:0] chans_sh_r [N_LISTENERS_P];    //! wire_chans mirror (w8[21:14])
  always_comb begin : chans_fanout
    for (int c = 0; c < N_LISTENERS_P; c++)
      wire_chans_all_o[c*4 +: 4] =
          (chans_sh_r[c] > 8'd15) ? 4'd15 : chans_sh_r[c][3:0];
  end : chans_fanout
  logic [6:0] sil_ms_r   [N_LISTENERS_P];    //! silence watchdog, ms units

  // ======================================================================
  //  LCTX RAM - one sync write process, ONE explicit sync read port
  // ======================================================================
  logic [31:0]      lctx_r [(1 << AW_C)];   //! N*32 words (power-of-2 sized)
  logic             ram_we_w;
  logic [AW_C-1:0]  ram_waddr_w, ram_raddr_w;
  logic [31:0]      ram_wdata_w;
  logic [31:0]      ram_q_r;

  always_ff @(posedge clk_i) begin : lctx_write_port
    if (ram_we_w) lctx_r[ram_waddr_w] <= ram_wdata_w;
  end : lctx_write_port

  always_ff @(posedge clk_i) begin : lctx_read_port
    ram_q_r <= lctx_r[ram_raddr_w];
  end : lctx_read_port

  // ======================================================================
  //  1 ms tick (spec timer rule: free-running timers stay in flops)
  // ======================================================================
  logic [$clog2(MS_DIV_C)-1:0] ms_div_r;
  logic                        ms_tick_r;
  always_ff @(posedge clk_i) begin : ms_tick_gen
    if (!rst_n) begin
      ms_div_r  <= '0;
      ms_tick_r <= 1'b0;
    end
    else if (32'(ms_div_r) >= MS_DIV_C - 1) begin
      ms_div_r  <= '0;
      ms_tick_r <= 1'b1;
    end
    else begin
      ms_div_r  <= ms_div_r + 1'b1;
      ms_tick_r <= 1'b0;
    end
  end : ms_tick_gen

  // ======================================================================
  //  Table 5.6 observation-interval tick (free-running; the clause fixes
  //  only an upper bound on the interval, not its phase)
  // ======================================================================
  localparam int unsigned IVALW_C = (IVAL_CYC_P <= 2) ? 1
                                                      : $clog2(IVAL_CYC_P);
  logic [IVALW_C-1:0] iv_div_r;
  logic               iv_tick_r;
  always_ff @(posedge clk_i) begin : iv_tick_gen
    if (!rst_n) begin
      iv_div_r  <= '0;
      iv_tick_r <= 1'b0;
    end
    else if (32'(iv_div_r) >= IVAL_CYC_P - 1) begin
      iv_div_r  <= '0;
      iv_tick_r <= 1'b1;
    end
    else begin
      iv_div_r  <= iv_div_r + 1'b1;
      iv_tick_r <= 1'b0;
    end
  end : iv_tick_gen

  // ======================================================================
  //  Event capture combinationals
  // ======================================================================
  wire signed [31:0] tsd_w   = avtp_ts_i - ptp_now_i;
  wire               late_w  = tsd_w < 0;
  wire               early_w = !late_w &&
                       (unsigned'(tsd_w) > (pres_ofs_i + EARLY_MARGIN_NS_C));
  wire [IDXW_C-1:0]  midx_w  = match_index_i[IDXW_C-1:0];
  wire               penq_w  = match_valid_i && bound_i[midx_w] &&
                               (pq_cnt_r != 2'd2);
  pdu_evt_t          new_evt_w;
  always_comb begin : new_evt_pack
    new_evt_w = '{s: midx_w, subtype: subtype_i, seq: seq_num_i,
                  tu: ts_uncertain_i, tv: ts_valid_i, mr: media_restart_i,
                  ts: avtp_ts_i,
                  fsh: fsh_i, tsd: unsigned'(tsd_w), late: late_w,
                  early: early_w};
  end : new_evt_pack

  wire [IDXW_C-1:0] rsel_w = render_sel_i[IDXW_C-1:0];
  //! external-clock unlock condition - RENDER stream only (USER rule)
  wire servo_unlock_w = locked_sh_r[rsel_w] && (clk_src_i != 16'd0) &&
                        !servo_conv_i;

  logic depkt_any_w;
  always_comb begin : pend_scans
    depkt_any_w = 1'b0;
    for (int s = 0; s < N_LISTENERS_P; s++)
      if (dpdu_pend_r[s] != '0 || ddrop_pend_r[s] != '0) depkt_any_w = 1'b1;
  end : pend_scans

  wire pdisp_w = (mst_r == M_IDLE_S) && (pq_cnt_r != '0);
  //! fresh-PDU fast dispatch: an idle walker takes the live pulse bundle
  //! directly (skips the queue hop - the depacketizer commit window on
  //! short PDUs is the reason: accept must land before the frame's tlast)
  wire pdisp_new_w = (mst_r == M_IDLE_S) && penq_w && (pq_cnt_r == '0);
  //! interval-commit dispatch, same M_IDLE_S priority slot the FSM uses
  //! (below depkt, above the window read) - defined ONCE so the FSM branch
  //! and the flag-fold block can never disagree about the drain cycle
  wire iv_go_w = (mst_r == M_IDLE_S) && !pdisp_w && !pdisp_new_w &&
                 (bind_pend_r == '0) && (sil_pend_r == '0) &&
                 (servo_pend_r == '0) && !depkt_any_w &&
                 (iv_res_list_r == '0) && (iv_pend_r != '0);
  logic [IDXW_C-1:0] iv_s_w;
  always_comb begin : iv_pick
    iv_s_w = '0;
    for (int s = N_LISTENERS_P-1; s >= 0; s--)
      if (iv_pend_r[s]) iv_s_w = IDXW_C'(s);
  end : iv_pick
  //! the window read gets the port only when the engine is fully idle
  wire ext_rd_go_w = lctx_rd_en_i && (mst_r == M_IDLE_S) && !penq_w &&
                     (pq_cnt_r == '0) && (bind_pend_r == '0) &&
                     (sil_pend_r == '0) && (servo_pend_r == '0) &&
                     (iv_pend_r == '0) && (iv_res_list_r == '0) &&
                     !depkt_any_w;
  //! stream index being dispatched this idle cycle (drives the prefetch)
  wire [IDXW_C-1:0] disp_s_w = pdisp_new_w ? midx_w : pq_r[0].s;

  // ======================================================================
  //  Verdict combinationals (valid in M_PDEC_S; MON_STATE = ram_q_r)
  // ======================================================================
  function automatic [7:0]  ms_prev(input [31:0] w);   ms_prev   = w[7:0];   endfunction
  function automatic [3:0]  ms_settle(input [31:0] w); ms_settle = w[11:8];  endfunction
  function automatic        ms_locked(input [31:0] w); ms_locked = w[12];    endfunction
  function automatic        ms_prevmr(input [31:0] w); ms_prevmr = w[22];    endfunction
  function automatic        ms_mrsd(input [31:0] w);   ms_mrsd   = w[23];    endfunction

  //! expected AAF fields from the format u64 (H.1 quadlet layout)
  wire [7:0] f_subtype_w = fmt_r[63:56];
  wire [3:0] f_nsr_w     = fmt_r[51:48];
  wire [7:0] f_format_w  = fmt_r[47:40];
  wire [7:0] f_depth_w   = fmt_r[39:32];
  wire [9:0] f_chans_w   = fmt_r[31:22];

  //! received AAF fields from the format-specific header (wire layout)
  wire [7:0] p_format_w = cur_r.fsh[63:56];
  wire [3:0] p_nsr_w    = cur_r.fsh[55:52];
  wire [7:0] p_chans_w  = cur_r.fsh[47:40];
  wire [7:0] p_depth_w  = cur_r.fsh[39:32];
  wire       p_sp_w     = cur_r.fsh[12];

  //! reference aaf_pdu_format_matches + CHANNELS-ADAPTIVE bench rule
  wire fmt_ok_w = (cur_r.subtype == f_subtype_w) &&
                  (p_format_w  == f_format_w)  &&
                  (p_nsr_w     == f_nsr_w)     &&
                  (p_depth_w   == f_depth_w)   &&
                  (p_chans_w   != 8'd0)        &&
                  ({2'b00, p_chans_w} <= f_chans_w) &&
                  (p_sp_w      == 1'b0);

  wire [7:0] expected_w = ms_prev(ram_q_r) + 8'd1;
  wire [7:0] lost_w     = cur_r.seq - expected_w;
  //! lock gate: internal for non-render streams; render follows clk_src/servo
  wire lock_ok_w  = (ev_s_r != rsel_w) || (clk_src_i == 16'd0) || servo_conv_i;
  wire lock_now_w = !ms_locked(ram_q_r) && lock_ok_w;
  wire seq_mm_w   = ms_locked(ram_q_r) && (ms_settle(ram_q_r) == '0) &&
                    (cur_r.seq != expected_w);
  //! Milan Table 5.6 MEDIA_RESET trigger: "the 'mr' bit was toggled in any of
  //! the received Stream Data AVTPDUs" (IEEE 1722.1-2021 Table 7-157 agrees -
  //! "on a toggle of the mr bit"). mr is a LEVEL held for >= 8 AVTPDUs
  //! [1722-2016 4.4.4.3], so the EDGE is the event: the era's first accepted
  //! PDU only SEEDS the reference (no toggle has been observed yet).
  wire mr_toggle_w = ms_mrsd(ram_q_r) && (cur_r.mr != ms_prevmr(ram_q_r));

  //! new MON_STATE after an ACCEPTED PDU (mirror of the flat-monitor rules)
  logic [31:0] monst_next_w;
  always_comb begin : monst_calc
    monst_next_w        = ram_q_r;
    monst_next_w[21:14] = p_chans_w;                  // wire_chans
    monst_next_w[22]    = cur_r.mr;                   // mr level reference
    monst_next_w[23]    = 1'b1;                       // ... now seeded
    monst_next_w[7:0]   = cur_r.seq;                  // seed / advance
    if (!ms_locked(ram_q_r)) begin
      if (lock_ok_w) monst_next_w[12] = 1'b1;         // lock
      monst_next_w[11:8] = 4'(SETTLE_C);
    end
    else if (ms_settle(ram_q_r) != '0)
      monst_next_w[11:8] = ms_settle(ram_q_r) - 4'd1;
  end : monst_calc

  //! next CNT increment to service (priority = Table 7-157 order)
  logic [3:0] inc_next_w;
  always_comb begin : inc_pick
    inc_next_w = 4'd15;
    for (int k = 11; k >= 0; k--)
      if (inc_list_r[k]) inc_next_w = 4'(k);
  end : inc_pick

  //! this cycle's Table 5.6 interval-flag events, per stream: the M_PDEC_S
  //! verdict raises ALL SEVEN PDU-derived flags (the walk itself only writes
  //! w8/w9/w10 and the EVENT counters). Decoded once so the fold below can
  //! harvest a tick-cycle event into the closing interval instead of losing
  //! it.
  //!
  //! MEDIA_RESET is a RECEIVED-WIRE flag like the other six. It used to be
  //! raised by the I2S playback buffer's overrun/underrun rail instead -
  //! a LOCAL health signal, not the clause's trigger - which made the
  //! counter wrong in both directions: a talker-signalled restart never
  //! ticked it (traceability AVTP-5, pinned by avtp_rxmon [30c]), and on a
  //! DAC-less shape (I2SPB_P=0 ties the rail to 1'b0) it could not tick at
  //! all. The playback buffer's own health keeps its dedicated
  //! underrun/overrun CSR tallies, which is where a local rail belongs.
  logic [11:0] iv_set_w [N_LISTENERS_P];
  always_comb begin : iv_events
    for (int s = 0; s < N_LISTENERS_P; s++) iv_set_w[s] = '0;
    if (mst_r == M_PDEC_S) begin
      if (!fmt_ok_w)
        iv_set_w[ev_s_r] = 12'b1 << C_UF_C;
      else
        iv_set_w[ev_s_r] =
            (12'b1 << C_FRX_C)
          | (cur_r.tu     ? (12'b1 << C_TU_C) : 12'b0)
          | (cur_r.late   ? (12'b1 << C_LT_C) : 12'b0)
          | (cur_r.early  ? (12'b1 << C_ET_C) : 12'b0)
          | (seq_mm_w     ? (12'b1 << C_SM_C) : 12'b0)
          | (mr_toggle_w  ? (12'b1 << C_MR_C) : 12'b0);
    end
  end : iv_events

  // ======================================================================
  //  Engine write mux (combinational) + port arbitration
  // ======================================================================
  logic            eng_we_w;
  logic [AW_C-1:0] eng_waddr_w;
  logic [31:0]     eng_wdata_w;

  always_comb begin : eng_write_mux
    eng_we_w    = 1'b0;
    eng_waddr_w = '0;
    eng_wdata_w = '0;
    unique case (mst_r)
      M_PWR_S : begin
        eng_we_w = 1'b1;
        unique case (wrph_r)
          4'd0 : begin
            eng_waddr_w = laddr(ev_s_r, W_MONST_C);
            eng_wdata_w = monst_r;
          end
          4'd1 : begin
            eng_waddr_w = laddr(ev_s_r, W_LTS_C);
            eng_wdata_w = cur_r.ts;
          end
          default : begin
            eng_waddr_w = laddr(ev_s_r, W_LTSD_C);
            eng_wdata_w = cur_r.tsd;
          end
        endcase
      end
      M_INC_S : begin
        if (w11_mode_r) begin
          if (inc_rd_q_r) begin
            eng_we_w    = 1'b1;
            eng_waddr_w = laddr(ev_s_r, W_DEPKT_C);
            eng_wdata_w = {ram_q_r[31:16] + ddrop_add_r,
                           ram_q_r[15:0]  + dpdu_add_r};
          end
        end
        else if (sil_mode_r) begin
          if (wrph_r == 4'd1) begin
            eng_we_w    = 1'b1;
            eng_waddr_w = laddr(ev_s_r, W_CNT0_C | 5'(C_MU_C));
            eng_wdata_w = ram_q_r + 32'd1;
          end
          else if (wrph_r == 4'd3) begin
            eng_we_w    = 1'b1;
            eng_waddr_w = laddr(ev_s_r, W_MONST_C);
            eng_wdata_w = ram_q_r & ~32'h0000_1000;   // clear media_locked
          end
        end
        else if (bind_zero_r) begin
          eng_we_w    = 1'b1;
          eng_waddr_w = laddr(ev_s_r, W_CNT0_C | 5'(zero_idx_r));
          eng_wdata_w = 32'd0;
        end
        else if (inc_list_r != '0 && inc_rd_q_r) begin
          eng_we_w    = 1'b1;
          eng_waddr_w = laddr(ev_s_r, W_CNT0_C | 5'(inc_next_w));
          eng_wdata_w = ram_q_r + 32'd1;
        end
      end
      M_BDEC_S : begin
        unique case (wrph_r)
          4'd0 : begin
            eng_we_w    = 1'b1;
            eng_waddr_w = laddr(ev_s_r, W_MONST_C);
            //! preserve prev_seq + wire_chans; clear lock/settle (flat-
            //! monitor bind semantics) AND the mr seed [23:22] - the mr
            //! LEVEL belongs to the previous binding era, so carrying it
            //! across a bind would score the new talker's first PDU as a
            //! toggle that never happened
            eng_wdata_w = {ram_q_r[31:24], 2'b00, ram_q_r[21:14],
                           2'b00, 4'd0, ram_q_r[7:0]};
          end
          4'd1 : begin
            eng_we_w    = 1'b1;
            eng_waddr_w = laddr(ev_s_r, W_SID_LO_C);
            eng_wdata_w = sid0_i[31:0];
          end
          4'd2 : begin
            eng_we_w    = 1'b1;
            eng_waddr_w = laddr(ev_s_r, W_SID_HI_C);
            eng_wdata_w = sid0_i[63:32];
          end
          4'd3 : begin
            eng_we_w    = 1'b1;
            eng_waddr_w = laddr(ev_s_r, W_FMT_LO_C);
            eng_wdata_w = fmt0_i[31:0];
          end
          4'd4 : begin
            eng_we_w    = 1'b1;
            eng_waddr_w = laddr(ev_s_r, W_FMT_HI_C);
            eng_wdata_w = fmt0_i[63:32];
          end
          default : ;                               //! wrph 5: no write
        endcase
      end
      default : ;
    endcase
  end : eng_write_mux

  wire ext_wr_ok_w = lctx_wr_en_i && !eng_we_w;
  assign ram_we_w    = eng_we_w | ext_wr_ok_w;
  assign ram_waddr_w = eng_we_w ? eng_waddr_w : lctx_wr_addr_i[AW_C-1:0];
  assign ram_wdata_w = eng_we_w ? eng_wdata_w : lctx_wr_data_i;
  always_comb lctx_wr_rdy_o = ext_wr_ok_w;

  // ======================================================================
  //  Read-address mux (single explicit read port; walker owns it, the
  //  window gets fully-idle slots)
  // ======================================================================
  always_comb begin : rd_mux
    ram_raddr_w = laddr(ev_s_r, W_MONST_C);
    unique case (mst_r)
      M_IDLE_S  : ram_raddr_w = ext_rd_go_w
                    ? lctx_rd_addr_i[AW_C-1:0]
                    : laddr(disp_s_w, (disp_s_w == '0) ? W_MONST_C
                                                       : W_FMT_LO_C);
      M_PFRD2_S : ram_raddr_w = laddr(ev_s_r, W_FMT_HI_C);
      M_PFRD3_S : ram_raddr_w = laddr(ev_s_r, W_MONST_C);
      M_BRD_S   : ram_raddr_w = laddr(ev_s_r, W_MONST_C);
      M_INC_S   : begin
        if (w11_mode_r)
          ram_raddr_w = laddr(ev_s_r, W_DEPKT_C);
        else if (sil_mode_r)
          ram_raddr_w = (wrph_r == 4'd0)
                        ? laddr(ev_s_r, W_CNT0_C | 5'(C_MU_C))
                        : laddr(ev_s_r, W_MONST_C);
        else
          ram_raddr_w = laddr(ev_s_r, W_CNT0_C | 5'(inc_next_w));
      end
      default   : ram_raddr_w = laddr(ev_s_r, W_MONST_C);
    endcase
  end : rd_mux

  // ======================================================================
  //  Walker + shadows + legacy view
  // ======================================================================
  //! stream-0 legacy view decode: ANY write (engine or window) to a
  //! stream-0 word mirrors into the flat output registers
  wire        leg_hit_w  = ram_we_w && (ram_waddr_w[AW_C-1:5] == '0);
  wire [4:0]  leg_word_w = ram_waddr_w[4:0];

  //! Milan 5.4.2.25 all-context counter mirror: the SAME write-through
  //! mechanism as the stream-0 view, applied to every stream's ten counter
  //! words (W_CNT0_C .. W_CNT0_C+9). Flop cost N x 10 x 32; the RAM's one
  //! read port stays wholly the walker's, and the AECP builder reads the
  //! mirror combinationally through diag_idx_i.
  //! NO reset ON PURPOSE: the mirror shadows a BRAM that has none either.
  //! Both power up all-zero (Xilinx GSR / Verilator zero-init), and every
  //! later word arrives by write-through, so a reset clause adds nothing -
  //! except that it FORBIDS distributed-RAM inference and turns the array
  //! into N x 10 x 32 fabric flops + a read mux (measured: +894 LUT /
  //! +2,560 FF on the 8x8, the DRC UTLZ-1 round of 2026-07-28).
  //!
  //! TEN SEPARATE COLUMN ARRAYS, not one [N][10]: the single array's read
  //! side pulls all ten columns of one row at once, i.e. ten async read
  //! ports on one memory - yosys read-replicates that into RAM32M, Vivado
  //! DOES NOT (measured on the m0019b seeds: the attribute was on the
  //! declaration and the block still synthesized to 1,855 LUT of flops
  //! and muxes). Per column the memory is textbook 1W1R - one decoded
  //! write, one async read at diag_ridx_w - which both tools map to
  //! distributed RAM without ceremony.
  wire cntw_hit_w = ram_we_w &&
                    (ram_waddr_w[4:0] >= W_CNT0_C) &&
                    (ram_waddr_w[4:0] < W_CNT0_C + 5'd10) &&
                    (32'(ram_waddr_w[AW_C-1:5]) < N_LISTENERS_P);
  wire [3:0] cntw_col_w = 4'(ram_waddr_w[4:0] - W_CNT0_C);

  //! indexed combinational read: the ten Table 5.6 counters plus the two
  //! Milan 1.3 tv tallies for one sink, in C_ML..C_FRX,C_TV,C_TNV order;
  //! an out-of-range index clamps to 0 (the builder only presents
  //! directory-served indexes)
  wire [IDXW_C-1:0] diag_ridx_w = (32'(diag_idx_i) < N_LISTENERS_P)
                                  ? diag_idx_i[IDXW_C-1:0] : '0;

  for (genvar c = 0; c < 10; c++) begin : diag_mirror
    (* ram_style = "distributed" *)
    logic [31:0] col_r [N_LISTENERS_P];
    always_ff @(posedge clk_i) begin : col_wr
      if (cntw_hit_w && cntw_col_w == 4'(c))
        col_r[ram_waddr_w[AW_C-1:5]] <= ram_wdata_w;
    end : col_wr
    assign diag_cnt_o[c*32 +: 32] = col_r[diag_ridx_w];
  end : diag_mirror
  //! appended slices 10/11 = the tv tallies straight from the flop arrays
  assign diag_cnt_o[10*32 +: 32] = tv_cnt_r [diag_ridx_w];
  assign diag_cnt_o[11*32 +: 32] = tnv_cnt_r[diag_ridx_w];
  assign cnt_ts_valid_o     = tv_cnt_r [0];
  assign cnt_ts_not_valid_o = tnv_cnt_r[0];

  always_ff @(posedge clk_i) begin : ctx_walker
    if (!rst_n) begin
      mst_r       <= M_IDLE_S;
      pq_cnt_r    <= '0;
      pq_r[0]     <= '0;
      pq_r[1]     <= '0;
      for (int s2 = 0; s2 < N_LISTENERS_P; s2++) begin
        tv_cnt_r[s2]  <= '0;
        tnv_cnt_r[s2] <= '0;
      end
      cur_r       <= '0;
      ev_s_r      <= '0;
      fmt_r       <= '0;
      monst_r     <= '0;
      wrph_r      <= '0;
      inc_list_r  <= '0;
      zero_idx_r  <= '0;
      inc_rd_q_r  <= 1'b0;
      bind_zero_r <= 1'b0;
      w11_mode_r  <= 1'b0;
      sil_mode_r  <= 1'b0;
      dpdu_add_r  <= '0;
      ddrop_add_r <= '0;
      bind_pend_r  <= '0;
      sil_pend_r   <= '0;
      servo_pend_r <= '0;
      iv_pend_r    <= '0;
      iv_res_list_r <= '0;
      iv_res_s_r    <= '0;
      locked_sh_r  <= '0;
      for (int s = 0; s < N_LISTENERS_P; s++) begin
        chans_sh_r[s]    <= '0;
        sil_ms_r[s]      <= '0;
        iv_seen_r[s]     <= '0;
        dpdu_pend_r[s]   <= '0;
        ddrop_pend_r[s]  <= '0;
      end
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
      media_locked_o   <= 1'b0;
      dirty_p_o        <= 1'b0;
      pdu_accept_p_o   <= 1'b0;
      pdu_accept_idx_o <= '0;
      wire_chans_o     <= '0;
      last_ts_o        <= '0;
      last_tsd_o       <= '0;
      lctx_rd_data_o   <= '0;
      lctx_rd_valid_o  <= 1'b0;
    end
    else begin
      dirty_p_o       <= 1'b0;
      pdu_accept_p_o  <= 1'b0;
      lctx_rd_valid_o <= 1'b0;

      // ---- PDU bundle queue (enqueue/dispatch, race-free; a fast-
      //      dispatched fresh pulse never enters the queue) ---------------
      unique case ({penq_w && !pdisp_new_w, pdisp_w})
        2'b01 : begin
          pq_r[0]  <= pq_r[1];
          pq_cnt_r <= pq_cnt_r - 2'd1;
        end
        2'b10 : begin
          pq_r[pq_cnt_r[0]] <= new_evt_w;
          pq_cnt_r          <= pq_cnt_r + 2'd1;
        end
        2'b11 : begin
          if (pq_cnt_r == 2'd1) pq_r[0] <= new_evt_w;
          else begin
            pq_r[0] <= pq_r[1];
            pq_r[1] <= new_evt_w;
          end
        end
        default : ;
      endcase

      // ---- pending event capture ----------------------------------------
      for (int s = 0; s < N_LISTENERS_P; s++) begin
        if (bind_rise_i[s]) bind_pend_r[s] <= 1'b1;
        if (depkt_pdu_p_i && (32'(depkt_pdu_idx_i) == s) &&
            !(&dpdu_pend_r[s]))
          dpdu_pend_r[s] <= dpdu_pend_r[s] + 3'd1;
        if (depkt_drop_p_i && (32'(depkt_drop_idx_i) == s) &&
            !(&ddrop_pend_r[s]))
          ddrop_pend_r[s] <= ddrop_pend_r[s] + 3'd1;
        //! silence watchdog: ms-tick flop scan (spec timer rule)
        if (ms_tick_r && locked_sh_r[s]) begin
          if (32'(sil_ms_r[s]) >= UNLOCK_MS_C - 1) begin
            sil_pend_r[s] <= 1'b1;
            sil_ms_r[s]   <= '0;
          end
          else sil_ms_r[s] <= sil_ms_r[s] + 7'd1;
        end
      end
      if (servo_unlock_w) servo_pend_r[rsel_w] <= 1'b1;

      // ---- walker FSM ----------------------------------------------------
      unique case (mst_r)
        M_IDLE_S : begin
          inc_list_r  <= '0;
          bind_zero_r <= 1'b0;
          w11_mode_r  <= 1'b0;
          sil_mode_r  <= 1'b0;
          inc_rd_q_r  <= 1'b0;
          wrph_r      <= '0;
          zero_idx_r  <= '0;
          if (pdisp_new_w || pdisp_w) begin
            //! PDU first: a same-cycle bind still wins overall because its
            //! reset walk runs after the PDU walk (flat-monitor ordering)
            cur_r  <= pdisp_new_w ? new_evt_w : pq_r[0];
            ev_s_r <= disp_s_w;
            if (disp_s_w == '0) begin
              fmt_r <= fmt0_i;              //! stream-0 format alias
              mst_r <= M_PFRD3_S;           //! (covers the w8 read latency)
            end
            else mst_r <= M_PFRD2_S;        //! FMT_LO read already issued
          end
          else if (bind_pend_r != '0) begin
            for (int s = N_LISTENERS_P-1; s >= 0; s--)
              if (bind_pend_r[s]) ev_s_r <= IDXW_C'(s);
            mst_r <= M_BRD_S;
          end
          else if (sil_pend_r != '0 || servo_pend_r != '0) begin
            for (int s = N_LISTENERS_P-1; s >= 0; s--)
              if (sil_pend_r[s] || servo_pend_r[s]) ev_s_r <= IDXW_C'(s);
            sil_mode_r <= 1'b1;
            mst_r      <= M_INC_S;
          end
          else if (depkt_any_w) begin
            for (int s = N_LISTENERS_P-1; s >= 0; s--)
              if (dpdu_pend_r[s] != '0 || ddrop_pend_r[s] != '0) begin
                ev_s_r      <= IDXW_C'(s);
                dpdu_add_r  <= 16'(dpdu_pend_r[s]);
                ddrop_add_r <= 16'(ddrop_pend_r[s]);
              end
            w11_mode_r <= 1'b1;
            mst_r      <= M_INC_S;
          end
          else if (iv_res_list_r != '0) begin
            //! resume a parked counter walk first (its bits predate any
            //! newly pending interval commit)
            ev_s_r        <= iv_res_s_r;
            inc_list_r    <= iv_res_list_r;
            iv_res_list_r <= '0;
            mst_r         <= M_INC_S;
          end
          else if (iv_go_w) begin
            //! Table 5.6 interval commit: +1 per flagged counter through
            //! the normal serial RMW walk (the fold block below clears the
            //! flags and the pend bit this same cycle)
            ev_s_r     <= iv_s_w;
            inc_list_r <= iv_seen_r[iv_s_w];
            if (iv_s_w == '0 && iv_seen_r[iv_s_w] != '0) dirty_p_o <= 1'b1;
            mst_r      <= M_INC_S;
          end
          else if (ext_rd_go_w) begin
            mst_r <= M_EXTRD_S;
          end
        end

        M_PFRD2_S : begin
          fmt_r[31:0] <= ram_q_r;
          mst_r       <= M_PFRD3_S;
        end
        M_PFRD3_S : begin
          if (ev_s_r != '0) fmt_r[63:32] <= ram_q_r;
          mst_r <= M_PDEC_S;
        end

        M_PDEC_S : begin
          if (!fmt_ok_w) begin
            //! counts nothing else (reference early-return); UNSUPPORTED_
            //! FORMAT is an interval counter now - iv_events raised the
            //! flag this cycle, so there is nothing to walk
            mst_r <= M_IDLE_S;
          end
          else begin
            pdu_accept_p_o     <= 1'b1;
            pdu_accept_idx_o   <= 4'(ev_s_r);
            chans_sh_r[ev_s_r] <= p_chans_w;
            sil_ms_r[ev_s_r]   <= '0;
            if (lock_now_w) locked_sh_r[ev_s_r] <= 1'b1;
            if (ev_s_r == '0) dirty_p_o <= 1'b1;
            monst_r <= monst_next_w;
            //! TV/TNV live in flops (below), NOT in this serial walk: a
            //! 12th RMW step per accepted PDU delayed the next verdict
            //! enough that the hostplane ax8x8 shape dropped the 3rd of 3
            //! back-to-back frames at the depacketizer commit. They keep
            //! the 1722.1-2021 Table 7-153 per-frame reading; the seven
            //! Table 5.6 interval flags were raised by iv_events this
            //! cycle and commit at the interval tick, so only the EVENT
            //! counters walk here.
            if (cur_r.tv) tv_cnt_r[ev_s_r]  <= tv_cnt_r[ev_s_r]  + 32'd1;
            else          tnv_cnt_r[ev_s_r] <= tnv_cnt_r[ev_s_r] + 32'd1;
            inc_list_r <=
                (lock_now_w  ? (12'b1 << C_ML_C) : 12'b0)
              | ((seq_mm_w && lost_w >= 8'(INTERRUPT_MIN_LOST_C))
                             ? (12'b1 << C_SI_C) : 12'b0);
            wrph_r <= '0;
            mst_r  <= M_PWR_S;
          end
        end

        M_PWR_S : begin
          if (wrph_r == 4'd2) begin
            wrph_r <= '0;
            mst_r  <= M_INC_S;
          end
          else wrph_r <= wrph_r + 4'd1;
        end

        M_INC_S : begin
          if (w11_mode_r) begin
            if (!inc_rd_q_r) inc_rd_q_r <= 1'b1;
            else begin
              //! drain exactly the latched amounts (new pulses survive)
              dpdu_pend_r[ev_s_r]  <= dpdu_pend_r[ev_s_r]
                                      - 3'(dpdu_add_r)
                                      + ((depkt_pdu_p_i &&
                                          32'(depkt_pdu_idx_i) == 32'(ev_s_r))
                                         ? 3'd1 : 3'd0);
              ddrop_pend_r[ev_s_r] <= ddrop_pend_r[ev_s_r]
                                      - 3'(ddrop_add_r)
                                      + ((depkt_drop_p_i &&
                                          32'(depkt_drop_idx_i) == 32'(ev_s_r))
                                         ? 3'd1 : 3'd0);
              inc_rd_q_r <= 1'b0;
              w11_mode_r <= 1'b0;
              mst_r      <= M_IDLE_S;
            end
          end
          else if (sil_mode_r) begin
            unique case (wrph_r)
              4'd0 : wrph_r <= 4'd1;              // MU read in flight
              4'd1 : begin                         // MU written this cycle
                if (ev_s_r == '0) dirty_p_o <= 1'b1;
                wrph_r <= 4'd2;
              end
              4'd2 : wrph_r <= 4'd3;              // w8 read in flight
              default : begin                      // w8 written this cycle
                locked_sh_r[ev_s_r]  <= 1'b0;
                sil_ms_r[ev_s_r]     <= '0;
                sil_pend_r[ev_s_r]   <= 1'b0;
                servo_pend_r[ev_s_r] <= 1'b0;
                sil_mode_r <= 1'b0;
                wrph_r     <= '0;
                mst_r      <= M_IDLE_S;
              end
            endcase
          end
          else if (bind_zero_r) begin
            if (zero_idx_r == 4'd9) begin
              bind_zero_r <= 1'b0;
              zero_idx_r  <= '0;
              if (ev_s_r == '0) dirty_p_o <= 1'b1;
              mst_r <= M_IDLE_S;
            end
            else zero_idx_r <= zero_idx_r + 4'd1;
          end
          else if (inc_list_r == '0) begin
            mst_r <= M_IDLE_S;
          end
          else begin
            //! PDU pressure YIELDS the counter walk: the depacketizer's
            //! commit verdict must land BEFORE the frame's tlast beat, and
            //! an interval drain starting at an arbitrary tick phase pushed
            //! it one cycle past that window (hostplane ax8x8 lost 1 of 2
            //! back-to-back ring frames; the verdict landed ON the tlast).
            //! The park happens in the SAME cycle - between RMWs it costs
            //! the walk nothing, mid-RMW the in-flight write still lands
            //! and only the remainder parks - so the queued dispatch runs
            //! exactly one cycle behind the fast path. The remainder sits
            //! in the ONE resume slot and finishes right after the PDU
            //! walk - every bit still commits exactly once.
            if (!inc_rd_q_r) begin
              if ((penq_w || pq_cnt_r != '0) && (iv_res_list_r == '0)) begin
                iv_res_list_r <= inc_list_r;
                iv_res_s_r    <= ev_s_r;
                inc_list_r    <= '0;
                mst_r         <= M_IDLE_S;
              end
              else inc_rd_q_r <= 1'b1;
            end
            else begin
              inc_list_r[inc_next_w] <= 1'b0;
              inc_rd_q_r <= 1'b0;
              if ((penq_w || pq_cnt_r != '0) && (iv_res_list_r == '0)) begin
                iv_res_list_r <= inc_list_r & ~(12'b1 << inc_next_w);
                iv_res_s_r    <= ev_s_r;
                inc_list_r    <= '0;
                mst_r         <= M_IDLE_S;
              end
            end
          end
        end

        M_BRD_S : mst_r <= M_BDEC_S;

        M_BDEC_S : begin
          if (wrph_r == 4'd0) begin
            locked_sh_r[ev_s_r] <= 1'b0;
            sil_ms_r[ev_s_r]    <= '0;
            tv_cnt_r[ev_s_r]    <= '0;   //! Milan era wipe (Table 5.6 rule)
            tnv_cnt_r[ev_s_r]   <= '0;
            //! an unlock owed by the PREVIOUS era dies with it. Milan Table
            //! 5.6: "either MEDIA_LOCKED=MEDIA_UNLOCKED, or
            //! MEDIA_LOCKED=MEDIA_UNLOCKED+1" - and the bind zeroes BOTH, so
            //! a watchdog/servo unlock still pending here would walk +1 into
            //! MEDIA_UNLOCKED over a zeroed MEDIA_LOCKED and strand the
            //! stream at UNLOCKED=LOCKED+1, which is neither legal state
            sil_pend_r[ev_s_r]   <= 1'b0;
            servo_pend_r[ev_s_r] <= 1'b0;
            //! a parked walk remainder for THIS stream dies with the era
            //! too (its counters are zeroed by the bind-zero walk below)
            if (iv_res_s_r == ev_s_r) iv_res_list_r <= '0;
            //! only stream 0 records the legacy sid/fmt aliases; other
            //! streams' CFG words are CSR-window-owned
            wrph_r <= (ev_s_r == '0) ? 4'd1 : 4'd5;
          end
          else if (wrph_r == 4'd4 || wrph_r == 4'd5) begin
            bind_pend_r[ev_s_r] <= 1'b0;
            bind_zero_r <= 1'b1;
            zero_idx_r  <= '0;
            wrph_r      <= '0;
            mst_r       <= M_INC_S;
          end
          else wrph_r <= wrph_r + 4'd1;
        end

        M_EXTRD_S : begin
          //! words 26/27 are VIRTUAL (flop-backed tv tallies); everything
          //! else is the RAM word. The requester holds rd_addr until valid.
          //! stream select masked to the elaborated width: [7:5] is 3 bits
          //! wide but the arrays are N_LISTENERS_P deep (4 on the Arty), so
          //! an unmasked index 4..7 reads out of range (Opus review 07-29)
          unique case (lctx_rd_addr_i[4:0])
            (W_CNT0_C | 5'(C_TV_C))  :
              lctx_rd_data_o <= tv_cnt_r [IDXW_C'(lctx_rd_addr_i[7:5])];
            (W_CNT0_C | 5'(C_TNV_C)) :
              lctx_rd_data_o <= tnv_cnt_r[IDXW_C'(lctx_rd_addr_i[7:5])];
            default : lctx_rd_data_o <= ram_q_r;
          endcase
          lctx_rd_valid_o <= 1'b1;
          mst_r <= M_IDLE_S;
        end

        default : mst_r <= M_IDLE_S;
      endcase

      // ---- Table 5.6 interval flags: fold / tick-pend / drain / era wipe
      //      (single writer for iv_seen_r/iv_pend_r; a tick-cycle event is
      //      harvested into the closing interval, a drain-cycle event
      //      survives into the fresh one, and the bind wipe [M-5.3.8.10]
      //      clears history while keeping this cycle's own event) ---------
      for (int s = 0; s < N_LISTENERS_P; s++) begin
        if ((mst_r == M_BDEC_S) && (wrph_r == 4'd0) && (32'(ev_s_r) == s))
        begin
          iv_seen_r[s] <= iv_set_w[s];
          iv_pend_r[s] <= 1'b0;
        end
        else begin
          if (iv_go_w && (32'(iv_s_w) == s))
            iv_seen_r[s] <= iv_set_w[s];
          else
            iv_seen_r[s] <= iv_seen_r[s] | iv_set_w[s];
          if (iv_tick_r && ((iv_seen_r[s] | iv_set_w[s]) != '0))
            iv_pend_r[s] <= 1'b1;
          else if (iv_go_w && (32'(iv_s_w) == s))
            iv_pend_r[s] <= 1'b0;
        end
      end

      // ---- legacy stream-0 write-through view ---------------------------
      if (leg_hit_w) begin
        unique case (leg_word_w)
          W_LTS_C                  : last_ts_o                <= ram_wdata_w;
          W_LTSD_C                 : last_tsd_o               <= ram_wdata_w;
          (W_CNT0_C | 5'(C_ML_C))  : cnt_media_locked_o       <= ram_wdata_w;
          (W_CNT0_C | 5'(C_MU_C))  : cnt_media_unlocked_o     <= ram_wdata_w;
          (W_CNT0_C | 5'(C_SI_C))  : cnt_stream_interrupted_o <= ram_wdata_w;
          (W_CNT0_C | 5'(C_SM_C))  : cnt_seq_mismatch_o       <= ram_wdata_w;
          (W_CNT0_C | 5'(C_MR_C))  : cnt_media_reset_o        <= ram_wdata_w;
          (W_CNT0_C | 5'(C_TU_C))  : cnt_ts_uncertain_o       <= ram_wdata_w;
          (W_CNT0_C | 5'(C_UF_C))  : cnt_unsupported_fmt_o    <= ram_wdata_w;
          (W_CNT0_C | 5'(C_LT_C))  : cnt_late_ts_o            <= ram_wdata_w;
          (W_CNT0_C | 5'(C_ET_C))  : cnt_early_ts_o           <= ram_wdata_w;
          (W_CNT0_C | 5'(C_FRX_C)) : cnt_frames_rx_o          <= ram_wdata_w;
          default : ;
        endcase
      end

      // ---- continuous legacy levels -------------------------------------
      media_locked_o <= locked_sh_r[0];
      wire_chans_o   <= chans_sh_r[rsel_w];
    end
  end : ctx_walker

endmodule

`default_nettype wire
