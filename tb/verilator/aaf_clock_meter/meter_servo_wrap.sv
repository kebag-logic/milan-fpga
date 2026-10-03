// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : meter_servo_wrap.sv
  Description : KL_aaf_clock_meter driving KL_mmcm_drp_servo's reference
                ports, the "servo with the meter in front of it" row of
                docs/design/MEDIA_CLOCK_FOLLOWING.md's test plan (#629). The
                datapath's selection is a constant here: an AAF source is
                followed, listener 0, never stopped or rebound.

                The servo runs its SILICON loop: a 512 ms window, NOM_WIN_NS
                512 ms, NORM_SHIFT 0, the shipping PI gains and lock rule.
                Two things are scaled, neither of them loop arithmetic:
                  * TICK_CYC_P: the harness's audio clock is the shipping
                    24.576 MHz / 32, so a tick is still 1 ms of it;
                  * GAIN_NUM_P = 1 with a 1 ns model phase step (silicon:
                    59 steps of 16.9 ps), so one PS step per tick per ppm,
                    a plant gain of 1, at a 59th of the PS traffic.
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

module meter_servo_wrap #(
  parameter int unsigned CLK_HZ_P   = 1_200_000,  //! the meter's timeout basis
  parameter int unsigned TICK_CYC_P = 768         //! one 1 ms servo tick
)(
  input  wire         clk_i,
  input  wire         rst_n,
  input  wire         clk_audio_i,
  input  wire         ps_clk_i,
  input  wire [63:0]  ptp_now_i,
  //! the followed talker's PDUs (listener 0, the 48 kHz Base format)
  input  wire         match_p_i,
  input  wire [7:0]   seq_i,
  input  wire [31:0]  ts_i,
  //! MMCME2_ADV model ports
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
  //! observation
  output wire [31:0]  status_o,
  output wire         servo_locked_o,
  output wire         meter_locked_o,
  output wire         meter_rate_valid_o,
  output wire signed [31:0] meter_rate_o,
  output wire [31:0]  meter_status_o
);

  //! 6 samples x 4 octets x 8 channels: the Base format the meter consumes
  localparam logic [63:0] FSH_C = {8'h02, 4'h5, 2'b00, 10'd8, 8'd32, 16'd192, 16'd0};

  KL_aaf_clock_meter #(
    .CLK_FREQ_HZ_P (CLK_HZ_P),
    .N_LISTENERS_P (1)
  ) meter (
    .clk_i (clk_i), .rst_n (rst_n),
    .en_i (1'b1), .follow_idx_i (1'b0), .bind_rise_i (1'b0), .stopped_i (1'b0),
    .match_p_i (match_p_i), .match_idx_i (1'b0), .subtype_i (8'h02),
    .tv_i (1'b1), .tu_i (1'b0), .mr_i (1'b0), .seq_i (seq_i), .ts_ns_i (ts_i),
    .fsh_i (FSH_C),
    .locked_o (meter_locked_o), .rate_ns_o (meter_rate_o),
    .rate_valid_o (meter_rate_valid_o), .disrupt_p_o (), .mr_toggle_p_o (),
    .max_dev_ns_o (meter_status_o[31:16]), .status_o (meter_status_o[15:0])
  );

  KL_mmcm_drp_servo #(
    .CLK_FREQ_HZ_P (CLK_HZ_P),
    .TICK_CYC_P    (TICK_CYC_P),
    .GAIN_NUM_P    (1)
  ) servo (
    .clk_i (clk_i), .rst_n (rst_n), .clk_audio_i (clk_audio_i),
    .ps_clk_i (ps_clk_i), .ptp_now_i (ptp_now_i), .phc_slew_active_i (1'b0),
    .sel_i (1'b1), .ref_locked_i (meter_locked_o),
    .ref_rate_valid_i (meter_rate_valid_o), .ref_rate_ns_i (meter_rate_o),
    .auto_repair_i (1'b0), .ps_invert_i (1'b0),
    .drp_addr_o (drp_addr_o), .drp_en_o (drp_en_o), .drp_we_o (drp_we_o),
    .drp_di_o (drp_di_o), .drp_do_i (drp_do_i), .drp_rdy_i (drp_rdy_i),
    .mmcm_rst_o (mmcm_rst_o), .mmcm_locked_i (mmcm_locked_i),
    .ps_en_o (ps_en_o), .ps_incdec_o (ps_incdec_o), .ps_done_i (ps_done_i),
    .status_o (status_o), .locked_o (servo_locked_o)
  );

endmodule

`default_nettype wire
