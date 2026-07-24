/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_chan_map_capture.sv
  Author      : Kebag Logic

  Date        : 2026-07-23
  Description : Per-pair-slot TX source multiplexer (docs/NXN_ARCHITECTURE.md
                §2.1 capture family; the SW-defined end-station channel map).
                Sits between the several pair-stream sources and the shared
                KL_aaf_packetizer's pair-injection interface: for every one of
                the N_SLOTS_P TX pair slots (the prefix-sum slot space; talker
                t owns chans/2 consecutive slots - see the packetizer header)
                a small map RAM selects which audio source feeds that slot.

                8 talker streams x up to 8 channels = up to 32 stereo PAIR
                slots, so the map is 32 entries deep and the emitted
                pair_slot_o is the full 5-bit (0..31) space the packetizer now
                accepts (the pair_slot widening).

                MAP ENTRY (8 bits, one per slot): {en[7], src[6:4], idx[3:0]}
                  en  - 1 = this slot is live and injected every media tick;
                        0 = the slot emits nothing (skipped in the walk).
                  src - the source bucket:
                          0 ZERO    : digital silence (L=R=0)
                          1 I2S_IN  : the stereo I2S capture pair (idx unused)
                          2 TDM_IN  : TDM pair idx (0..N_TDM_P/2-1; slot pair
                                      idx carries TDM slots {2*idx, 2*idx+1})
                          3 RING    : ALSA playback ring pair idx (the
                                      KL_pcm_tx pair-channel index)
                          4 TONE    : the pilot tone on BOTH channels
                        (5..7 reserved -> silence)
                  idx - the within-source pair index (see src).

                SOURCE BUCKETS (wire-truth, free-running): the latest pair per
                source is latched into a hold register the instant its
                pair_valid pulse arrives, so the tick-time walk always injects
                the freshest sample. The tone bucket is the live tone_smp_i
                (both L/R). No CDC lives here - every source has already
                crossed into clk_i.

                EMIT (media sample tick): on tick_i the engine walks the slot
                map low-to-high; each ENABLED slot injects one pair
                (pair_valid_o one-cycle pulse + pair_slot_o + pair_l_o/
                pair_r_o) then idles GAP_CYC_P cycles before the next slot -
                the proven inject cadence the packetizer admits (one pair per
                cycle with a settle gap, mirroring the golden NxN TB's
                pair()). Disabled slots are skipped with no pulse. Six media
                ticks (6 samples/ch) fill one AVTPDU per talker on the shared
                6-sample cadence; a tick arriving mid-walk is queued one deep
                (never dropped).

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! Per-pair-slot TX source mux (NXN §2.1 capture family): a 32-slot map RAM
//! ({en, src, idx}) routes each packetizer pair slot to a source bucket (I2S
//! capture / TDM / ALSA ring / tone / silence); free-running source holds,
//! per-tick low-to-high slot walk emitting the packetizer inject cadence
//! (one pulse + GAP_CYC_P settle), disabled slots silent. Single clock, no CDC.

