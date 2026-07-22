/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_crf_rx.sv
  Description : Milan CRF Media Clock Input engine (measurement half).

                Consumes the avtp_stream_parser's per-frame pulse and
                validates Avnu Pro Audio CRF Media Clock Stream PDUs
                (Milan v1.2 7.3.2 / IEEE 1722-2016 Clause 10): subtype 4,
                type CRF_AUDIO_SAMPLE (1), pull 0, base_frequency 48000,
                timestamps_per_pdu 1 (crf_data_length 8),
                timestamp_interval 96 => 500 PDUs/s, one 64-bit gPTP-ns
                reference timestamp per PDU.

                Outputs (CSR-read, all captured per accepted PDU):
                  delta_o : crf_ts - ptp_now (signed 32) - the phase error
                            the media-clock servo daemon consumes (same
                            contract as the AAF ts_delta CSR 0x6EC).
                  rate_o  : accumulated (crf_ts[n] - crf_ts[n-256]) minus
                            nominal 256*2ms, signed ns per 512 ms window -
                            the frequency error input.
                  locked_o: PDUs arriving AND |delta jitter| within window
                            for 8 consecutive PDUs; drops after 100 ms
                            without an accepted PDU (mirrors the AAF
                            media-lock contract) or on a validation error.
                  lock/unlock event counters: CLOCK_DOMAIN GET_COUNTERS
                            LOCKED/UNLOCKED when clock_source = CRF.

                The stream to follow is selected by sid_i/en_i (CSR pair
                today, the ACMP sink-1 SM once it exists - the remaining
                CRF work is the sink-1 bind chain, see
                docs/MILAN_COMPLIANCE_GAPS.md).

  Spec refs   : Milan v1.2 7.3.2-7.3.4; IEEE 1722-2016 Clause 10
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

