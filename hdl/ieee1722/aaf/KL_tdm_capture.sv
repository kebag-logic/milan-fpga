/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_tdm_capture.sv
  Author      : Kebag Logic

  Date        : 2026-07-22
  Description : TDM slave audio-capture front-end (item-4 audio-interface
                family; docs/NXN_ARCHITECTURE.md §2.1 "physical interface
                x1"). Deserializes a SLOTS_P-slot TDM bus (8/16/32 slots,
                WORD_BITS_P bit clocks per slot, MSB first) and emits the
                same {slot, L, R} pair stream toward KL_aaf_packetizer that
                KL_aaf_capture_i2s emits for stereo I2S: pair k carries TDM
                slots {2k, 2k+1}, so a stream of C channels consumes C/2
                consecutive pair slots (the packetizer's TCTX chans field
                partitions the pair-slot space - see its header).

                INTERFACE CONTRACT (the whole capture family):
                  * clk_i-domain output: pair_valid_o one-cycle pulse,
                    pair_slot_o = pair index, pair_l_o/pair_r_o = 24-bit
                    left-justified samples;
                  * serial capture runs in the interface's own bit-clock
                    domain with a locally synchronized reset; pairs cross
                    into clk_i through the gray-pointer cdc_pair_fifo -
                    the clean-clock discipline copied from
                    KL_aaf_capture_i2s (07-18 lineage).

                TDM slave conventions (documented modes):
                  * we are bus SLAVE: tdm_bclk_i / tdm_fsync_i are inputs
                    driven by the codec/DSP master. tdm_mclk_o is a
                    convenience clk_audio_i/2 master clock (12.288 MHz off
                    the 24.576 MHz MMCM) for codecs that need an MCLK.
                  * data/fsync are sampled on the RISING bclk edge (the
                    master shifts on the falling edge - standard TDM).
                  * frame sync: only the 0->1 transition is meaningful, so
                    BOTH common shapes work unchanged: the one-bclk PULSE
                    (TI DSP / McASP style) and the 50%-duty long frame
                    clock (I2S-heritage TDM). A level is never trusted as
                    an edge: detection arms only after fsync has been
                    sampled LOW once out of reset (a long fsync already
                    high at enable would otherwise fake a mid-frame rise).
                  * DATA_DELAY_P selects the data offset: 0 = slot-0 MSB
                    on the same rising edge that first samples fsync high
                    (DSP mode A), 1 = one bclk later (DSP mode B /
                    Philips-heritage). The delay is applied HERE, ONCE -
                    never also in a TB chip model (the DOUBLE-Philips-delay
                    history, 78bbabe).
                  * every fsync start realigns the slot/bit counters (a
                    mid-frame fsync abandons the partial word); between
                    fsyncs the counters free-run at the exact frame length.
                  * samples: top min(24, WORD_BITS_P) bits of each slot,
                    left-justified into the 24-bit pipeline width.

                AES3/S-PDIF (later family members - contract only, see
                doc/audio_frontend_family.md): same pair-stream output and
                the same clean-clock discipline, with the bit clock RECOVERED
                from the biphase-mark line inside the module; subframes
                A/B map to pair slot 0 L/R.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! TDM slave deserializer (item-4 front-end family): SLOTS_P x WORD_BITS_P
//! frame -> {pair_slot, L, R} stream in clk_i via the gray-pointer pair CDC.
//! Pulse and 50%-duty frame syncs, data delay 0/1, MSB first.

