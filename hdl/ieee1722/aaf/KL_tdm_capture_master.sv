/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_tdm_capture_master.sv
  Author      : Kebag Logic

  Date        : 2026-07-28
  Description : TDM MASTER audio-capture front-end (item-4 audio-interface
                family; roadmap item 5 - the framer half). Same
                {slot, L, R} pair-stream contract as KL_aaf_capture_i2s and
                KL_tdm_capture, so milan_datapath swaps it in 1:1 and the
                shared KL_aaf_packetizer needs no change.

                WHY A SEPARATE MODULE AND NOT A `MASTER_P` ON THE SLAVE.
                KL_tdm_capture is a genuine SLAVE: its deserializer runs
                `always_ff @(posedge tdm_bclk_i)` and its CDC writes on that
                same external clock. A master cannot reuse that shape - it
                would have to synthesise a clock in fabric and then drive a
                clock net with it, which needs a BUFG and its own timing
                closure. The house rule (KL_aaf_capture_i2s, 07-18 lineage)
                is the CLEAN-CLOCK discipline: run in the MMCM's clk_audio_i
                and treat the serial clock as a generated SIGNAL with a
                rising-edge ENABLE. That is a different structure, so it is a
                different module - and the proven slave path stays untouched
                and byte-identical.

                WHY IT EXISTS AT ALL (measured, 2026-07-28). The AX7101 has
                `_connectors = []`: no pmoda, so `i2s_pads = None` and
                `i_i2s_sdout_i = 0`. Its capture front-end clocked in a
                constant zero and produced ONE pair of digital silence, so
                the 8x8 talkers advertised 8-channel AAF and put 2 channels
                on the wire. A Milan-validated listener bound to a 2ch sink
                counted UNSUPPORTED_FORMAT 0 over 1,491,239 frames and to an
                8ch sink 296,294 of 296,294 - the framer's width proven in
                BOTH directions. And the slave TDM front-end could not help:
                milan_soc.py ties i_tdm_bclk_i/i_tdm_fsync_i/i_tdm_data_i to
                0 on every SoC in the tree, so its fsync never toggles and it
                yields no pairs at all. A MASTER needs nobody to drive it:
                it makes its own bclk and fsync, which is what turns the TDM
                interface from a declaration into a fabric fact.

                CLOCKING. bclk = SLOTS_P x WORD_BITS_P x fs. At the shipping
                24.576 MHz audio MMCM, TDM8 x 32-bit slots @ 48 kHz needs
                8*32*48000 = 12.288 MHz = clk_audio_i / 2, i.e. a half-period
                of ONE clk_audio_i cycle (BCLK_HALF_P = 1). fsync is a
                one-bclk PULSE at the start of slot 0 (the TI/McASP shape);
                KL_tdm_capture accepts both that and the 50%-duty long frame,
                so a board that loops our own master back into the slave
                interoperates.

                DATA. We drive bclk and fsync and SAMPLE tdm_data_i on the
                bclk RISING edge, the same convention the slave uses, so a
                codec shifting on the falling edge meets setup. DATA_DELAY_P
                keeps the same meaning (0 = slot-0 MSB on the fsync edge,
                1 = one bclk later / Philips-heritage) and is applied HERE,
                ONCE - never also in a TB chip model (the double-Philips-delay
                history, 78bbabe).

                CHANNEL MAP. Pair k carries TDM slots {2k, 2k+1}, so a
                C-channel stream consumes C/2 consecutive pair slots exactly
                as the packetizer's TCTX chans prefix-sum expects. Slots 0/1
                are the FIRST pair - USER 2026-07-28: channels 1/2 stay the
                I2S Pmod, so a board mixing the two feeds this module's slots
                0/1 from that Pmod and the rest from the TDM header.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! TDM MASTER deserializer (item-4 front-end family): generates bclk/fsync
//! from clk_audio_i and emits the {pair_slot, L, R} stream in clk_i via the
//! gray-pointer pair CDC. Clean-clock discipline: no generated clock net.

