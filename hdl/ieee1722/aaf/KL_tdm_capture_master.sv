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

                FSYNC LAUNCHES ON THE BCLK FALL (2026-09-17, issue #452).
                fsync used to be registered on brise_w, the same clk_audio_i
                edge on which the bclk pin goes 0 -> 1, so at the PINS it
                changed together with the receiver's sampling edge: zero
                nominal setup and zero hold, and which rise a receiver
                attributed the pulse to was decided by the sign of an
                unconstrained pin skew rather than by a margin. It is now
                registered on the bclk FALL - the edge tdm_dout_o already
                launches on (KL_tdm_render_master, "latch on the rise, launch
                on the fall") - so the pulse is CENTRED on the rise that
                carries it: fsync goes high half a bit period BEFORE that rise
                and low half a bit period AFTER it. A receiver sampling fsync
                on the rise (a McASP at CLKRP = 1) then has half a bit period
                of setup and half of hold, sees fsync high across EXACTLY ONE
                rise, and with a one-bit data delay (dsp_a, RDATDLY = 1) takes
                slot 0's MSB on the very next rise.

                What did NOT move: fpos_r still advances on brise_w, the three
                exported timing ports are the same wires, and the deserializer
                samples tdm_data_i on the same rises it always did. The change
                is half a bit period of delay on ONE pin.

                THE BCLK PIN LEAVES FROM AN IOB FLOP (2026-09-19, issue #452).
                The platform packs bclk, fsync and dout into the output flop
                of their own IOBs, and that flop has no D-pin inverter and no
                route back into the fabric: its Q reaches the pad and nothing
                else. bclk used to be ONE self-toggling flop (bclk_r <=
                !bclk_r) that the enables also read, so Vivado folded the
                inverter into its D pin and every AX7101 placement stopped at
                Place 30-1008. Now bclk_n_r toggles in the fabric and bclk_r,
                the pad flop, copies it on every tick: the pad flop's D is a
                flop output and its one load is the pin, and brise_w/bfall_w
                read bclk_n_r, which is !bclk_r from reset on. The pin
                waveform, the enable cycles and the reset values are what
                they were. Two flops that swap values would not do: the pad
                flop would then feed its partner, and a single fabric load is
                enough for the placer to leave it in a slice. fsync_r and
                KL_tdm_render_master's tdm_dout_o already had the packable
                shape (a fabric D, no load but the pin).

                ONE TIMING OWNER (2026-09-14, issue #447). bclk and fsync are
                SHARED pins of one bus, so the render direction must not
                generate a second frame phase beside this one. This module
                stays the sole owner and EXPORTS its timing -
                bclk_rise_o / bclk_fall_o / frame_pos_o - for a same-domain
                render serializer (KL_tdm_render_master) to consume. The three
                ports are continuous assigns off wires that already existed:
                no flop, expression or reset here changed, so the capture
                waveform and the proven deserializer phase are untouched.

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
  parameter bit          DATA_DELAY_P = 1'b1  //! fsync->MSB offset (0 = DSP B,
                                              //! slot-0 MSB on the fsync edge
                                              //! itself; 1 = one bclk later,
                                              //! i.e. DSP A / Philips-heritage)
)(
  input  wire         clk_i,             //! datapath clock
  input  wire         rst_n,             //! active-low synchronous reset
  input  wire         clk_audio_i,       //! clean MMCM audio clock (24.576 MHz)

  // ---- TDM bus (we are MASTER: bclk/fsync are OUTPUTS) -----------------
  //! DURING RESET THE BUS PARKS: bclk LOW and fsync HIGH, and no bclk edge
  //! happens at all while rst_n is low, so nothing on the bus is clocked. The
  //! first rise after the release is therefore already the first frame's
  //! sync, and slot 0 starts from it. A receiver that needs an observable
  //! fsync EDGE rather than a level takes the next frame's, one frame later.
  output wire         tdm_mclk_o,        //! clk_audio_i/2 codec master clock
  output wire         tdm_bclk_o,        //! generated bit clock
  //! generated frame sync: one bclk period wide, registered on the bclk FALL.
  //! It goes high half a bit period BEFORE the rise it marks and low half a
  //! bit period AFTER it, so it is high across exactly ONE rise with half a
  //! bit period of setup and of hold there (issue #452).
  output wire         tdm_fsync_o,
  input  wire         tdm_data_i,        //! serial data, MSB first

  // ---- exported bus TIMING (clk_audio_i domain; RTL consumers only) ----
  //! THE ONE TIMING OWNER. There is exactly one TDM bus: bclk and fsync are
  //! shared pins and only this module drives them. A render serializer on the
  //! same bus therefore CONSUMES this timing instead of generating a second,
  //! unconstrained frame phase of its own. All three are continuous assigns
  //! off wires that already drive the deserializer, so no flop, expression or
  //! reset in this module changes and the pin waveform is bit for bit what it
  //! was. They are clk_audio_i-domain RTL signals, never a pin and never a
  //! clock: a pin-level receiver model must read bclk/fsync/dout and nothing
  //! here.
  output wire         bclk_rise_o,       //! one clk_audio_i cycle: at the END
                                         //! of this cycle the bclk pin goes
                                         //! 0 -> 1
  output wire         bclk_fall_o,       //! one clk_audio_i cycle: at the END
                                         //! of this cycle the bclk pin goes
                                         //! 1 -> 0
  //! PRE-EDGE frame position during a bclk_rise_o cycle. After that edge the
  //! position is (frame_pos_o + 1) mod SLOTS_P*WORD_BITS_P. The fsync pin is
  //! HIGH ACROSS the rise whose pre-edge position is 0 (it went high at the
  //! fall before it and goes low at the fall after it), so a pin-level
  //! receiver reads the sync on that rise.
  output wire [$clog2(SLOTS_P*WORD_BITS_P)-1:0] frame_pos_o,

  // ---- pair stream out (clk_i domain; one pulse per slot pair) ---------
  output logic        pair_valid_o,      //! one-cycle pulse per pair
  output logic [3:0]  pair_slot_o,       //! pair index (TDM slots {2k,2k+1})
  output logic [23:0] pair_l_o,
  output logic [23:0] pair_r_o,

  // ---- status (firmware-visible via CSR) ------------------------------
  output logic [31:0] pairs_captured_o   //! pairs captured (liveness)
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

  //! bclk generation: toggle every BCLK_HALF_P cycles of clk_audio_i.
  //!
  //! TWO FLOPS, AND ONLY ONE OF THEM IS THE PIN (see the banner). bclk_r is
  //! the PAD flop, packed into the bclk pin's IOB, and it takes bclk_n_r - a
  //! flop output, never an inversion - so nothing folds an inverter into its
  //! D. bclk_n_r toggles in the fabric and is !bclk_r from reset on (1 vs 0,
  //! and both move on every tick), so the two enables below read bclk_n_r
  //! and bclk_r drives the pin and nothing else.
  localparam int unsigned PHW_C = (BCLK_HALF_P <= 1) ? 1 : $clog2(BCLK_HALF_P);
  logic [PHW_C-1:0] phase_r;
  logic             bclk_r;             //! PAD flop: its only load is the pin
  logic             bclk_n_r;           //! fabric complement: always !bclk_r
  wire              tick_w  = (32'(phase_r) == BCLK_HALF_P - 1);
  //! the enable that REPLACES `posedge tdm_bclk_i`: the cycle on which bclk
  //! goes 0 -> 1. Everything the slave does on its clock edge, we do here.
  wire              brise_w = tick_w && bclk_n_r;

  always_ff @(posedge clk_audio_i) begin : t_bclk_gen
    if (!arst_n_w) begin
      phase_r  <= '0;
      bclk_r   <= 1'b0;
      bclk_n_r <= 1'b1;
    end else if (tick_w) begin
      phase_r  <= '0;
      bclk_r   <= bclk_n_r;
      bclk_n_r <= !bclk_n_r;
    end else begin
      phase_r <= phase_r + 1'b1;
    end
  end : t_bclk_gen
  assign tdm_bclk_o = bclk_r;

  //! the cycle on which bclk goes 1 -> 0: the LAUNCH edge of this bus, which
  //! is where tdm_dout_o changes too
  wire              bfall_w = tick_w && !bclk_n_r;

  //! frame position, advanced once per bclk RISE - unchanged, and it is what
  //! the deserializer and the exported ports are scheduled from.
  //!
  //! fsync is a one-bclk pulse taken on the bclk FALL (issue #452). The fall
  //! that sees fpos_r == 0 is the one half a bit period before the rise that
  //! ENDS bit period 0, and it carries the decision "the COMING rise is the
  //! frame sync": the pin is then high across that one rise, with half a bit
  //! period of setup and of hold, and the rise after it is where a one-bit
  //! delay (dsp_a) receiver takes slot 0's MSB. Registering fsync on brise_w
  //! instead put the transition ON the sampling edge.
  logic [$clog2(FRAME_C)-1:0] fpos_r;
  logic                       fsync_r;
  always_ff @(posedge clk_audio_i) begin : t_frame
    if (!arst_n_w) begin
      fpos_r  <= '0;
      fsync_r <= 1'b1;          //! parked HIGH: the first rise after the
                                //! release IS the first frame's sync
    end else begin
      if (brise_w)
        fpos_r  <= (32'(fpos_r) == FRAME_C - 1) ? '0 : fpos_r + 1'b1;
      if (bfall_w) fsync_r <= (32'(fpos_r) == 0);
    end
  end : t_frame
  assign tdm_fsync_o = fsync_r;

  //! the exported timing, one continuous assign each - see the port banner
  assign bclk_rise_o = brise_w;
  assign bclk_fall_o = bfall_w;
  assign frame_pos_o = fpos_r;

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
