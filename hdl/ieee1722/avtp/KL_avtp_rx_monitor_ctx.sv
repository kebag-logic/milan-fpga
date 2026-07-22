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
                (LCTX). Functional contract per stream = KL_avtp_rx_monitor
                (the pipewire-extracted Milan Table 7-156 engine): lock on
                first valid PDU / 8-PDU settle / SEQ_NUM_MISMATCH +
                STREAM_INTERRUPTED(lost>=2) / 100 ms silence unlock /
                per-PDU format compare (UNSUPPORTED_FORMAT counts nothing
                else) / TIMESTAMP_UNCERTAIN / LATE+EARLY / MEDIA_RESET /
                counter reset ONLY on that stream's not-bound->bound edge
                [M-5.3.8.10].

                LCTX record (spec §1.4, address {s, word[4:0]}, 32 words):
                  CFG  w0 SID_LO | w1 SID_HI | w2 FMT_LO | w3 FMT_HI
                       w4 CTRL {en[0], route[2:1]} (CSR-owned, P11)
                  DYN  w8 MON_STATE {prev_seq[7:0], settle[11:8],
                       media_locked[12], bound_q[13], wire_chans[21:14]}
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

                N=1 bit-compat deltas vs KL_avtp_rx_monitor (accepted,
                TB-gated): pdu_accept_p/dirty_p/counter updates land 2-3
                cycles later (serial walk); the silence unlock fires on the
                ms grid (100-101 ms) instead of an exact cycle count. Wire
                bytes, counter values and CSR semantics are unchanged.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! Shared NxN Milan STREAM_INPUT monitor (NXN_ARCHITECTURE §1.2/§1.4, P2):
//! one engine, N listener contexts in the LCTX RAM (CNT region in Table
//! 7-157 offset order), serial RMW walk per event, per-stream ms-tick
//! silence watchdog in flops, stream-0 legacy outputs via write-through
//! shadows. `pdu_accept_p_o`+`pdu_accept_idx_o` = the depacketizer's
//! per-stream commit verdict.

