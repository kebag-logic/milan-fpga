/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_tdm_render.sv
  Author      : Kebag Logic

  Date        : 2026-07-23
  Description : TDM slave audio-render front-end - the OUTPUT-side symmetric
                twin of KL_tdm_capture (item-4 audio-interface family;
                docs/NXN_ARCHITECTURE.md §2.1 "physical interface x1"). The
                mapping fabric writes SLOTS_P per-slot 24-bit samples into a
                slot bank on clk_i; a whole-frame double-buffer crosses into
                the external TDM bit-clock domain, where the module serializes
                an SLOTS_P-slot TDM frame (MSB first, 24-in-SLOT_BITS_P
                left-justified, low bits pad zero) onto tdm_dout_o.

                SYMMETRY WITH KL_tdm_capture (the contract twin):
                  * we are the bus SLAVE, exactly like the capture:
                    tdm_bclk_i / tdm_fsync_i are INPUTS driven by the
                    codec/DSP master; the capture SAMPLES tdm_data_i on the
                    rising edge, so this render (the data driver) SHIFTS on
                    the FALLING edge - standard TDM ("the master shifts on
                    the falling edge"). A KL_tdm_capture wired to this
                    render's tdm_dout_o recovers the exact slot samples.
                  * frame sync: only the 0->1 transition is meaningful, so
                    BOTH shapes work unchanged - the one-bclk PULSE
                    (TI/McASP) and the 50%-duty long frame clock. A level is
                    never trusted as an edge: detection arms only after
                    fsync has been sampled LOW once out of reset (the same
                    "never fake a mid-frame rise" rule as the capture).
                  * every fsync start realigns the slot/bit counters; between
                    fsyncs the counters free-run at the exact frame length
                    (SLOTS_P * SLOT_BITS_P bclk).
                  * data-to-fsync alignment matches the capture's DEFAULT
                    DATA_DELAY_P=1 (Philips-heritage): slot-0 MSB rides the
                    bclk period FOLLOWING the fsync-high edge. The one-bclk
                    Philips delay is produced HERE, ONCE, by the
                    compute-on-rising / present-on-falling output register -
                    never doubled in a TB chip model (78bbabe history).

                CLOCK-DOMAIN DISCIPLINE (mirrored from KL_tdm_capture):
                  * the slot bank crosses clk_i -> tdm_bclk_i through the SAME
                    gray-pointer cdc_pair_fifo the capture uses for its pair
                    stream (there: bclk -> clk_i). No new CDC idiom is
                    invented. The payload is one packed frame
                    (SLOTS_P * 24 bits); the bclk read side keeps an
                    active/next DOUBLE-BUFFER so slot-0 MSB is always ready on
                    the fsync edge and mid-frame producer updates never tear.
                  * an empty FIFO at a frame start is an underrun: the last
                    frame is repeated (slip-dup) and counted, the same
                    repeat-last discipline as KL_i2s_playback's DAC underrun.

                PRODUCER INTERFACE (why slot-indexed writes, not a flat bank):
                  KL_tdm_capture's datapath contract is a slot-indexed
                  valid-PULSE stream (pair_valid_o + pair_slot_o + data). The
                  render's producer interface is the symmetric INVERSE: a
                  slot-indexed valid-pulse WRITE (smp_wr_en_i + smp_wr_slot_i
                  + smp_wr_data_i) into the bank, committed as a frame by a
                  one-cycle tick_i. This mirrors the capture's pulse-indexed
                  geometry and is the natural fit for the mapping fabric,
                  which routes one channel onto one slot at a time.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! TDM slave serializer (item-4 front-end family, OUTPUT side): a clk_i slot
//! bank -> packed-frame gray-pointer CDC -> active/next double-buffer ->
//! MSB-first 24-in-SLOT_BITS_P TDM frame on tdm_dout_o. Pulse and 50%-duty
//! fsyncs (edge-armed), Philips-heritage slot-0 alignment, slot 0 first.

`default_nettype none

module KL_tdm_render #(
  parameter int unsigned SLOTS_P     = 8,   //! TDM slots per frame (8/16/32)
  parameter int unsigned SLOT_BITS_P = 32,  //! bit clocks per slot (16/24/32)
  parameter int unsigned FIFO_LOG2_P = 2    //! frame CDC depth = 2^N (>=2 for
                                            //! the active/next double-buffer)
)(
  input  wire         clk_i,             //! datapath clock (producer domain)
  input  wire         rst_n,             //! active-low synchronous reset (clk_i)

  // ---- producer side (clk_i domain; slot-indexed writes) ---------------
  input  wire         smp_wr_en_i,       //! one-cycle per-slot write strobe
  input  wire [$clog2(SLOTS_P)-1:0] smp_wr_slot_i, //! target slot index
  input  wire [23:0]  smp_wr_data_i,     //! 24-bit sample (MSB-justified)
  input  wire         tick_i,            //! one-cycle frame commit: latch the
                                         //! bank as written up to the prior
                                         //! cycle into the CDC toward the bus

  // ---- TDM bus (we are slave; master drives bclk/fsync) ----------------
  input  wire         tdm_bclk_i,        //! bit clock (serializer domain)
  input  wire         tdm_fsync_i,       //! frame sync (pulse or 50% duty)
  output logic        tdm_dout_o,        //! serial data out, MSB first (driven
                                         //! on the falling bclk edge)

  // ---- status (Linux-observable via CSR; plain clk_i counters) ---------
  output wire  [15:0] frames_o,          //! frames serialized onto the bus
  output wire  [15:0] underruns_o,       //! frame starts with no fresh frame
                                         //! (last frame repeated)
  output wire  [15:0] overruns_o         //! tick_i frames dropped (CDC full)
);

  localparam int unsigned SW = $clog2(SLOTS_P);      //! slot-index width
  localparam int unsigned BW = $clog2(SLOT_BITS_P);  //! bit-index width
  localparam int unsigned DBITS =
      (SLOT_BITS_P < 24) ? SLOT_BITS_P : 24;         //! data bits per slot
  localparam int unsigned FRAME_BITS = SLOTS_P * 24; //! packed frame width

  // ======================================================================
  //  clk_i domain: slot bank + frame commit into the gray-pointer CDC
  // ======================================================================
  logic [23:0]            bank_r [SLOTS_P];  //! per-slot sample bank
  logic [15:0]            overruns_r;
  wire  [FRAME_BITS-1:0]  bank_flat_w;
  wire                    wfull_w;

  genvar gs;
  generate
    for (gs = 0; gs < SLOTS_P; gs++) begin : g_pack
      assign bank_flat_w[gs*24 +: 24] = bank_r[gs];
    end
  endgenerate

  //! FIFO write is combinational off tick_i (the FIFO registers internally
  //! and self-guards on !wfull); bank_flat_w reflects writes up to the prior
  //! cycle - the fabric pulses tick_i after its slot writes have landed.
  wire fifo_wen_w = tick_i && !wfull_w;

  always_ff @(posedge clk_i) begin : producer
    if (!rst_n) begin
      overruns_r <= '0;
      for (int i = 0; i < SLOTS_P; i++) bank_r[i] <= '0;
    end else begin
      if (smp_wr_en_i) bank_r[smp_wr_slot_i] <= smp_wr_data_i;
      //! a commit that finds the CDC full drops the frame (consumer behind)
      if (tick_i && wfull_w)
        overruns_r <= (&overruns_r) ? overruns_r : overruns_r + 16'd1;
    end
  end : producer

  // ======================================================================
  //  clk_i -> tdm_bclk_i frame crossing (the KL_tdm_capture CDC idiom,
  //  gray-pointer dual-clock cdc_pair_fifo, reversed direction)
  // ======================================================================
  logic [1:0]            brst_n_r;        //! bclk-domain reset sync (2FF)
  wire  [FRAME_BITS-1:0] rdata_w;
  wire                   rempty_w;
  logic                  ren_r;

  always_ff @(posedge tdm_bclk_i) begin : t_bclk_rst
    brst_n_r <= {brst_n_r[0], rst_n};
  end : t_bclk_rst

  cdc_pair_fifo #(.WIDTH(FRAME_BITS), .LOG2D(FIFO_LOG2_P)) u_fcdc (
    .wclk_i  (clk_i),
    .wrst_n  (rst_n),
    .wen_i   (fifo_wen_w),
    .wdata_i (bank_flat_w),
    .wfull_o (wfull_w),
    .rclk_i  (tdm_bclk_i),
    .rrst_n  (brst_n_r[1]),
    .ren_i   (ren_r),
    .rdata_o (rdata_w),
    .rempty_o(rempty_w)
  );

  // ======================================================================
  //  tdm_bclk_i domain: frame tracking + double-buffer + bit serializer
  // ======================================================================
  logic                   fsync_q_r;   //! fsync at the previous rising edge
  logic                   armed_r;     //! fsync sampled low once (edge valid)
  logic                   run_r;       //! a frame start has been seen
  logic [SW-1:0]          slot_r;
  logic [BW-1:0]          bit_r;
  logic [FRAME_BITS-1:0]  active_r;    //! frame currently serializing
  logic [FRAME_BITS-1:0]  next_r;      //! prefetched frame (double-buffer)
  logic                   have_next_r; //! next_r holds a fresh frame
  logic                   fetch_v_r;   //! rdata_w valid this cycle (post-ren)
  logic                   dout_nxt_r;  //! bit for the next falling edge
  logic [15:0]            frames_b_r;  //! frames serialized (bclk domain)
  logic [15:0]            unders_b_r;  //! underruns (bclk domain)

  //! frame start = ARMED fsync 0->1 on the rising edge (same rule as capture)
  wire                  start_w = tdm_fsync_i && !fsync_q_r && armed_r;
  wire                  sol_w   = start_w;
  //! effective position of THIS edge (a frame start overrides the counters)
  wire [SW-1:0]         eslot_w = sol_w ? '0 : slot_r;
  wire [BW-1:0]         ebit_w  = sol_w ? '0 : bit_r;
  //! at a frame start with a fresh frame, read the incoming frame directly so
  //! slot-0 MSB comes from next_r on the very edge active_r adopts it
  wire                  adopt_w = sol_w && have_next_r;
  wire [FRAME_BITS-1:0] frame_sel_w = adopt_w ? next_r : active_r;
  wire [23:0]           smp_w   = frame_sel_w[24*eslot_w +: 24];
  //! MSB-first, top DBITS bits of the slot are data, the remainder pad zero
  wire [4:0]            didx_w  = 5'd23 - ebit_w[4:0];
  wire                  dbit_w  = (32'(ebit_w) < DBITS) ? smp_w[didx_w] : 1'b0;

  always_ff @(posedge tdm_bclk_i) begin : t_ser
    if (!brst_n_r[1]) begin
      fsync_q_r <= 1'b0; armed_r <= 1'b0; run_r <= 1'b0;
      slot_r <= '0; bit_r <= '0;
      active_r <= '0; next_r <= '0; have_next_r <= 1'b0;
      ren_r <= 1'b0; fetch_v_r <= 1'b0; dout_nxt_r <= 1'b0;
      frames_b_r <= '0; unders_b_r <= '0;
    end else begin
      fsync_q_r <= tdm_fsync_i;
      if (!tdm_fsync_i) armed_r <= 1'b1;

      // ---- prefetch the next frame from the CDC (2-step: ren, then data) --
      ren_r <= 1'b0;
      if (!have_next_r && !ren_r && !fetch_v_r && !rempty_w) ren_r <= 1'b1;
      fetch_v_r <= ren_r;
      if (fetch_v_r) begin
        next_r      <= rdata_w;
        have_next_r <= 1'b1;
      end

      // ---- frame start: adopt the fresh frame, else underrun-repeat -------
      //  (the 256-bclk frame gap vs the 2-bclk prefetch means a fetch and a
      //   frame start never coincide; adopt still uses the pre-edge next_r)
      if (sol_w) begin
        frames_b_r <= frames_b_r + 16'd1;
        if (have_next_r) begin
          active_r    <= next_r;
          have_next_r <= 1'b0;             //! schedule a refill
        end else begin
          unders_b_r  <= unders_b_r + 16'd1;  //! keep active_r (repeat)
        end
      end

      // ---- serialize: advance the free-running counters, latch next bit ---
      if (run_r || sol_w) begin
        run_r      <= 1'b1;
        dout_nxt_r <= dbit_w;
        if (32'(ebit_w) == SLOT_BITS_P - 1) begin
          bit_r  <= '0;
          slot_r <= (32'(eslot_w) == SLOTS_P - 1) ? '0 : eslot_w + 1'b1;
        end else begin
          bit_r  <= ebit_w + 1'b1;
          slot_r <= eslot_w;
        end
      end
    end
  end : t_ser

  //! output register on the FALLING edge: the bit computed on the rising edge
  //! is presented half a bclk later, so it is stable across the receiver's
  //! next rising edge - this IS the one-bclk Philips-heritage delay.
  logic [1:0] nrst_n_r;
  always_ff @(negedge tdm_bclk_i) begin : t_dout
    nrst_n_r <= {nrst_n_r[0], rst_n};
    if (!nrst_n_r[1]) tdm_dout_o <= 1'b0;
    else              tdm_dout_o <= dout_nxt_r;
  end : t_dout

  // ======================================================================
  //  status counters back into clk_i (quasi-static 2-FF, KL_i2s_playback
  //  discipline: the counts are monotonic and read for trends only)
  // ======================================================================
  logic [15:0] fr_m_r, fr_s_r, un_m_r, un_s_r;
  always_ff @(posedge clk_i) begin : t_cnt_sync
    {fr_s_r, fr_m_r} <= {fr_m_r, frames_b_r};
    {un_s_r, un_m_r} <= {un_m_r, unders_b_r};
  end : t_cnt_sync

  assign frames_o    = fr_s_r;
  assign underruns_o = un_s_r;
  assign overruns_o  = overruns_r;

endmodule

`default_nettype wire
