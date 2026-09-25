// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Receiver-to-servo integration at the production 512 ms window scale.
// The remote sample travels through the real receiver and validity wire.
`default_nettype none
module crf_talker_wrap (
  input wire frame_p_i, //! one received CRF PDU
  input wire [63:0] ts_ns_i, //! talker reference timestamp
  input wire [7:0] seq_i, //! talker sequence
  input wire tu_i, //! remote timing uncertainty
  output wire rx_locked_o, //! receiver media lock
  output wire rate_valid_o, //! receiver rate validity
  output wire signed [31:0] rate_o, //! receiver ns per 512 ms
  output wire [31:0] rx_unlocks_o, //! counted receiver unlocks
  input  wire         clk_i,          //! datapath clock (= MMCM DCLK domain)
  input  wire         rst_n,          //! active-low reset (clk_i)
  input  wire         clk_audio_i,    //! MMCM CLKOUT0 (the measured clock)
  input  wire         ps_clk_i,       //! MMCM PSCLK domain (SoC: 200 MHz idelay)

  input  wire [63:0]  ptp_now_i,      //! gPTP-synced time (ns, clk_i)
  input  wire [15:0]  clk_src_i,      //! live CLOCK_DOMAIN clock_source_index
  //! which CLOCK_SOURCE index means "the CRF stream". NOT a literal: the
  //! set is internal then CRF (1 on every shipping shape since #389 dropped
  //! the per-listener sources; it was 2 on a 1-listener shape and 9 on an
  //! 8-listener one before). The datapath feeds this from the generated
  //! AEM (AEM_CRF_CLKSRC_C); a wrong value here engages the servo on the
  //! wrong source, silently.
  input  wire [15:0]  crf_src_idx_i,

  input  wire         auto_repair_i,  //! 1 = DRP REPAIR allowed on mismatch
  input  wire         ps_invert_i,    //! flip the PS direction mapping (bench
                                      //! knob, MCSRV_CTRL 0x8FC[0]: 2026-07-23
                                      //! mf51 silicon stepped the WRONG way -
                                      //! rails 25x worse under the servo; the
                                      //! TB model bakes the UG472 sign, so
                                      //! only silicon can settle it)

  //! MMCME2_ADV DRP port (DCLK = clk_i; DS181 FDCK <= 200 MHz)
  output logic [6:0]  drp_addr_o,
  output logic        drp_en_o,       //! 1-cycle DEN (with drp_we_o for writes)
  output logic        drp_we_o,
  output logic [15:0] drp_di_o,
  input  wire  [15:0] drp_do_i,
  input  wire         drp_rdy_i,      //! DRDY completion pulse

  output logic        mmcm_rst_o,     //! MMCME2_ADV RST (held through repair)
  input  wire         mmcm_locked_i,  //! MMCME2_ADV LOCKED (async)

  //! MMCME2_ADV dynamic fine phase shift port (ps_clk_i domain, UG472)
  output logic        ps_en_o,        //! 1-PSCLK-cycle PSEN
  output logic        ps_incdec_o,    //! 1 = increment (delay = slow down)
  input  wire         ps_done_i,      //! PSDONE (12 PSCLK cycles after PSEN)

  output logic [31:0] status_o        //! A_MCSRV_STAT (0x8F8) readback
);
  KL_crf_rx rx (
    .clk_i(clk_i), .rst_n(rst_n), .frame_p_i(frame_p_i),
    .subtype_i(8'd4), .seq_i(seq_i), .sid_frame_i(64'd1),
    .pullbase_i(32'd48000), .type_i(8'd1),
    .fsh_i({16'd8, 16'd96, ts_ns_i[63:32]}),
    .fsh2_i({ts_ns_i[31:0], 32'd0}),
    .mr_i(1'b0), .tu_i(tu_i), .ptp_now_i(ptp_now_i),
    .en_i(1'b1), .sid_i(64'd1), .stop_i(1'b0),
    .rate_o(rate_o), .rate_valid_o(rate_valid_o), .locked_o(rx_locked_o),
    .cnt_unlocked_o(rx_unlocks_o),
    .delta_o(), .pdu_count_o(), .fmt_err_o(), .seq_err_o(),
    .mr_cnt_o(), .tu_cnt_o(), .late_cnt_o(), .early_cnt_o(),
    .cnt_locked_o(), .cnt_intr_o(), .dirty_p_o(), .mr_toggle_p_o()
  );
  KL_mmcm_drp_servo servo (
    .crf_locked_i(rx_locked_o), .crf_rate_i(rate_o),
    .crf_rate_valid_i(rate_valid_o), .*
  );
endmodule
`default_nettype wire