`default_nettype none

module KL_avtp_rx_monitor_ctx #(
  parameter int unsigned N_LISTENERS_P = 1,           //! listener contexts
  parameter int unsigned CLK_FREQ_HZ_P = 50_000_000   //! for the 1 ms tick
)(
  input  wire         clk_i,             //! Global clock
  input  wire         rst_n,             //! Active-low synchronous reset

  //! --- per-frame pulse bundle from avtp_stream_parser -------------------
  input  wire         match_valid_i,     //! one-cycle pulse per matched frame
  input  wire [3:0]   match_index_i,     //! matched stream index s
  input  wire [7:0]   subtype_i,         //! AVTP subtype of the matched PDU
  input  wire [7:0]   seq_num_i,         //! sequence_num of the matched PDU
  input  wire         ts_uncertain_i,    //! tu bit
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
  input  wire         media_reset_p_i,   //! playback servo rail event (pulse)
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
  output logic        media_locked_o,    //! stream-0 lock state (level)
  output logic        dirty_p_o,         //! stream-0 counter-change pulse
  output logic        pdu_accept_p_o,    //! per-PDU commit verdict pulse
  output logic [3:0]  pdu_accept_idx_o,  //! its stream index
  output logic [7:0]  wire_chans_o,      //! RENDER stream's wire channels
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
                         C_FRX_C = 4'd9;

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
  pdu_evt_t          cur_r;
  logic [IDXW_C-1:0] ev_s_r;
  logic [63:0]       fmt_r;
  logic [31:0]       monst_r;
  logic [3:0]        wrph_r;
  logic [9:0]        inc_list_r;
  logic [3:0]        zero_idx_r;
  logic              inc_rd_q_r;
  logic              bind_zero_r;
  logic              w11_mode_r;
  logic              sil_mode_r;
  logic [15:0]       dpdu_add_r, ddrop_add_r;
  logic [1:0]        mr_add_r;

  logic [N_LISTENERS_P-1:0] bind_pend_r;
  logic [N_LISTENERS_P-1:0] sil_pend_r;
  logic [N_LISTENERS_P-1:0] servo_pend_r;
  logic [1:0] mreset_pend_r [N_LISTENERS_P];
  logic [2:0] dpdu_pend_r   [N_LISTENERS_P];
  logic [2:0] ddrop_pend_r  [N_LISTENERS_P];

  logic [N_LISTENERS_P-1:0] locked_sh_r;     //! media_locked mirror (w8[12])
  logic [7:0] chans_sh_r [N_LISTENERS_P];    //! wire_chans mirror (w8[21:14])
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
                  tu: ts_uncertain_i, ts: avtp_ts_i, fsh: fsh_i,
                  tsd: unsigned'(tsd_w), late: late_w, early: early_w};
  end : new_evt_pack

  wire [IDXW_C-1:0] rsel_w = render_sel_i[IDXW_C-1:0];
  //! external-clock unlock condition - RENDER stream only (USER rule)
  wire servo_unlock_w = locked_sh_r[rsel_w] && (clk_src_i != 16'd0) &&
                        !servo_conv_i;

  logic mreset_any_w, depkt_any_w;
  always_comb begin : pend_scans
    mreset_any_w = 1'b0;
    depkt_any_w  = 1'b0;
    for (int s = 0; s < N_LISTENERS_P; s++) begin
      if (mreset_pend_r[s] != '0) mreset_any_w = 1'b1;
      if (dpdu_pend_r[s] != '0 || ddrop_pend_r[s] != '0) depkt_any_w = 1'b1;
    end
  end : pend_scans

  wire pdisp_w = (mst_r == M_IDLE_S) && (pq_cnt_r != '0);
  //! fresh-PDU fast dispatch: an idle walker takes the live pulse bundle
  //! directly (skips the queue hop - the depacketizer commit window on
  //! short PDUs is the reason: accept must land before the frame's tlast)
  wire pdisp_new_w = (mst_r == M_IDLE_S) && penq_w && (pq_cnt_r == '0);
  //! the window read gets the port only when the engine is fully idle
  wire ext_rd_go_w = lctx_rd_en_i && (mst_r == M_IDLE_S) && !penq_w &&
                     (pq_cnt_r == '0) && (bind_pend_r == '0) &&
                     (sil_pend_r == '0) && (servo_pend_r == '0) &&
                     !mreset_any_w && !depkt_any_w;
  //! stream index being dispatched this idle cycle (drives the prefetch)
  wire [IDXW_C-1:0] disp_s_w = pdisp_new_w ? midx_w : pq_r[0].s;

  // ======================================================================
  //  Verdict combinationals (valid in M_PDEC_S; MON_STATE = ram_q_r)
  // ======================================================================
  function automatic [7:0]  ms_prev(input [31:0] w);   ms_prev   = w[7:0];   endfunction
  function automatic [3:0]  ms_settle(input [31:0] w); ms_settle = w[11:8];  endfunction
  function automatic        ms_locked(input [31:0] w); ms_locked = w[12];    endfunction

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

  //! new MON_STATE after an ACCEPTED PDU (mirror of the flat-monitor rules)
  logic [31:0] monst_next_w;
  always_comb begin : monst_calc
    monst_next_w        = ram_q_r;
    monst_next_w[21:14] = p_chans_w;                  // wire_chans
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
    for (int k = 9; k >= 0; k--)
      if (inc_list_r[k]) inc_next_w = 4'(k);
  end : inc_pick

  //! increment amount (MEDIA_RESET drains its latched count; others +1)
  wire [31:0] inc_amt_w = (inc_next_w == C_MR_C) ? 32'(mr_add_r) : 32'd1;

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
          eng_wdata_w = ram_q_r + inc_amt_w;
        end
      end
      M_BDEC_S : begin
        unique case (wrph_r)
          4'd0 : begin
            eng_we_w    = 1'b1;
            eng_waddr_w = laddr(ev_s_r, W_MONST_C);
            //! preserve prev_seq + wire_chans; clear lock/settle (flat-
            //! monitor bind semantics)
            eng_wdata_w = {ram_q_r[31:14], 2'b00, 4'd0, ram_q_r[7:0]};
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

  always_ff @(posedge clk_i) begin : ctx_walker
    if (!rst_n) begin
      mst_r       <= M_IDLE_S;
      pq_cnt_r    <= '0;
      pq_r[0]     <= '0;
      pq_r[1]     <= '0;
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
      mr_add_r    <= '0;
      bind_pend_r  <= '0;
      sil_pend_r   <= '0;
      servo_pend_r <= '0;
      locked_sh_r  <= '0;
      for (int s = 0; s < N_LISTENERS_P; s++) begin
        chans_sh_r[s]    <= '0;
        sil_ms_r[s]      <= '0;
        mreset_pend_r[s] <= '0;
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
      if (media_reset_p_i && bound_i[rsel_w] && !(&mreset_pend_r[rsel_w]))
        mreset_pend_r[rsel_w] <= mreset_pend_r[rsel_w] + 2'd1;
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
          else if (mreset_any_w) begin
            for (int s = N_LISTENERS_P-1; s >= 0; s--)
              if (mreset_pend_r[s] != '0) begin
                ev_s_r   <= IDXW_C'(s);
                mr_add_r <= mreset_pend_r[s];
              end
            inc_list_r <= 10'b1 << C_MR_C;
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
            //! counts nothing else (reference early-return)
            inc_list_r <= 10'b1 << C_UF_C;
            if (ev_s_r == '0) dirty_p_o <= 1'b1;
            mst_r <= M_INC_S;
          end
          else begin
            pdu_accept_p_o     <= 1'b1;
            pdu_accept_idx_o   <= 4'(ev_s_r);
            chans_sh_r[ev_s_r] <= p_chans_w;
            sil_ms_r[ev_s_r]   <= '0;
            if (lock_now_w) locked_sh_r[ev_s_r] <= 1'b1;
            if (ev_s_r == '0) dirty_p_o <= 1'b1;
            monst_r <= monst_next_w;
            inc_list_r <=
                (10'b1 << C_FRX_C)
              | (cur_r.tu    ? (10'b1 << C_TU_C) : 10'b0)
              | (cur_r.late  ? (10'b1 << C_LT_C) : 10'b0)
              | (cur_r.early ? (10'b1 << C_ET_C) : 10'b0)
              | (lock_now_w  ? (10'b1 << C_ML_C) : 10'b0)
              | (seq_mm_w    ? (10'b1 << C_SM_C) : 10'b0)
              | ((seq_mm_w && lost_w >= 8'(INTERRUPT_MIN_LOST_C))
                             ? (10'b1 << C_SI_C) : 10'b0);
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
            if (!inc_rd_q_r) inc_rd_q_r <= 1'b1;
            else begin
              if (inc_next_w == C_MR_C)
                mreset_pend_r[ev_s_r] <= mreset_pend_r[ev_s_r] - mr_add_r
                  + ((media_reset_p_i && bound_i[rsel_w] &&
                      32'(rsel_w) == 32'(ev_s_r)) ? 2'd1 : 2'd0);
              inc_list_r[inc_next_w] <= 1'b0;
              inc_rd_q_r <= 1'b0;
            end
          end
        end

        M_BRD_S : mst_r <= M_BDEC_S;

        M_BDEC_S : begin
          if (wrph_r == 4'd0) begin
            locked_sh_r[ev_s_r] <= 1'b0;
            sil_ms_r[ev_s_r]    <= '0;
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
          lctx_rd_data_o  <= ram_q_r;
          lctx_rd_valid_o <= 1'b1;
          mst_r <= M_IDLE_S;
        end

        default : mst_r <= M_IDLE_S;
      endcase

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