`default_nettype none

module KL_tdm_capture #(
  parameter int unsigned SLOTS_P      = 8,    //! TDM slots per frame (8/16/32)
  parameter int unsigned WORD_BITS_P  = 32,   //! bit clocks per slot (16/24/32)
  parameter bit          DATA_DELAY_P = 1'b1  //! fsync->MSB offset (0 = DSP A,
                                              //! 1 = DSP B / Philips-heritage)
)(
  input  wire         clk_i,             //! datapath clock
  input  wire         rst_n,             //! active-low synchronous reset
  input  wire         clk_audio_i,       //! clean MMCM audio clock (24.576 MHz)

  // ---- TDM bus (we are slave; master drives bclk/fsync) ----------------
  output wire         tdm_mclk_o,        //! clk_audio_i/2 codec master clock
  input  wire         tdm_bclk_i,        //! bit clock (capture domain)
  input  wire         tdm_fsync_i,       //! frame sync (pulse or 50% duty)
  input  wire         tdm_data_i,        //! serial data, MSB first

  // ---- pair stream out (clk_i domain; one pulse per slot pair) ---------
  output logic        pair_valid_o,      //! one-cycle pulse per pair
  output logic [3:0]  pair_slot_o,       //! pair index (TDM slots {2k,2k+1})
  output logic [23:0] pair_l_o,
  output logic [23:0] pair_r_o,

  // ---- status (Linux-observable via CSR) ------------------------------
  output reg  [31:0]  pairs_captured_o   //! pairs captured (liveness)
);

  localparam int unsigned BW_C = $clog2(WORD_BITS_P);
  localparam int unsigned SW_C = $clog2(SLOTS_P);

  //! convenience MCLK: registered divider of the clean audio clock (the
  //! clean-clock rule - never a fractional-N edge, see KL_aaf_capture_i2s)
  logic [1:0] marst_n_r;
  logic       mdiv_r;
  always_ff @(posedge clk_audio_i) begin : t_mclk_div
    marst_n_r <= {marst_n_r[0], rst_n};
    if (!marst_n_r[1]) mdiv_r <= 1'b0;
    else               mdiv_r <= !mdiv_r;
  end : t_mclk_div
  assign tdm_mclk_o = mdiv_r;

  // ======================================================================
  //  bclk domain: frame tracking + slot deserializer
  // ======================================================================
  logic [1:0] brst_n_r;                 //! bclk-domain reset sync
  always_ff @(posedge tdm_bclk_i) begin : t_bclk_rst
    brst_n_r <= {brst_n_r[0], rst_n};
  end : t_bclk_rst

  logic                   fsync_q_r;    //! fsync at the previous rising edge
  logic                   armed_r;      //! fsync sampled low once (edge valid)
  logic                   startp_r;     //! DATA_DELAY_P=1: MSB on next edge
  logic                   run_r;        //! a frame start has been seen
  logic [BW_C-1:0]        bit_r;
  logic [SW_C-1:0]        slot_r;
  logic [WORD_BITS_P-1:0] shift_r;
  logic [23:0]            lhold_r;      //! even-slot sample awaiting its pair
  logic                   cap_wen_r;
  logic [3:0]             cap_slot_r;
  logic [23:0]            cap_l_r, cap_r_r;
  wire                    cap_full_w;

  //! frame start = ARMED fsync 0->1 sampled on the rising edge; with delay 1
  //! the MSB rides the NEXT edge (this edge still finishes the prior frame)
  wire start_w = tdm_fsync_i && !fsync_q_r && armed_r;
  wire sol_w   = DATA_DELAY_P ? startp_r : start_w;

  //! effective position of THIS edge (a frame start overrides the counters)
  wire [SW_C-1:0] eslot_w = sol_w ? '0 : slot_r;
  wire [BW_C-1:0] ebit_w  = sol_w ? '0 : bit_r;
  //! completed slot word (available on the edge capturing its last bit)
  wire [WORD_BITS_P-1:0] word_w = {shift_r[WORD_BITS_P-2:0], tdm_data_i};
  //! top min(24, WORD_BITS_P) bits, left-justified into 24
  wire [WORD_BITS_P+23:0] wext_w = {word_w, 24'b0};
  wire [23:0]             smp_w  = 24'(wext_w >> WORD_BITS_P);

  always_ff @(posedge tdm_bclk_i) begin : t_deser
    if (!brst_n_r[1]) begin
      fsync_q_r <= 1'b0; armed_r <= 1'b0; startp_r <= 1'b0; run_r <= 1'b0;
      bit_r <= '0; slot_r <= '0; shift_r <= '0; lhold_r <= '0;
      cap_wen_r <= 1'b0; cap_slot_r <= '0; cap_l_r <= '0; cap_r_r <= '0;
    end else begin
      fsync_q_r <= tdm_fsync_i;
      if (!tdm_fsync_i) armed_r <= 1'b1;
      startp_r  <= start_w;
      cap_wen_r <= 1'b0;
      if (run_r || sol_w) begin
        run_r   <= 1'b1;
        shift_r <= {shift_r[WORD_BITS_P-2:0], tdm_data_i};
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
  //  pairs into the datapath clock domain (gray-pointer CDC)
  // ======================================================================
  wire        cap_rempty_w;
  wire [51:0] cap_pair_w;
  logic       cap_ren_r;
  cdc_pair_fifo #(.WIDTH(52), .LOG2D(3)) u_tcdc (
    .wclk_i  (tdm_bclk_i),
    .wrst_n  (brst_n_r[1]),
    .wen_i   (cap_wen_r),
    .wdata_i ({cap_slot_r, cap_l_r, cap_r_r}),
    .wfull_o (cap_full_w),
    .rclk_i  (clk_i),
    .rrst_n  (rst_n),
    .ren_i   (cap_ren_r),
    .rdata_o (cap_pair_w),
    .rempty_o(cap_rempty_w)
  );

  //! clk_i side: pop one pair at a time; pair_valid pulses per pop. The
  //! FIFO registers rdata_o ON the ren edge, so the pop cycle's data is
  //! live during the following pair_valid cycle - the outputs alias
  //! rdata_o directly (it holds until the next ren).
  always_ff @(posedge clk_i or negedge rst_n) begin : t_pop
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