module KL_crf_rx #(
  parameter int CLK_FREQ_HZ_P = 50_000_000
)(
  input  wire         clk_i,
  input  wire         rst_n,

  //! per-frame capture from avtp_stream_parser (any AVTP stream frame)
  input  wire         frame_p_i,      //! parse pulse (all stream subtypes)
  input  wire [7:0]   subtype_i,
  input  wire [7:0]   seq_i,
  input  wire [63:0]  sid_frame_i,    //! frame's stream_id
  input  wire [31:0]  pullbase_i,     //! CRF: pull[31:29] | base_frequency
  input  wire [63:0]  fsh_i,          //! CRF: {dlen16, interval16, ts_hi32}
  input  wire [63:0]  fsh2_i,         //! CRF: {ts_lo32, -}
  input  wire [7:0]   type_i,         //! CRF type field (frame byte o+3)

  input  wire [63:0]  ptp_now_i,      //! gPTP-synced time (ns)

  //! CRF sink selection (CSR-provisioned; ACMP sink-1 SM later)
  input  wire         en_i,
  input  wire [63:0]  sid_i,

  //! measurement outputs (CSR)
  output logic signed [31:0] delta_o,     //! crf_ts - ptp_now @ last PDU
  output logic signed [31:0] rate_o,      //! ns error per 256-PDU window
  output logic [15:0] pdu_count_o,        //! accepted CRF PDUs (wraps)
  output logic [7:0]  fmt_err_o,          //! wrong pull/base/interval/dlen/type
  output logic [7:0]  seq_err_o,          //! sequence_num discontinuities
  output logic        locked_o,
  output logic [31:0] cnt_locked_o,       //! lock events (CLOCK_DOMAIN ctr)
  output logic [31:0] cnt_unlocked_o      //! unlock events
);

  //! Milan 7.3.2 constants
  localparam [7:0]  CRF_SUBTYPE_C  = 8'h04;
  localparam [7:0]  CRF_TYPE_AS_C  = 8'h01;   // CRF_AUDIO_SAMPLE
  localparam [28:0] CRF_BASEHZ_C   = 29'd48000;
  localparam [15:0] CRF_DLEN_C     = 16'd8;   // 1 timestamp per PDU
  localparam [15:0] CRF_IVAL_C     = 16'd96;

  //! nominal spacing: interval/base = 96/48000 s = 2 ms
  localparam logic [31:0] NOM_PDU_NS_C  = 32'd2_000_000;
  localparam int unsigned RATE_LOG2_C   = 8;   // 256-PDU rate window
  localparam logic [63:0] NOM_WIN_NS_C  = 64'(NOM_PDU_NS_C) << RATE_LOG2_C;

  //! lock: 8 clean consecutive PDUs in, 100 ms silence out (AAF contract)
  localparam int unsigned SETTLE_C   = 8;
  localparam int unsigned TOUT_CYC_C = CLK_FREQ_HZ_P / 10;

  wire w_hit = frame_p_i && en_i && (subtype_i == CRF_SUBTYPE_C)
             && (sid_frame_i == sid_i);

  wire w_fmt_ok = (type_i == CRF_TYPE_AS_C)
               && (pullbase_i[31:29] == 3'd0)
               && (pullbase_i[28:0]  == CRF_BASEHZ_C)
               && (fsh_i[63:48] == CRF_DLEN_C)
               && (fsh_i[47:32] == CRF_IVAL_C);

  wire [63:0] w_crf_ts = {fsh_i[31:0], fsh2_i[63:32]};

  logic [63:0] ts_hist_r [0:(1<<RATE_LOG2_C)-1];  //! ring of accepted ts
  logic [RATE_LOG2_C-1:0] hidx_r;
  logic [8:0]  hfill_r;                           //! saturates at 256
  logic [7:0]  exp_seq_r;
  logic        have_seq_r;
  logic [2:0]  settle_r;
  logic [$clog2(TOUT_CYC_C+1)-1:0] tout_r;

  always_ff @(posedge clk_i or negedge rst_n) begin : engine
    if (!rst_n) begin
      delta_o <= '0; rate_o <= '0;
      pdu_count_o <= '0; fmt_err_o <= '0; seq_err_o <= '0;
      locked_o <= 1'b0; cnt_locked_o <= '0; cnt_unlocked_o <= '0;
      hidx_r <= '0; hfill_r <= '0;
      exp_seq_r <= '0; have_seq_r <= 1'b0;
      settle_r <= '0; tout_r <= '0;
    end else begin
      //! lock timeout: 100 ms without an accepted PDU
      if (w_hit && w_fmt_ok) begin
        tout_r <= '0;
      end else if (tout_r == TOUT_CYC_C[$clog2(TOUT_CYC_C+1)-1:0]) begin
        if (locked_o) begin
          locked_o       <= 1'b0;
          cnt_unlocked_o <= cnt_unlocked_o + 32'd1;
        end
        settle_r <= '0;
        have_seq_r <= 1'b0;
        hfill_r  <= '0;
      end else begin
        tout_r <= tout_r + 1'b1;
      end

      if (w_hit) begin
        if (!w_fmt_ok) begin
          fmt_err_o <= (&fmt_err_o) ? fmt_err_o : fmt_err_o + 8'd1;
          //! a malformed PDU breaks the settle run
          settle_r  <= '0;
        end else begin
          pdu_count_o <= pdu_count_o + 16'd1;

          if (have_seq_r && (seq_i != exp_seq_r)) begin
            seq_err_o <= (&seq_err_o) ? seq_err_o : seq_err_o + 8'd1;
            settle_r  <= '0;
          end else if (settle_r != 3'(SETTLE_C - 1)) begin
            settle_r <= settle_r + 3'd1;
          end else if (!locked_o) begin
            locked_o     <= 1'b1;
            cnt_locked_o <= cnt_locked_o + 32'd1;
          end
          exp_seq_r  <= seq_i + 8'd1;
          have_seq_r <= 1'b1;

          delta_o <= 32'(signed'(w_crf_ts - ptp_now_i));

          //! frequency error across the 256-PDU ring (512 ms)
          ts_hist_r[hidx_r] <= w_crf_ts;
          if (hfill_r == 9'(1 << RATE_LOG2_C)) begin
            rate_o <= 32'(signed'((w_crf_ts - ts_hist_r[hidx_r])
                                  - NOM_WIN_NS_C));
          end else begin
            hfill_r <= hfill_r + 9'd1;
          end
          hidx_r <= hidx_r + 1'b1;
        end
      end
    end
  end : engine

endmodule

`default_nettype wire