`default_nettype none

module KL_chan_map_capture #(
  parameter int unsigned N_SLOTS_P = 32,   //! TX pair slots (prefix-sum space)
  parameter int unsigned N_TDM_P   = 8,    //! TDM slots (pairs = N_TDM_P/2)
  parameter int unsigned N_RING_P  = 16,   //! ALSA ring pair sources (idx 0..15)
  parameter int unsigned GAP_CYC_P = 24    //! settle cycles between slot injects
)(
  input  wire         clk_i,             //! datapath clock
  input  wire         rst_n,             //! active-low synchronous reset

  //! --- map RAM write port (CSR window / TB) ------------------------------
  input  wire         map_wr_en_i,       //! one-cycle write strobe
  input  wire [$clog2(N_SLOTS_P)-1:0] map_wr_addr_i, //! slot index
  input  wire [7:0]   map_wr_data_i,     //! {en[7], src[6:4], idx[3:0]}

  //! --- map RAM readback port (registered, 1-cycle latency) ---------------
  input  wire         map_rd_en_i,       //! one-cycle read request
  input  wire [$clog2(N_SLOTS_P)-1:0] map_rd_addr_i,
  output logic [7:0]  map_rd_data_o,     //! map entry (valid with rd_valid)
  output logic        map_rd_valid_o,    //! read data valid this cycle

  //! --- I2S capture pair source (single stereo pair) ----------------------
  input  wire         i2s_pair_valid_i,  //! latch pulse
  input  wire [23:0]  i2s_l_i,
  input  wire [23:0]  i2s_r_i,

  //! --- TDM capture pair sources (indexed by pair slot) -------------------
  input  wire         tdm_pair_valid_i,  //! latch pulse
  input  wire [3:0]   tdm_pair_slot_i,   //! TDM pair index (0..N_TDM_P/2-1)
  input  wire [23:0]  tdm_l_i,
  input  wire [23:0]  tdm_r_i,

  //! --- ALSA ring pair sources (KL_pcm_tx output, indexed by pair slot) ---
  input  wire         ring_pair_valid_i, //! latch pulse
  input  wire [3:0]   ring_pair_slot_i,  //! ring pair-channel index (0..N-1)
  input  wire [23:0]  ring_l_i,
  input  wire [23:0]  ring_r_i,

  //! --- tone generator sample (live; drives both L/R when TONE) -----------
  input  wire [23:0]  tone_smp_i,

  //! --- media sample tick (one walk of the enabled slots per pulse) -------
  input  wire         tick_i,

  //! --- pair injection to the shared packetizer (its capture contract) ----
  output logic        pair_valid_o,      //! one-cycle pulse per L/R pair
  output logic [4:0]  pair_slot_o,       //! pair slot 0..31 (widened space)
  output logic [23:0] pair_l_o,
  output logic [23:0] pair_r_o
);

  // ---------------------------------------------------------------------- //
  // Derived sizing                                                          //
  // ---------------------------------------------------------------------- //
  localparam int unsigned SLOTW_C      = $clog2(N_SLOTS_P);
  localparam int unsigned N_TDM_PAIRS_C = (N_TDM_P < 2) ? 1 : N_TDM_P / 2;
  localparam int unsigned TDMPW_C      = (N_TDM_PAIRS_C <= 1) ? 1
                                                      : $clog2(N_TDM_PAIRS_C);
  localparam int unsigned RINGPW_C     = (N_RING_P <= 1) ? 1
                                                      : $clog2(N_RING_P);

  //! map entry field encoding (src[6:4])
  localparam logic [2:0] SRC_ZERO_C = 3'd0, SRC_I2S_C = 3'd1, SRC_TDM_C = 3'd2,
                         SRC_RING_C = 3'd3, SRC_TONE_C = 3'd4;

  // ---------------------------------------------------------------------- //
  // Map RAM (small config store: flop register file, like KL_pcm_route)     //
  //   one sync write process; combinational reads for the walk; the         //
  //   readback port registers a snapshot (RAM house style read turnaround)  //
  // ---------------------------------------------------------------------- //
  logic [7:0] map_r [N_SLOTS_P];

  always_ff @(posedge clk_i) begin : map_write_port
    if (!rst_n) begin
      for (int s = 0; s < N_SLOTS_P; s++) map_r[s] <= 8'h00;
    end
    else if (map_wr_en_i) begin
      map_r[map_wr_addr_i] <= map_wr_data_i;
    end
  end : map_write_port

  always_ff @(posedge clk_i) begin : map_read_port
    if (!rst_n) begin
      map_rd_data_o  <= 8'h00;
      map_rd_valid_o <= 1'b0;
    end
    else begin
      map_rd_valid_o <= 1'b0;
      if (map_rd_en_i) begin
        map_rd_data_o  <= map_r[map_rd_addr_i];
        map_rd_valid_o <= 1'b1;
      end
    end
  end : map_read_port

  // ---------------------------------------------------------------------- //
  // Source hold buckets (latch the latest pair per source; wire-truth)      //
  // ---------------------------------------------------------------------- //
  logic [47:0] i2s_hold_r;               //! the single stereo I2S pair
  logic [47:0] tdm_hold_r  [N_TDM_PAIRS_C];
  logic [47:0] ring_hold_r [N_RING_P];

  always_ff @(posedge clk_i) begin : source_latch
    if (!rst_n) begin
      i2s_hold_r <= '0;
      for (int t = 0; t < N_TDM_PAIRS_C; t++) tdm_hold_r[t]  <= '0;
      for (int r = 0; r < N_RING_P;      r++) ring_hold_r[r] <= '0;
    end
    else begin
      if (i2s_pair_valid_i) i2s_hold_r <= {i2s_l_i, i2s_r_i};
      if (tdm_pair_valid_i && (32'(tdm_pair_slot_i) < N_TDM_PAIRS_C))
        tdm_hold_r[tdm_pair_slot_i[TDMPW_C-1:0]] <= {tdm_l_i, tdm_r_i};
      if (ring_pair_valid_i && (32'(ring_pair_slot_i) < N_RING_P))
        ring_hold_r[ring_pair_slot_i[RINGPW_C-1:0]] <= {ring_l_i, ring_r_i};
    end
  end : source_latch

  // ---------------------------------------------------------------------- //
  // Source select for the current walk slot (combinational)                 //
  // ---------------------------------------------------------------------- //
  logic [SLOTW_C-1:0] slot_r;            //! walk pointer

  wire [7:0] ent_w = map_r[slot_r];
  wire       en_w  = ent_w[7];
  wire [2:0] src_w = ent_w[6:4];
  wire [3:0] idx_w = ent_w[3:0];

  logic [23:0] sel_l_w, sel_r_w;
  always_comb begin : source_mux
    unique case (src_w)
      SRC_I2S_C : {sel_l_w, sel_r_w} = i2s_hold_r;
      SRC_TDM_C : {sel_l_w, sel_r_w} =
                    (32'(idx_w) < N_TDM_PAIRS_C)
                      ? tdm_hold_r[idx_w[TDMPW_C-1:0]] : 48'd0;
      SRC_RING_C : {sel_l_w, sel_r_w} =
                    (32'(idx_w) < N_RING_P)
                      ? ring_hold_r[idx_w[RINGPW_C-1:0]] : 48'd0;
      SRC_TONE_C : {sel_l_w, sel_r_w} = {tone_smp_i, tone_smp_i};
      default    : {sel_l_w, sel_r_w} = 48'd0;   //! ZERO + reserved = silence
    endcase
  end : source_mux

  // ---------------------------------------------------------------------- //
  // Emit walk FSM                                                           //
  // ---------------------------------------------------------------------- //
  typedef enum logic [1:0] {
    CM_IDLE_S,     //! wait for a media tick
    CM_STEP_S,     //! decide the current slot: skip / emit
    CM_GAP_S       //! settle gap after a pair pulse
  } cstate_t;

  cstate_t                    st_r;
  logic                       tick_pend_r;   //! one-deep tick queue
  logic [$clog2(GAP_CYC_P+1)-1:0] gap_r;
  wire  last_slot_w = (32'(slot_r) == N_SLOTS_P - 1);

  always_ff @(posedge clk_i) begin : emit_engine
    if (!rst_n) begin
      st_r         <= CM_IDLE_S;
      tick_pend_r  <= 1'b0;
      slot_r       <= '0;
      gap_r        <= '0;
      pair_valid_o <= 1'b0;
      pair_slot_o  <= '0;
      pair_l_o     <= '0;
      pair_r_o     <= '0;
    end
    else begin
      unique case (st_r)
        // -------- wait for the media tick --------------------------------
        CM_IDLE_S : begin
          pair_valid_o <= 1'b0;
          if (tick_pend_r) begin
            tick_pend_r <= 1'b0;           //! a coincident tick re-arms below
            slot_r      <= '0;
            st_r        <= CM_STEP_S;
          end
        end

        // -------- decide the current slot --------------------------------
        CM_STEP_S : begin
          if (en_w) begin
            //! inject one pair for this enabled slot (1-cycle pulse next)
            pair_valid_o <= 1'b1;
            pair_slot_o  <= 5'(slot_r);
            pair_l_o     <= sel_l_w;
            pair_r_o     <= sel_r_w;
            gap_r        <= ($clog2(GAP_CYC_P+1))'(GAP_CYC_P);
            st_r         <= CM_GAP_S;
          end
          else begin
            //! disabled slot: emit nothing, advance immediately
            pair_valid_o <= 1'b0;
            if (last_slot_w) st_r <= CM_IDLE_S;
            else             slot_r <= slot_r + 1'b1;
          end
        end

        // -------- settle gap between injects ------------------------------
        CM_GAP_S : begin
          pair_valid_o <= 1'b0;            //! the pulse was one cycle only
          if (gap_r == '0) begin
            if (last_slot_w) st_r <= CM_IDLE_S;
            else begin
              slot_r <= slot_r + 1'b1;
              st_r   <= CM_STEP_S;
            end
          end
          else gap_r <= gap_r - 1'b1;
        end

        default : st_r <= CM_IDLE_S;
      endcase

      //! media-tick capture (after the case: a tick coincident with an
      //! IDLE consume re-arms the one-deep queue instead of being dropped)
      if (tick_i) tick_pend_r <= 1'b1;
    end
  end : emit_engine

endmodule

`default_nettype wire
