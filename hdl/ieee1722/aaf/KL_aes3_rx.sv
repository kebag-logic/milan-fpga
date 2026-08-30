/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_aes3_rx.sv
  Author      : Kebag Logic

  Date        : 2026-07-26
  Description : AES3 / S-PDIF biphase-mark RECEIVER - the last member of the
                item-4 audio-interface family (doc/audio_frontend_family.md,
                "AES3 / S-PDIF contract"). ONE deserializer core serves both
                transports; CONSUMER_P selects only how the channel-status
                block is INTERPRETED (AES3-2009 professional vs
                IEC 60958-3 consumer), never how it is decoded.

                Family output contract (identical to KL_aaf_capture_i2s /
                KL_tdm_capture, so KL_aaf_packetizer never changes):
                  * clk_i-domain pair stream: pair_valid_o one-cycle pulse,
                    pair_slot_o = 0 (a stereo member owns pair 0),
                    pair_l_o/pair_r_o = 24-bit MSB-justified samples;
                  * serial capture runs in the interface's own bit-clock
                    domain - here the OVERSAMPLING clock clk_audio_i, since
                    an AES3 link carries no separate bit clock - and pairs
                    cross into clk_i through the gray-pointer cdc_pair_fifo.

                Line decoding (no external bit clock exists):
                  * clk_audio_i oversamples the biphase-mark line; the time
                    between line transitions is measured in clk_audio_i
                    cycles and classified against a MEASURED unit-interval
                    (UI) estimate - the receiver never assumes a sample
                    rate. Acquisition takes the smallest run over
                    HUNT_RUNS_P runs (a frame's worth) as 1 UI; afterwards
                    every 1-UI run blends into the estimate (3/4 + 1/4), so
                    it tracks source drift.
                  * a data cell is 2 UI: one 2-UI run = '0', two 1-UI runs =
                    '1'. A 3-UI run is impossible in biphase mark, which is
                    exactly what the X/Y/Z preambles use as their sync
                    anchor; run signatures (AES3-2009 4.1, IEC 60958-3 4.2):
                        X (subframe A, mid-block) 3,3,1,1
                        Y (subframe B)            3,2,1,2
                        Z (subframe A, block 0)   3,1,1,3
                    all 8 UI = 4 cells, all opening with the illegal 3-UI
                    run, and all satisfying r3 == 1 UI and r2 + r4 == 4 UI -
                    which is how r2 both SELECTS the preamble and how r3/r4
                    VERIFY it. Polarity-independent by construction (only
                    intervals are measured), so an inverted line decodes.

                Subframe (32 cells, LSB first, AES3-2009 Table 2):
                    [3:0] preamble  [7:4] aux  [27:8] sample(20)
                    [28] V  [29] U  [30] C  [31] P (even over [31:4])
                  * WORD_BITS_P 24 takes aux+sample as one 24-bit word; 20
                    and 16 take the top bits of that field and MSB-justify
                    into the 24-bit pipeline width;
                  * subframe A -> pair_l_o, subframe B -> pair_r_o, the pair
                    emitted on B completion with pair_slot_o = 0.

                Honest lock / error reporting (the contract's rule):
                  * a P-parity failure, a biphase violation or a malformed
                    preamble DROPS lock immediately - no pairs are emitted
                    while unlocked - and lock is only re-armed by
                    LOCK_BLOCKS_P consecutive CLEAN 192-frame blocks;
                  * V (validity) set does NOT drop lock and does NOT
                    suppress the pair: the wire truth reaches the talker and
                    invalid_o counts it (policy belongs to the control plane,
                    never to the capture front-end);
                  * a line with no transition for 2**RUN_W_P cycles is a
                    lock loss, not a hang;
                  * every counter is a saturating 16-bit CSR-observable
                    census in clk_i (event pulses crossed with cdc_pulse);
                    pairs_captured_o is the family liveness counter.

                Channel status: the first CS_SNAP_BITS_C C bits of SUBFRAME
                A of each block are snapshotted at the FOLLOWING block start
                (Z) and published with cs_valid_o. The interpretation ports
                are the only thing CONSUMER_P changes:
                  professional  byte0[0]=1, emphasis byte0[4:2],
                                fs byte0[7:6]
                  consumer      byte0[0]=0, emphasis byte0[5:3],
                                fs byte3[3:0]
                cs_mismatch_o flags a block whose own professional/consumer
                bit disagrees with CONSUMER_P (the classic "S-PDIF source in
                the AES3 socket" complaint) without refusing the audio.

                NOT implemented (stated, not hidden): the U (user-data)
                channel is decoded into the subframe word but not exported;
                only the first CS_SNAP_BITS_C channel-status bits are kept
                (a full 192-bit block needs a CSR window, not a port); the
                CRC of professional byte 23 is not checked; subframe B
                channel status is not accumulated separately.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! AES3 / S-PDIF biphase-mark receiver (item-4 front-end family): recovered
//! symbol clock, X/Y/Z framing, parity + channel status -> {pair 0, L, R}.

`default_nettype none

module KL_aes3_rx #(
  parameter bit          CONSUMER_P    = 1'b0, //! 0 = AES3 professional, 1 = IEC 60958-3 consumer (S/PDIF)
  parameter int unsigned WORD_BITS_P   = 24,   //! sample width taken off the wire (16/20/24)
  parameter int unsigned LOCK_BLOCKS_P = 2,    //! consecutive CLEAN blocks required to (re-)lock
  parameter int unsigned HUNT_RUNS_P   = 64,   //! runs measured to acquire the UI estimate
  parameter int unsigned RUN_W_P       = 12    //! edge-interval counter width (clk_audio_i cycles)
)(
  input  wire         clk_i,             //! datapath clock (pair stream + census)
  input  wire         rst_n,             //! active-low synchronous reset (clk_i)
  input  wire         clk_audio_i,       //! oversampling clock (>= 4x the UI rate)
  input  wire         aes_rx_i,          //! biphase-mark line in (asynchronous)

  // ---- pair stream out (clk_i domain; family contract) ------------------
  output logic        pair_valid_o,      //! one-cycle pulse per L/R pair
  output logic [3:0]  pair_slot_o,       //! always 0 (stereo members own pair 0)
  output logic [23:0] pair_l_o,          //! subframe A sample, MSB-justified
  output logic [23:0] pair_r_o,          //! subframe B sample, MSB-justified
  output logic [31:0] pairs_captured_o,  //! pairs captured (family liveness)

  // ---- lock / channel status (clk_i domain, CSR-observable) -------------
  output logic        locked_o,          //! subframe+block sync held (pairs flow)
  output logic        cs_valid_o,        //! at least one complete block captured
  output logic [31:0] cs_bits_o,         //! first 32 channel-status bits, subframe A
  output logic        cs_pro_o,          //! channel status says PROFESSIONAL (byte0[0])
  output logic [3:0]  cs_fs_code_o,      //! sample-frequency code, per CONSUMER_P
  output logic [2:0]  cs_emphasis_o,     //! emphasis code, per CONSUMER_P
  output logic        cs_mismatch_o,     //! block's own pro/consumer bit != CONSUMER_P

  // ---- error census (clk_i domain, saturating) --------------------------
  output logic [15:0] blocks_o,          //! Z preambles seen (block liveness)
  output logic [15:0] parity_err_o,      //! subframes failing the P even-parity check
  output logic [15:0] invalid_o,         //! subframes carrying V=1 (pair still emitted)
  output logic [15:0] sync_loss_o        //! locked -> unlocked transitions
);

  // ======================================================================
  //  local constants
  // ======================================================================
  localparam int unsigned BLOCK_FRAMES_C = 192; //! AES3-2009 4.3 block length
  localparam int unsigned CS_SNAP_BITS_C = 32;  //! channel-status bits published
  localparam int unsigned SUB_CELLS_C    = 28;  //! data cells after the preamble
  localparam int unsigned RW_C           = RUN_W_P + 3; //! threshold arithmetic width
  localparam int unsigned LKW_C          = $clog2(LOCK_BLOCKS_P + 2);
  localparam int unsigned HTW_C          = $clog2(HUNT_RUNS_P + 1);

  //! run classes returned by the interval discriminator
  localparam logic [1:0] CL_BAD_C = 2'd0;  //! glitch / illegal interval
  localparam logic [1:0] CL_1UI_C = 2'd1;
  localparam logic [1:0] CL_2UI_C = 2'd2;
  localparam logic [1:0] CL_3UI_C = 2'd3;  //! preamble anchor (illegal in BMC)

  //! preamble identity, taken verbatim from the r2 class
  localparam logic [1:0] PRE_Z_C = 2'd1;   //! 3,1,1,3 - subframe A, block start
  localparam logic [1:0] PRE_Y_C = 2'd2;   //! 3,2,1,2 - subframe B
  localparam logic [1:0] PRE_X_C = 2'd3;   //! 3,3,1,1 - subframe A, mid-block

  typedef enum logic [1:0] { HUNT_S, SYNC_S, PRE_S, DATA_S } rstate_t;

  // ======================================================================
  //  clk_audio_i domain: line recovery, framing, channel status
  // ======================================================================
  logic [1:0] arst_n_r;                  //! audio-domain reset synchroniser
  always_ff @(posedge clk_audio_i) begin : t_arst
    arst_n_r <= {arst_n_r[0], rst_n};
  end : t_arst
  wire arst_n_w = arst_n_r[1];

  //! 2-FF input synchroniser + one stage for edge detection
  logic [2:0]         rxs_r;
  logic [RUN_W_P-1:0] ecnt_r;            //! clk_audio_i cycles since the last edge
  logic [RUN_W_P-1:0] ui_r;              //! measured unit interval
  logic [RUN_W_P-1:0] hmin_r;            //! HUNT: smallest run seen so far
  logic [HTW_C-1:0]   hcnt_r;            //! HUNT: runs measured
  rstate_t            st_r;
  logic [1:0]         pidx_r;            //! preamble run index (1..3 after the anchor)
  logic [1:0]         ptype_r;           //! PRE_Z_C / PRE_Y_C / PRE_X_C
  logic [1:0]         pr2_r;             //! r2 class, kept for the r2+r4 == 4 check
  logic               half_r;            //! a 1-UI half-cell is outstanding
  logic [4:0]         cell_r;            //! data cells decoded in this subframe (0..27)
  logic [31:0]        sub_r;             //! subframe under construction (LSB first)
  logic [7:0]         fidx_r;            //! frame index inside the block (0..191)
  logic               have_a_r;          //! subframe A of this frame has been decoded
  logic [23:0]        lhold_r;           //! subframe A sample awaiting its B
  logic [CS_SNAP_BITS_C-1:0] csacc_r;    //! channel status accumulating this block
  logic [CS_SNAP_BITS_C-1:0] cssnap_r;   //! last COMPLETE block's snapshot
  logic               sawz_r;            //! a Z has been seen (the next Z ends a full block)
  logic               blkclean_r;        //! no error since this block started
  logic [LKW_C-1:0]   clean_r;           //! consecutive clean blocks
  logic               locked_r;

  //! event pulses (audio domain) crossed into clk_i for the census
  logic parity_p_r, invalid_p_r, syncloss_p_r, block_p_r, csnew_p_r;

  //! FIFO write side
  logic        cap_wen_r;
  logic [47:0] cap_data_r;
  wire         cap_full_w;

  wire edge_w    = rxs_r[2] ^ rxs_r[1];
  wire estall_w  = &ecnt_r;              //! no transition in a full count = dead line

  //! the run that just ended (valid on edge_w)
  wire [RW_C-1:0] run_w = RW_C'(ecnt_r);
  wire [RW_C-1:0] ui_w  = RW_C'(ui_r);
  //! class boundaries at 0.5 / 1.5 / 2.5 / 3.5 UI
  wire [RW_C-1:0] thr_lo_w = ui_w >> 1;
  wire [RW_C-1:0] thr_12_w = ui_w + (ui_w >> 1);
  wire [RW_C-1:0] thr_23_w = (ui_w << 1) + (ui_w >> 1);
  wire [RW_C-1:0] thr_hi_w = (ui_w << 1) + ui_w + (ui_w >> 1);
  wire [1:0] cls_w = (run_w <= thr_lo_w) ? CL_BAD_C :
                     (run_w <  thr_12_w) ? CL_1UI_C :
                     (run_w <  thr_23_w) ? CL_2UI_C :
                     (run_w <  thr_hi_w) ? CL_3UI_C : CL_BAD_C;
  //! 3/4 + 1/4 blend, so the estimate tracks drift without ever running away
  wire [RUN_W_P-1:0] ui_blend_w = (ui_r - (ui_r >> 2)) + (ecnt_r >> 2);

  //! sample of the subframe that just completed: bits [27:4] are the 24-bit
  //! aux+sample field, LSB first; take its top WORD_BITS_P bits and
  //! MSB-justify into the 24-bit pipeline width.
  wire [23:0] smp_w = 24'({sub_r[27 -: WORD_BITS_P],
                           {(24 - WORD_BITS_P){1'b0}}});

  //! cell decode. A 2-UI run mid-cell is a biphase VIOLATION, never a
  //! completion - which is why cell_done_w qualifies on !half_r.
  wire cell_done_w = ((cls_w == CL_2UI_C) && !half_r)
                  || ((cls_w == CL_1UI_C) &&  half_r);
  wire cell_bit_w  = (cls_w == CL_1UI_C);
  wire [4:0] cell_idx_w = cell_r + 5'd4;   //! subframe bit this cell lands in

  //! preamble signature check: r2 names it, r3 must be 1 UI, r2 + r4 == 4 UI
  wire pre_ok_w = (pidx_r == 2'd1) ? (cls_w != CL_BAD_C)
                : (pidx_r == 2'd2) ? (cls_w == CL_1UI_C)
                : ((3'(pr2_r) + 3'(cls_w)) == 3'd4);

  //! the three things that cost lock (contract), all qualified by edge_w
  wire pre_bad_w  = (st_r == PRE_S) && !pre_ok_w;
  wire data_bad_w = (st_r == DATA_S)
                 && ((cls_w == CL_BAD_C) || (cls_w == CL_3UI_C)
                     || ((cls_w == CL_2UI_C) && half_r));
  wire sub_end_w  = (st_r == DATA_S) && cell_done_w
                 && (32'(cell_r) == SUB_CELLS_C - 1);
  //! P is even parity over bits [31:4]; the last cell is folded in here
  wire par_bad_w  = sub_end_w && (^{sub_r[30:4], cell_bit_w});
  wire err_w      = edge_w && (pre_bad_w || data_bad_w || par_bad_w);
  //! a preamble completes on its fourth run
  wire pre_end_w  = edge_w && (st_r == PRE_S) && pre_ok_w && (pidx_r == 2'd3);

  always_ff @(posedge clk_audio_i) begin : t_recover
    if (!arst_n_w) begin
      rxs_r        <= '0;
      ecnt_r       <= '0;
      ui_r         <= '0;
      hmin_r       <= '1;
      hcnt_r       <= '0;
      st_r         <= HUNT_S;
      pidx_r       <= '0;
      ptype_r      <= '0;
      pr2_r        <= '0;
      half_r       <= 1'b0;
      cell_r       <= '0;
      sub_r        <= '0;
      fidx_r       <= '0;
      have_a_r     <= 1'b0;
      lhold_r      <= '0;
      csacc_r      <= '0;
      cssnap_r     <= '0;
      sawz_r       <= 1'b0;
      blkclean_r   <= 1'b0;
      clean_r      <= '0;
      locked_r     <= 1'b0;
      parity_p_r   <= 1'b0;
      invalid_p_r  <= 1'b0;
      syncloss_p_r <= 1'b0;
      block_p_r    <= 1'b0;
      csnew_p_r    <= 1'b0;
      cap_wen_r    <= 1'b0;
      cap_data_r   <= '0;
    end else begin
      rxs_r        <= {rxs_r[1:0], aes_rx_i};
      parity_p_r   <= 1'b0;
      invalid_p_r  <= 1'b0;
      syncloss_p_r <= 1'b0;
      block_p_r    <= 1'b0;
      csnew_p_r    <= 1'b0;
      cap_wen_r    <= 1'b0;

      // ---- edge-interval measurement -----------------------------------
      if (edge_w)          ecnt_r <= {{(RUN_W_P-1){1'b0}}, 1'b1};
      else if (!estall_w)  ecnt_r <= ecnt_r + 1'b1;

      if (estall_w && !edge_w) begin
        // ---- dead line: fall all the way back to acquisition ------------
        if (locked_r) syncloss_p_r <= 1'b1;
        locked_r <= 1'b0;
        clean_r  <= '0;
        st_r     <= HUNT_S;
        hmin_r   <= '1;
        hcnt_r   <= '0;
        half_r   <= 1'b0;
        have_a_r <= 1'b0;
        sawz_r   <= 1'b0;
      end else if (edge_w) begin
        //! the UI estimate tracks every clean 1-UI run once acquired
        if ((st_r != HUNT_S) && (cls_w == CL_1UI_C)) ui_r <= ui_blend_w;

        unique case (st_r)
          // ---- acquire the unit interval --------------------------------
          HUNT_S: begin
            //! run 0 is a PARTIAL interval (we started mid-cell) - measuring
            //! it would drag the estimate below 1 UI and poison every
            //! threshold, so it is counted and discarded.
            if ((hcnt_r != '0) && (ecnt_r < hmin_r)) hmin_r <= ecnt_r;
            hcnt_r <= hcnt_r + 1'b1;
            if (32'(hcnt_r) == HUNT_RUNS_P - 1) begin
              ui_r <= (ecnt_r < hmin_r) ? ecnt_r : hmin_r;
              st_r <= SYNC_S;
            end
          end

          // ---- hunt the illegal 3-UI run that opens every preamble -------
          SYNC_S: begin
            if (cls_w == CL_3UI_C) begin
              st_r   <= PRE_S;
              pidx_r <= 2'd1;
            end
          end

          // ---- the three runs that name and verify the preamble ----------
          PRE_S: begin
            if (!pre_ok_w) begin
              st_r <= SYNC_S;
            end else begin
              if (pidx_r == 2'd1) begin
                ptype_r <= cls_w;
                pr2_r   <= cls_w;
              end
              pidx_r <= pidx_r + 1'b1;
              if (pidx_r == 2'd3) begin
                //! preamble complete: 4 cells consumed, data starts next run
                st_r   <= DATA_S;
                half_r <= 1'b0;
                cell_r <= '0;
                sub_r  <= '0;
              end
            end
          end

          // ---- 28 data cells, LSB first ----------------------------------
          DATA_S: begin
            if (data_bad_w) begin
              //! a 3-UI run here means a preamble arrived early - keep it
              half_r <= 1'b0;
              pidx_r <= 2'd1;
              st_r   <= (cls_w == CL_3UI_C) ? PRE_S : SYNC_S;
            end else if (!cell_done_w) begin
              half_r <= 1'b1;
            end else begin
              half_r          <= 1'b0;
              sub_r[cell_idx_w] <= cell_bit_w;
              if (32'(cell_r) == SUB_CELLS_C - 1) st_r   <= SYNC_S;
              else                                cell_r <= cell_r + 1'b1;
            end
          end
          default: st_r <= HUNT_S;
        endcase

        // ---- preamble completion: block / frame bookkeeping --------------
        if (pre_end_w) begin
          if (ptype_r == PRE_Z_C) begin
            block_p_r <= 1'b1;
            sawz_r    <= 1'b1;
            if (sawz_r) begin
              //! the block that just ENDED is complete: publish + judge it
              cssnap_r  <= csacc_r;
              csnew_p_r <= 1'b1;
              if (blkclean_r) begin
                if (32'(clean_r) < LOCK_BLOCKS_P) clean_r <= clean_r + 1'b1;
                if (32'(clean_r) + 1 >= LOCK_BLOCKS_P) locked_r <= 1'b1;
              end else begin
                clean_r <= '0;
              end
            end
            blkclean_r <= 1'b1;
            csacc_r    <= '0;
            fidx_r     <= '0;
            have_a_r   <= 1'b0;
          end else if (ptype_r == PRE_X_C) begin
            fidx_r   <= (32'(fidx_r) == BLOCK_FRAMES_C - 1)
                        ? 8'd0 : fidx_r + 1'b1;
            have_a_r <= 1'b0;
          end
        end

        // ---- subframe completion (the edge its last cell lands on) -------
        if (sub_end_w) begin
          if (sub_r[28]) invalid_p_r <= 1'b1;
          if (par_bad_w) parity_p_r  <= 1'b1;
          if (ptype_r == PRE_Y_C) begin
            //! subframe B closes the frame
            if (have_a_r && locked_r && !cap_full_w && !par_bad_w) begin
              cap_wen_r  <= 1'b1;
              cap_data_r <= {lhold_r, smp_w};
            end
            have_a_r <= 1'b0;
          end else begin
            lhold_r  <= smp_w;
            have_a_r <= 1'b1;
            if (32'(fidx_r) < CS_SNAP_BITS_C) csacc_r[fidx_r[4:0]] <= sub_r[30];
          end
        end

        // ---- ONE place decides what an error costs ----------------------
        if (err_w) begin
          if (locked_r) syncloss_p_r <= 1'b1;
          locked_r   <= 1'b0;
          clean_r    <= '0;
          blkclean_r <= 1'b0;
          have_a_r   <= 1'b0;
        end
      end
    end
  end : t_recover

  // ======================================================================
  //  pairs into the datapath clock (gray-pointer CDC, family discipline)
  // ======================================================================
  wire        cap_rempty_w;
  wire [47:0] cap_pair_w;
  logic       cap_ren_r;
  cdc_pair_fifo #(.WIDTH(48), .LOG2D(3)) u_acdc (
    .wclk_i  (clk_audio_i),
    .wrst_n  (arst_n_w),
    .wen_i   (cap_wen_r),
    .wdata_i (cap_data_r),
    .wfull_o (cap_full_w),
    .rclk_i  (clk_i),
    .rrst_n  (rst_n),
    .ren_i   (cap_ren_r),
    .rdata_o (cap_pair_w),
    .rempty_o(cap_rempty_w)
  );

  //! clk_i side: pop one pair at a time; pair_valid pulses per pop (the
  //! KL_tdm_capture pop discipline verbatim - rdata_o holds until the next
  //! ren, so the outputs may alias it).
  always_ff @(posedge clk_i) begin : t_pop
    if (!rst_n) begin
      pair_valid_o     <= 1'b0;
      cap_ren_r        <= 1'b0;
      pairs_captured_o <= '0;
    end else begin
      pair_valid_o <= cap_ren_r;
      cap_ren_r    <= !cap_rempty_w && !cap_ren_r && !pair_valid_o;
      if (pair_valid_o) pairs_captured_o <= pairs_captured_o + 1'b1;
    end
  end : t_pop

  always_comb begin : t_pair_out
    pair_slot_o = 4'd0;
    pair_l_o    = cap_pair_w[47:24];
    pair_r_o    = cap_pair_w[23:0];
  end : t_pair_out

  // ======================================================================
  //  census + channel status in clk_i
  // ======================================================================
  wire par_p_w, inv_p_w, los_p_w, blk_p_w, csn_p_w;
  cdc_pulse u_p_par (.src_clk(clk_audio_i), .src_rst_n(arst_n_w),
                     .src_pulse(parity_p_r), .dest_clk(clk_i),
                     .dest_rst_n(rst_n), .dest_pulse(par_p_w));
  cdc_pulse u_p_inv (.src_clk(clk_audio_i), .src_rst_n(arst_n_w),
                     .src_pulse(invalid_p_r), .dest_clk(clk_i),
                     .dest_rst_n(rst_n), .dest_pulse(inv_p_w));
  cdc_pulse u_p_los (.src_clk(clk_audio_i), .src_rst_n(arst_n_w),
                     .src_pulse(syncloss_p_r), .dest_clk(clk_i),
                     .dest_rst_n(rst_n), .dest_pulse(los_p_w));
  cdc_pulse u_p_blk (.src_clk(clk_audio_i), .src_rst_n(arst_n_w),
                     .src_pulse(block_p_r), .dest_clk(clk_i),
                     .dest_rst_n(rst_n), .dest_pulse(blk_p_w));
  cdc_pulse u_p_csn (.src_clk(clk_audio_i), .src_rst_n(arst_n_w),
                     .src_pulse(csnew_p_r), .dest_clk(clk_i),
                     .dest_rst_n(rst_n), .dest_pulse(csn_p_w));

  //! locked_r is a LEVEL: a plain 2-FF synchroniser is the whole contract
  logic [1:0] lock_s_r;

  always_ff @(posedge clk_i) begin : t_census
    if (!rst_n) begin
      lock_s_r     <= '0;
      blocks_o     <= '0;
      parity_err_o <= '0;
      invalid_o    <= '0;
      sync_loss_o  <= '0;
      cs_valid_o   <= 1'b0;
      cs_bits_o    <= '0;
    end else begin
      lock_s_r <= {lock_s_r[0], locked_r};
      if (blk_p_w && !(&blocks_o))     blocks_o     <= blocks_o + 1'b1;
      if (par_p_w && !(&parity_err_o)) parity_err_o <= parity_err_o + 1'b1;
      if (inv_p_w && !(&invalid_o))    invalid_o    <= invalid_o + 1'b1;
      if (los_p_w && !(&sync_loss_o))  sync_loss_o  <= sync_loss_o + 1'b1;
      //! cssnap_r is written one block (>= 4 ms) before its pulse arrives and
      //! holds until the next block boundary - sampling it here is safe.
      if (csn_p_w) begin
        cs_bits_o  <= cssnap_r;
        cs_valid_o <= 1'b1;
      end
    end
  end : t_census

  assign locked_o = lock_s_r[1];

  //! the ONLY thing CONSUMER_P changes: how the snapshot is read
  always_comb begin : t_cs_decode
    cs_pro_o      = cs_bits_o[0];
    cs_mismatch_o = cs_valid_o && (cs_bits_o[0] == CONSUMER_P);
    if (CONSUMER_P) begin
      cs_emphasis_o = cs_bits_o[5:3];             //! IEC 60958-3 byte0[5:3]
      cs_fs_code_o  = cs_bits_o[27:24];           //! IEC 60958-3 byte3[3:0]
    end else begin
      cs_emphasis_o = cs_bits_o[4:2];             //! AES3-2009 byte0[4:2]
      cs_fs_code_o  = {2'b00, cs_bits_o[7:6]};    //! AES3-2009 byte0[7:6]
    end
  end : t_cs_decode

endmodule

`default_nettype wire
