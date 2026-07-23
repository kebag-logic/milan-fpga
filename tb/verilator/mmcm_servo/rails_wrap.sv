/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : rails_wrap.sv
  Description : Rails-cease closed-loop harness top: KL_i2s_playback (the
                drift-lottery rails) + KL_mmcm_drp_servo sharing one modeled
                audio clock. The C++ harness (sim_rails.cpp) is the MMCM
                behavioral model: the audio clock period follows the PS
                steps, so with clock_source == 2 the servo pulls the render
                clock onto the talker's rate and the FIFO rail events cease;
                with clock_source == 0 the identical stimulus shows the
                historical drift-lottery rails.

                Sim-compressed servo parameters (silicon values in the
                servo defaults): 125 us tick (TICK_CYC 3072), 4 ms window
                (WIN_LOG2 5, NORM_SHIFT 7 renormalizes to the fixed
                ns/512ms CSR scale), authority 2000 ppm with 169 ps model
                steps (10x silicon: same loop math, 10x fewer PS events so
                seconds of media time simulate in CPU minutes), gains one
                notch softer (KI 2 / KP 3) for the model's +35% step-gain
                rounding.

  Spec refs   : docs/MILAN_COMPLIANCE_GAPS.md 2 (clock-recovery ACTUATOR)
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

module rails_wrap (
  input  wire         clk_i,
  input  wire         rst_n,
  input  wire         clk_audio_i,
  input  wire         ps_clk_i,

  input  wire [63:0]  ptp_now_i,
  input  wire [15:0]  clk_src_i,
  input  wire         crf_locked_i,
  input  wire signed [31:0] crf_rate_i,

  //! talker PCM feed (depacketizer tap shape)
  input  wire [63:0]  pcm_tdata_i,
  input  wire         pcm_tvalid_i,
  input  wire         pcm_tlast_i,
  input  wire [7:0]   wire_chans_i,

  //! MMCM behavioral-model boundary (C++ harness)
  output wire [6:0]   drp_addr_o,
  output wire         drp_en_o,
  output wire         drp_we_o,
  output wire [15:0]  drp_di_o,
  input  wire [15:0]  drp_do_i,
  input  wire         drp_rdy_i,
  output wire         mmcm_rst_o,
  input  wire         mmcm_locked_i,
  output wire         ps_en_o,
  output wire         ps_incdec_o,
  input  wire         ps_done_i,

  //! observability
  output wire [31:0]  status_o,
  output wire [15:0]  underruns_o,
  output wire [15:0]  overruns_o,
  output wire [15:0]  fill_o,
  output wire         i2s_sclk_o,
  output wire         i2s_lrck_o,
  output wire         i2s_sdin_o
);

  wire i2s_mclk_unused_w;
  wire signed [15:0] trim_unused_w;
  wire media_reset_unused_w, converged_unused_w;
  wire [31:0] dbg_frame_unused_w;

  KL_i2s_playback #(
    .FIFO_LOG2 (4),      //! 16-pair FIFO: rails observable in seconds
    .PREFILL_C (0)
  ) i2spb (
    .clk_i        (clk_i),
    .rst_n        (rst_n),
    .clk_audio_i  (clk_audio_i),
    .servo_en_i   (1'b0),
    .pcm_tdata_i  (pcm_tdata_i),
    .pcm_tvalid_i (pcm_tvalid_i),
    .pcm_tready_i (1'b1),
    .pcm_tlast_i  (pcm_tlast_i),
    .lpf_tdata_i  (64'd0),
    .lpf_tvalid_i (1'b0),
    .lpf_active_i (1'b0),
    .wire_chans_i (wire_chans_i),
    .i2s_mclk_o   (i2s_mclk_unused_w),
    .i2s_sclk_o   (i2s_sclk_o),
    .i2s_lrck_o   (i2s_lrck_o),
    .i2s_sdin_o   (i2s_sdin_o),
    .clr_under_i  (1'b0),
    .clr_over_i   (1'b0),
    .underruns_o  (underruns_o),
    .overruns_o   (overruns_o),
    .trim_o       (trim_unused_w),
    .fill_o       (fill_o),
    .media_reset_p_o (media_reset_unused_w),
    .converged_o  (converged_unused_w),
    .dbg_frame_o  (dbg_frame_unused_w)
  );

  KL_mmcm_drp_servo #(
    .TICK_CYC_P   (3072),          //! 125 us tick
    .WIN_LOG2_P   (5),             //! 32 ticks = 4 ms window
    .NOM_WIN_NS_P (64'd4_000_000),
    .NORM_SHIFT_P (7),             //! 4 ms -> 512 ms CSR scale
    .KI_SHIFT_P   (2),
    .KP_SHIFT_P   (3),
    .U_MAX_P      (1_024_000),     //! 2000 ppm (model steps are 10x)
    .SLEW_MAX_P   (512_000),       //! 1000 ppm / window
    .LOCK_THR_P   (8192),          //! 16 ppm: tick jitter x128 (see Makefile)
    .GAIN_NUM_P   (1),             //! 169 ps step, 125 us tick
    .RELOCK_TOUT_P(20000)
  ) servo (
    .clk_i         (clk_i),
    .rst_n         (rst_n),
    .clk_audio_i   (clk_audio_i),
    .ps_clk_i      (ps_clk_i),
    .ptp_now_i     (ptp_now_i),
    .clk_src_i     (clk_src_i),
    .crf_locked_i  (crf_locked_i),
    .crf_rate_i    (crf_rate_i),
    .auto_repair_i (1'b0),
    .ps_invert_i   (1'b0),
    .drp_addr_o    (drp_addr_o),
    .drp_en_o      (drp_en_o),
    .drp_we_o      (drp_we_o),
    .drp_di_o      (drp_di_o),
    .drp_do_i      (drp_do_i),
    .drp_rdy_i     (drp_rdy_i),
    .mmcm_rst_o    (mmcm_rst_o),
    .mmcm_locked_i (mmcm_locked_i),
    .ps_en_o       (ps_en_o),
    .ps_incdec_o   (ps_incdec_o),
    .ps_done_i     (ps_done_i),
    .status_o      (status_o)
  );

endmodule

`default_nettype wire