`default_nettype none

module KL_tdm_capture_master #(
  parameter int unsigned SLOTS_P      = 8,    //! TDM slots per frame (8/16/32)
  parameter int unsigned WORD_BITS_P  = 32,   //! bit clocks per slot (16/24/32)
  //! clk_audio_i cycles per bclk HALF period. bclk = clk_audio_i/(2*this).
  //! 24.576 MHz / 2 = 12.288 MHz = TDM8 x 32 bits x 48 kHz, so 1 is the
  //! shipping value. Never 0 - that would ask for a clock, not a divider.
  parameter int unsigned BCLK_HALF_P  = 1,
  parameter bit          DATA_DELAY_P = 1'b1  //! fsync->MSB offset (0 = DSP A,
                                              //! 1 = DSP B / Philips-heritage)
)(
  input  wire         clk_i,             //! datapath clock
  input  wire         rst_n,             //! active-low synchronous reset
  input  wire         clk_audio_i,       //! clean MMCM audio clock (24.576 MHz)

  // ---- TDM bus (we are MASTER: bclk/fsync are OUTPUTS) -----------------
  output wire         tdm_mclk_o,        //! clk_audio_i/2 codec master clock
  output wire         tdm_bclk_o,        //! generated bit clock
  output wire         tdm_fsync_o,       //! generated frame sync (1-bclk pulse)
  input  wire         tdm_data_i,        //! serial data, MSB first

  // ---- pair stream out (clk_i domain; one pulse per slot pair) ---------
  output logic        pair_valid_o,      //! one-cycle pulse per pair
  output logic [3:0]  pair_slot_o,       //! pair index (TDM slots {2k,2k+1})
  output logic [23:0] pair_l_o,
  output logic [23:0] pair_r_o,

  // ---- status (firmware-visible via CSR) ------------------------------
  output reg  [31:0]  pairs_captured_o   //! pairs captured (liveness)
);

  localparam int unsigned BW_C     = $clog2(WORD_BITS_P);
  localparam int unsigned SW_C     = $clog2(SLOTS_P);
  localparam int unsigned FRAME_C  = SLOTS_P * WORD_BITS_P;   //! bclks/frame

  //! A divider of 0 is not a slow clock, it is no clock - and it would make
  //! the phase counter compare against a value it can never hold, so the
  //! front-end would sit silent exactly like the tied-off slave bus this
  //! module exists to replace. Fail the build instead.
  if (BCLK_HALF_P < 1) begin : g_bclk_div_guard
    $error("KL_tdm_capture_master: BCLK_HALF_P=%0d must be >= 1 (clk_audio_i cycles per bclk half period; bclk = SLOTS_P*WORD_BITS_P*sample_rate).",
           BCLK_HALF_P);
  end : g_bclk_div_guard

  // ======================================================================
  //  clk_audio_i domain: bclk/fsync generation + slot deserializer
  //
  //  CLEAN-CLOCK DISCIPLINE: bclk is a SIGNAL, never a clock net. Every
  //  flop here is clocked by clk_audio_i and gated by the bclk rising-edge
  //  enable, which is what KL_aaf_capture_i2s does for sclk/lrck.
  // ======================================================================
  logic [1:0] arst_n_r;                 //! audio-domain reset sync
  always_ff @(posedge clk_audio_i) arst_n_r <= {arst_n_r[0], rst_n};
  wire arst_n_w = arst_n_r[1];

  //! convenience MCLK: clk_audio_i/2, same as the slave's
  logic mdiv_r;
  always_ff @(posedge clk_audio_i) begin : t_mclk_div
    if (!arst_n_w) mdiv_r <= 1'b0;
    else           mdiv_r <= !mdiv_r;
  end : t_mclk_div
  assign tdm_mclk_o = mdiv_r;

  //! bclk generation: toggle every BCLK_HALF_P cycles of clk_audio_i
  localparam int unsigned PHW_C = (BCLK_HALF_P <= 1) ? 1 : $clog2(BCLK_HALF_P);
  logic [PHW_C-1:0] phase_r;
  logic             bclk_r;
  wire              tick_w  = (32'(phase_r) == BCLK_HALF_P - 1);
  //! the enable that REPLACES `posedge tdm_bclk_i`: the cycle on which bclk
  //! goes 0 -> 1. Everything the slave does on its clock edge, we do here.
  wire              brise_w = tick_w && !bclk_r;

  always_ff @(posedge clk_audio_i) begin : t_bclk_gen
    if (!arst_n_w) begin
      phase_r <= '0;
      bclk_r  <= 1'b0;
    end else if (tick_w) begin
      phase_r <= '0;
      bclk_r  <= !bclk_r;
    end else begin
      phase_r <= phase_r + 1'b1;
    end
  end : t_bclk_gen
  assign tdm_bclk_o = bclk_r;

  //! frame position, advanced once per bclk RISE. fsync is asserted for the
  //! whole of bclk 0 of the frame (a one-bclk pulse), which KL_tdm_capture
  //! and every McASP-style slave read as the frame start.
  logic [$clog2(FRAME_C)-1:0] fpos_r;
  logic                       fsync_r;
  always_ff @(posedge clk_audio_i) begin : t_frame
    if (!arst_n_w) begin
      fpos_r  <= '0;
      fsync_r <= 1'b1;          //! first bclk of the first frame IS slot 0
    end else if (brise_w) begin
      fpos_r  <= (32'(fpos_r) == FRAME_C - 1) ? '0 : fpos_r + 1'b1;
      fsync_r <= (32'(fpos_r) == FRAME_C - 1);
    end
  end : t_frame
  assign tdm_fsync_o = fsync_r;

  // ======================================================================
  //  Deserializer - the slave's state machine, driven by brise_w instead of
  //  by a clock edge. We KNOW where the frame starts (we made it), so there
  //  is no arming/edge-detect dance: sol_w is a position compare.
  // ======================================================================
  logic                   startp_r;     //! DATA_DELAY_P=1: MSB on next rise
  logic [BW_C-1:0]        bit_r;
  logic [SW_C-1:0]        slot_r;
  //! WORD_BITS_P-1 wide, not WORD_BITS_P: the MSB is shifted out into
  //! word_w the same cycle it would be written, so a full-width register
  //! carries one bit nothing ever reads.
  logic [WORD_BITS_P-2:0] shift_r;
  logic [23:0]            lhold_r;
  logic                   cap_wen_r;
  logic [3:0]             cap_slot_r;
  logic [23:0]            cap_l_r, cap_r_r;
  wire                    cap_full_w;

  wire start_w = (32'(fpos_r) == 0);            //! this rise carries slot 0
  wire sol_w   = DATA_DELAY_P ? startp_r : start_w;

  wire [SW_C-1:0] eslot_w = sol_w ? '0 : slot_r;
  wire [BW_C-1:0] ebit_w  = sol_w ? '0 : bit_r;
  wire [WORD_BITS_P-1:0] word_w = {shift_r, tdm_data_i};
  wire [WORD_BITS_P+23:0] wext_w = {word_w, 24'b0};
  wire [23:0]             smp_w  = 24'(wext_w >> WORD_BITS_P);

  always_ff @(posedge clk_audio_i) begin : t_deser
    if (!arst_n_w) begin
      startp_r <= 1'b0;
      bit_r <= '0; slot_r <= '0; shift_r <= '0; lhold_r <= '0;
      cap_wen_r <= 1'b0; cap_slot_r <= '0; cap_l_r <= '0; cap_r_r <= '0;
    end else begin
      cap_wen_r <= 1'b0;                //! one clk_audio_i-wide write pulse
      if (brise_w) begin
        startp_r <= start_w;
        shift_r  <= {shift_r[WORD_BITS_P-3:0], tdm_data_i};
        if (32'(ebit_w) == WORD_BITS_P - 1) begin
          //! slot complete: even holds L, odd pushes the pair
          if (!eslot_w[0]) lhold_r <= smp_w;
          else begin
            cap_slot_r <= 4'(eslot_w >> 1);
            cap_l_r    <= lhold_r;
            cap_r_r    <= smp_w;
            cap_wen_r  <= !cap_full_w;
          end
          bit_r  <= '0;
          slot_r <= (32'(eslot_w) == SLOTS_P - 1) ? '0 : eslot_w + 1'b1;
        end else begin
          bit_r  <= ebit_w + 1'b1;
          slot_r <= eslot_w;
        end
      end
    end
  end : t_deser

  // ======================================================================
  //  pairs into the datapath clock domain (gray-pointer CDC) - the write
  //  side is clk_audio_i here, not an external bclk, because that is the
  //  domain the deserializer actually runs in.
  // ======================================================================
  wire        cap_rempty_w;
  wire [51:0] cap_pair_w;
  logic       cap_ren_r;
  cdc_pair_fifo #(.WIDTH(52), .LOG2D(3)) u_tcdc (
    .wclk_i  (clk_audio_i),
    .wrst_n  (arst_n_w),
    .wen_i   (cap_wen_r),
    .wdata_i ({cap_slot_r, cap_l_r, cap_r_r}),
    .wfull_o (cap_full_w),
    .rclk_i  (clk_i),
    .rrst_n  (rst_n),
    .ren_i   (cap_ren_r),
    .rdata_o (cap_pair_w),
    .rempty_o(cap_rempty_w)
  );

  //! clk_i side: IDENTICAL to KL_tdm_capture's proven pop - the FIFO
  //! registers rdata_o ON the ren edge, so the pop cycle's data is live
  //! during the following pair_valid cycle and the outputs alias rdata_o
  //! directly (it holds until the next ren). Copied rather than reinvented:
  //! the pair contract is what the packetizer depends on.
  always_ff @(posedge clk_i) begin : t_pop
    if (!rst_n) begin
      pair_valid_o <= 1'b0; cap_ren_r <= 1'b0;
      pairs_captured_o <= '0;
    end else begin
      pair_valid_o <= cap_ren_r;
      cap_ren_r <= !cap_rempty_w && !cap_ren_r && !pair_valid_o;
      if (pair_valid_o) pairs_captured_o <= pairs_captured_o + 1'b1;
    end
  end : t_pop

  always_comb begin : t_pair_out
    pair_slot_o = cap_pair_w[51:48];
    pair_l_o    = cap_pair_w[47:24];
    pair_r_o    = cap_pair_w[23:0];
  end : t_pair_out

endmodule

`default_nettype wire
