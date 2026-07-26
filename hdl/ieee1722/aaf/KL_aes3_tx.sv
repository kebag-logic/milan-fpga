/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_aes3_tx.sv
  Author      : Kebag Logic

  Date        : 2026-07-26
  Description : AES3 / S-PDIF biphase-mark TRANSMITTER - the render half of
                the item-4 AES3 family (doc/audio_frontend_family.md). The
                exact inverse of KL_aes3_rx: it consumes the SAME {pair 0,
                L, R} stereo pair stream the render path already speaks
                (KL_chan_map_render / KL_i2s_playback) and serializes it as
                a legal AES3-2009 / IEC 60958 biphase-mark line.

                Structure (mirror image of the receiver):
                  * pairs arrive in clk_i and cross into the SERIAL clock
                    domain clk_audio_i through the gray-pointer
                    cdc_pair_fifo - the same family CDC discipline, the same
                    52-bit-class payload ({L, R}, slot implicit 0);
                  * clk_audio_i is the bit-rate reference: one unit interval
                    (UI) is OVERSAMPLE_P cycles, a data cell is 2 UI, a
                    subframe is 64 UI and a frame (A + B) is 128 UI. At
                    48 kHz that is 128 x 48000 x OVERSAMPLE_P = 24.576 MHz
                    for OVERSAMPLE_P = 4 - the clean MMCM audio clock.

                Line coding (AES3-2009 4.1):
                  * biphase mark: EVERY cell starts with a transition; a '1'
                    adds a mid-cell transition, a '0' does not. The encoder
                    therefore only ever decides "toggle or hold" per UI,
                    which makes it polarity-free by construction.
                  * the four preamble cells are emitted as raw UI toggle
                    masks - the run signatures the receiver hunts:
                        X (subframe A, mid-block) 3,3,1,1 -> toggles 0,3,6,7
                        Y (subframe B)            3,2,1,2 -> toggles 0,3,5,6
                        Z (subframe A, block 0)   3,1,1,3 -> toggles 0,3,4,5
                    all opening with the 3-UI run that biphase mark cannot
                    otherwise produce.

                Subframe assembly (AES3-2009 Table 2, LSB first):
                    [3:0] preamble  [7:4] aux  [27:8] sample(20)
                    [28] V  [29] U  [30] C  [31] P
                  * WORD_BITS_P bits are taken from the MSB end of the
                    24-bit pipeline sample and placed at the MSB end of the
                    aux+sample field, so a 16- or 20-bit link truncates
                    where the wire says it does;
                  * V is driven from smp_invalid_i (the wire-truth rule: the
                    transmitter never silently substitutes silence);
                  * U is 0 (no user-data channel - stated, not hidden);
                  * C is bit `frame index` of the channel-status block, from
                    cs_bits_i for the first 32 frames and 0 for the rest;
                    both subframes carry the same block (a Milan end station
                    has one media clock and one channel status).
                  * P makes bits [31:4] EVEN parity.

                Honest reporting: frames_o / blocks_o are the liveness
                census, underrun_o counts frames that started with no fresh
                pair in the FIFO. An underrun REPEATS the last sample and
                keeps the line legal - a gap in a biphase-mark stream would
                cost the far end its lock, which is a far worse failure than
                one repeated frame. All three counters live in clk_i (event
                pulses crossed with cdc_pulse).

                NOT implemented (stated, not hidden): the user-data channel,
                the professional byte-23 CRC, channel-status bits beyond
                CS_SRC_BITS_C, and per-subframe (A != B) channel status.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! AES3 / S-PDIF biphase-mark transmitter (item-4 front-end family): {pair 0,
//! L, R} -> X/Y/Z framed, parity-correct, channel-status-carrying BMC line.

`default_nettype none

module KL_aes3_tx #(
  parameter int unsigned OVERSAMPLE_P = 4,    //! clk_audio_i cycles per unit interval
  parameter int unsigned WORD_BITS_P  = 24,   //! sample width put on the wire (16/20/24)
  parameter bit          CONSUMER_P   = 1'b0  //! documents the channel-status dialect of cs_bits_i
)(
  input  wire         clk_i,             //! datapath clock (pair input + census)
  input  wire         rst_n,             //! active-low synchronous reset (clk_i)
  input  wire         clk_audio_i,       //! serial bit-rate reference

  // ---- pair stream in (clk_i domain; family contract) -------------------
  input  wire         pair_valid_i,      //! one-cycle pulse per L/R pair
  input  wire [23:0]  pair_l_i,          //! subframe A sample, MSB-justified
  input  wire [23:0]  pair_r_i,          //! subframe B sample, MSB-justified
  input  wire         smp_invalid_i,     //! drives the V bit of both subframes
  output wire         pair_ready_o,      //! FIFO has room for another pair

  // ---- channel status (clk_i domain, quasi-static) ----------------------
  input  wire [31:0]  cs_bits_i,         //! channel-status bits 0..31 (rest transmitted 0)

  // ---- line + census ----------------------------------------------------
  output wire         aes_tx_o,          //! biphase-mark line out
  output logic [31:0] frames_o,          //! frames transmitted (liveness)
  output logic [15:0] blocks_o,          //! 192-frame blocks transmitted
  output logic [15:0] underrun_o         //! frames that repeated the last pair
);

  // ======================================================================
  //  local constants
  // ======================================================================
  localparam int unsigned BLOCK_FRAMES_C = 192;  //! AES3-2009 4.3 block length
  localparam int unsigned CS_SRC_BITS_C  = 32;   //! channel-status bits cs_bits_i carries
  localparam int unsigned SUB_UI_C       = 64;   //! UI per subframe (4 + 28 cells)
  localparam int unsigned PRE_UI_C       = 8;    //! UI of preamble per subframe
  localparam int unsigned OSW_C          = (OVERSAMPLE_P < 2)
                                           ? 1 : $clog2(OVERSAMPLE_P);

  //! UI toggle masks, bit i = "toggle the line entering UI i"
  localparam logic [7:0] PRE_X_C = 8'b1100_1001;  //! runs 3,3,1,1 (toggles 0,3,6,7)
  localparam logic [7:0] PRE_Y_C = 8'b0110_1001;  //! runs 3,2,1,2 (toggles 0,3,5,6)
  localparam logic [7:0] PRE_Z_C = 8'b0011_1001;  //! runs 3,1,1,3 (toggles 0,3,4,5)

  // ======================================================================
  //  pairs from the datapath clock (gray-pointer CDC, family discipline)
  // ======================================================================
  logic [1:0] arst_n_r;
  always_ff @(posedge clk_audio_i) begin : t_arst
    arst_n_r <= {arst_n_r[0], rst_n};
  end : t_arst
  wire arst_n_w = arst_n_r[1];

  wire         src_full_w;
  wire         src_empty_w;
  wire [47:0]  src_pair_w;
  logic        src_ren_r;
  cdc_pair_fifo #(.WIDTH(48), .LOG2D(3)) u_scdc (
    .wclk_i  (clk_i),
    .wrst_n  (rst_n),
    .wen_i   (pair_valid_i && !src_full_w),
    .wdata_i ({pair_l_i, pair_r_i}),
    .wfull_o (src_full_w),
    .rclk_i  (clk_audio_i),
    .rrst_n  (arst_n_w),
    .ren_i   (src_ren_r),
    .rdata_o (src_pair_w),
    .rempty_o(src_empty_w)
  );
  assign pair_ready_o = !src_full_w;

  //! smp_invalid_i is quasi-static policy, not per-sample data: sample it in
  //! the serial domain with a plain 2-FF synchroniser.
  logic [1:0] inv_s_r;

  // ======================================================================
  //  clk_audio_i domain: framing + biphase-mark serializer
  // ======================================================================
  logic [OSW_C-1:0] uicnt_r;             //! clk_audio_i cycles inside this UI
  logic [6:0]       uidx_r;              //! UI index inside the subframe (0..63)
  logic             subb_r;              //! 0 = subframe A, 1 = subframe B
  logic [7:0]       fidx_r;              //! frame index inside the block (0..191)
  logic [23:0]      lcur_r, rcur_r;      //! the frame being transmitted
  logic [23:0]      lnxt_r, rnxt_r;      //! the prefetched next frame
  logic             nxt_vld_r;           //! a prefetched frame is waiting
  logic             src_rvld_r;          //! rdata_o carries the popped word THIS cycle
  logic             line_r;
  logic             csinit_r;            //! cs_bits_i has been latched at least once
  logic             frame_p_r, block_p_r, under_p_r;

  wire ui_last_w  = (32'(uicnt_r) == OVERSAMPLE_P - 1);
  wire ui_first_w = (uicnt_r == '0);
  //! the very first UI of subframe A is the frame boundary
  wire frame_top_w = ui_first_w && (uidx_r == '0) && !subb_r;

  //! the sample this subframe carries, MSB-justified into the aux+sample field
  wire [23:0] smp_w = subb_r ? rcur_r : lcur_r;
  //! channel-status bit for this frame (0 beyond the bits cs_bits_i carries)
  logic [CS_SRC_BITS_C-1:0] cs_lat_r;    //! cs_bits_i latched per block
  wire  cs_bit_w = (32'(fidx_r) < CS_SRC_BITS_C) ? cs_lat_r[fidx_r[4:0]] : 1'b0;

  //! subframe word, LSB first; [3:0] are the preamble cells (never shifted
  //! out as data, so they stay 0) and P closes even parity over [31:4]
  logic [31:0] sub_w;
  always_comb begin : t_subframe
    sub_w         = 32'h0;
    sub_w[27 -: WORD_BITS_P] = smp_w[23 -: WORD_BITS_P];
    sub_w[28]     = inv_s_r[1];          //! V
    sub_w[29]     = 1'b0;                //! U
    sub_w[30]     = cs_bit_w;            //! C
    sub_w[31]     = ^sub_w[30:4];        //! P: even parity over [31:4]
  end : t_subframe

  //! preamble in use this subframe
  wire [7:0] pre_w = subb_r ? PRE_Y_C
                            : ((fidx_r == 8'd0) ? PRE_Z_C : PRE_X_C);

  //! cell / half-cell position inside the 28 data cells
  wire [6:0] duidx_w = uidx_r - 7'(PRE_UI_C);
  wire [4:0] cell_w  = 5'(duidx_w >> 1);
  wire       half_w  = duidx_w[0];
  wire [4:0] bidx_w  = cell_w + 5'd4;    //! subframe bit this cell carries
  wire       bit_w   = sub_w[bidx_w];

  //! toggle decision for the UI being entered: preamble cells follow the
  //! mask, data cells always toggle on the first half and toggle on the
  //! second half only for a '1'
  wire tog_w = (32'(uidx_r) < PRE_UI_C) ? pre_w[uidx_r[2:0]]
                                        : (!half_w || bit_w);

  always_ff @(posedge clk_audio_i) begin : t_serial
    if (!arst_n_w) begin
      inv_s_r    <= '0;
      cs_lat_r   <= '0;
      csinit_r   <= 1'b0;
      uicnt_r    <= '0;
      uidx_r     <= '0;
      subb_r     <= 1'b0;
      fidx_r     <= '0;
      lcur_r     <= '0;
      rcur_r     <= '0;
      lnxt_r     <= '0;
      rnxt_r     <= '0;
      nxt_vld_r  <= 1'b0;
      line_r     <= 1'b0;
      src_ren_r  <= 1'b0;
      src_rvld_r <= 1'b0;
      frame_p_r  <= 1'b0;
      block_p_r  <= 1'b0;
      under_p_r  <= 1'b0;
    end else begin
      inv_s_r   <= {inv_s_r[0], smp_invalid_i};
      frame_p_r <= 1'b0;
      block_p_r <= 1'b0;
      under_p_r <= 1'b0;

      //! the line changes ONCE per UI, at its first cycle
      if (ui_first_w) line_r <= line_r ^ tog_w;

      //! a frame boundary: take the prefetched pair, or repeat and confess
      if (frame_top_w) begin
        frame_p_r <= 1'b1;
        if (fidx_r == 8'd0) block_p_r <= 1'b1;
        //! channel status is latched per BLOCK, one frame BEFORE the block
        //! starts, so frame 0 already carries the fresh word
        if (!csinit_r || (32'(fidx_r) == BLOCK_FRAMES_C - 1)) begin
          cs_lat_r <= cs_bits_i;
          csinit_r <= 1'b1;
        end
        if (nxt_vld_r) begin
          lcur_r    <= lnxt_r;
          rcur_r    <= rnxt_r;
          nxt_vld_r <= 1'b0;
        end else begin
          under_p_r <= 1'b1;             //! repeat lcur_r/rcur_r, stay legal
        end
      end

      //! prefetch: cdc_pair_fifo registers rdata_o ON the ren edge, so the
      //! popped word is live the cycle AFTER ren - never at the frame top.
      //! Placed after the consumer so a pop landing on a frame boundary
      //! keeps its fresh word instead of being cleared by the handover.
      src_ren_r  <= !nxt_vld_r && !src_empty_w && !src_ren_r && !src_rvld_r;
      src_rvld_r <= src_ren_r;
      if (src_rvld_r) begin
        lnxt_r    <= src_pair_w[47:24];
        rnxt_r    <= src_pair_w[23:0];
        nxt_vld_r <= 1'b1;
      end

      if (ui_last_w) begin
        uicnt_r <= '0;
        if (32'(uidx_r) == SUB_UI_C - 1) begin
          uidx_r <= '0;
          subb_r <= !subb_r;
          if (subb_r) fidx_r <= (32'(fidx_r) == BLOCK_FRAMES_C - 1)
                                ? 8'd0 : fidx_r + 1'b1;
        end else begin
          uidx_r <= uidx_r + 1'b1;
        end
      end else begin
        uicnt_r <= uicnt_r + 1'b1;
      end
    end
  end : t_serial

  assign aes_tx_o = line_r;

  // ======================================================================
  //  census in clk_i
  // ======================================================================
  wire frm_p_w, blk_p_w, und_p_w;
  cdc_pulse u_p_frm (.src_clk(clk_audio_i), .src_rst_n(arst_n_w),
                     .src_pulse(frame_p_r), .dest_clk(clk_i),
                     .dest_rst_n(rst_n), .dest_pulse(frm_p_w));
  cdc_pulse u_p_blk (.src_clk(clk_audio_i), .src_rst_n(arst_n_w),
                     .src_pulse(block_p_r), .dest_clk(clk_i),
                     .dest_rst_n(rst_n), .dest_pulse(blk_p_w));
  cdc_pulse u_p_und (.src_clk(clk_audio_i), .src_rst_n(arst_n_w),
                     .src_pulse(under_p_r), .dest_clk(clk_i),
                     .dest_rst_n(rst_n), .dest_pulse(und_p_w));

  always_ff @(posedge clk_i) begin : t_census
    if (!rst_n) begin
      frames_o   <= '0;
      blocks_o   <= '0;
      underrun_o <= '0;
    end else begin
      if (frm_p_w)                    frames_o   <= frames_o + 1'b1;
      if (blk_p_w && !(&blocks_o))    blocks_o   <= blocks_o + 1'b1;
      if (und_p_w && !(&underrun_o))  underrun_o <= underrun_o + 1'b1;
    end
  end : t_census

endmodule

`default_nettype wire
