/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_pcm_lpf.sv
  Description : 2nd-order IIR low-pass (Butterworth fc 20 kHz @ fs 48 kHz)
                on the DAC render tap - band-limits the analog output that
                the signal the loop ADC receives. Serial-MAC engine: ONE
                shared signed 17x24 multiplier sequenced over the 10 biquad
                terms (5 per channel), so the logic cone fits the 100 MHz
                AX datapath clock (the v1 fully-combinational cone was
                WNS -4.7 there; 2022 failing endpoints). Latency ~12 clk
                cycles per stereo pair - absorbed by the playback FIFO,
                inaudible (0.12 us @100 MHz vs the 20.8 us sample period).

                Passive AXIS tap: captures the (tdata, tvalid&tready) beats
                of the 2ch PCM stream into a small burst FIFO (AAF PDUs
                deliver 6 back-to-back beats every 125 us; drain ~72 cycles),
                emits filtered pairs on m_tvalid. active_o tells the
                consumer (KL_i2s_playback) to capture on m_tvalid/m_tdata
                instead of the raw AXIS handshake; when inactive (disabled
                or chans != 2) the raw path is used and this engine only
                keeps its history primed so an enable edge does not thump.

                Coefficients Q2.14, exact unity DC after rounding:
                b = {11294, 22587, 11294}, a = {16384, 20966, 7825}.
                Direct Form I, s24 audio, 44-bit accumulator, round half
                up (>>14), saturate to s24.

  Spec refs   : audio quality item (user 2026-07-20); AAF S32BE lane
                layout per KL_aaf_rx_depacketizer / KL_i2s_playback
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

module KL_pcm_lpf (
    input  wire        clk_i,
    input  wire        rst_n,
    input  wire        enable_i,        //! LPF_CTRL[0]
    input  wire [9:0]  chans_i,         //! bound stream channels (2 = engage)
    //! passive tap on the depacketized PCM AXIS stream
    input  wire [63:0] s_tdata,
    input  wire        s_tvalid,
    input  wire        s_tready,        //! the DMA consumer's ready (observed)
    //! filtered pair stream (consumer captures on m_tvalid when active_o)
    output logic [63:0] m_tdata,
    output logic        m_tvalid,
    output wire         active_o
);

  //! Q2.14 Butterworth fc=20k fs=48k; b0+b1+b2 == 16384+a1+a2 (DC unity)
  localparam logic signed [16:0] B0_C = 17'sd11294;
  localparam logic signed [16:0] B1_C = 17'sd22587;
  localparam logic signed [16:0] B2_C = 17'sd11294;
  localparam logic signed [16:0] A1_C = 17'sd20966;
  localparam logic signed [16:0] A2_C = 17'sd7825;

  wire beat_acc = s_tvalid & s_tready;
  assign active_o = enable_i && (chans_i == 10'd2);

  //! S32BE unpack: wire byte 0 = lane 0 = sample MSB; audio = top 24 bits
  wire signed [23:0] xl_in = {s_tdata[7:0],   s_tdata[15:8],  s_tdata[23:16]};
  wire signed [23:0] xr_in = {s_tdata[39:32], s_tdata[47:40], s_tdata[55:48]};

  // ---- burst FIFO (8 deep: a 6-beat PDU burst fits with margin) ---------
  logic [47:0] bfifo_r [0:7];
  logic [2:0]  bwr_r, brd_r;
  logic [3:0]  bcnt_r;
  wire         bpop_w;

  // ---- per-channel Direct Form I state ----------------------------------
  logic signed [23:0] xl1_r, xl2_r, yl1_r, yl2_r;
  logic signed [23:0] xr1_r, xr2_r, yr1_r, yr2_r;

  // ---- serial MAC -------------------------------------------------------
  //! step 0..4 = L terms (b0*x, b1*x1, b2*x2, -a1*y1, -a2*y2),
  //! step 5..9 = R terms; one product added to the accumulator per cycle.
  logic [3:0]         step_r;
  logic               busy_r;
  logic signed [23:0] curl_r, curr_r;      //! popped input pair
  logic signed [43:0] acc_r;
  logic signed [23:0] yl_hold_r;

  wire signed [16:0] coef_w = (step_r == 4'd0 || step_r == 4'd5) ? B0_C
                            : (step_r == 4'd1 || step_r == 4'd6) ? B1_C
                            : (step_r == 4'd2 || step_r == 4'd7) ? B2_C
                            : (step_r == 4'd3 || step_r == 4'd8) ? A1_C
                            :                                      A2_C;
  wire signed [23:0] oper_w = (step_r == 4'd0) ? curl_r
                            : (step_r == 4'd1) ? xl1_r
                            : (step_r == 4'd2) ? xl2_r
                            : (step_r == 4'd3) ? yl1_r
                            : (step_r == 4'd4) ? yl2_r
                            : (step_r == 4'd5) ? curr_r
                            : (step_r == 4'd6) ? xr1_r
                            : (step_r == 4'd7) ? xr2_r
                            : (step_r == 4'd8) ? yr1_r
                            :                    yr2_r;
  wire               sub_w  = (step_r == 4'd3) || (step_r == 4'd4)
                           || (step_r == 4'd8) || (step_r == 4'd9);
  wire signed [40:0] prod_w = coef_w * oper_w;

  //! round half up then saturate to s24
  function automatic logic signed [23:0] sat24(input logic signed [43:0] a);
    logic signed [29:0] sh;
    begin
      sh = 30'(a >>> 14) + 30'(a[13] ? 1 : 0);
      if      (sh >  30'sd8388607)  sat24 = 24'sd8388607;
      else if (sh < -30'sd8388608)  sat24 = -24'sd8388608;
      else                          sat24 = 24'(sh);
    end
  endfunction

  wire signed [23:0] yfin_w = sat24(acc_r);        //! current-channel result

  wire ch_l_done_w = busy_r && (step_r == 4'd5);   //! acc holds the L sum
  wire pair_done_w = busy_r && (step_r == 4'd10);

  assign bpop_w = !busy_r && (bcnt_r != 4'd0);

  always_ff @(posedge clk_i or negedge rst_n) begin : engine
    if (!rst_n) begin
      bwr_r <= '0; brd_r <= '0; bcnt_r <= '0;
      step_r <= '0; busy_r <= 1'b0;
      curl_r <= '0; curr_r <= '0; acc_r <= '0; yl_hold_r <= '0;
      xl1_r <= '0; xl2_r <= '0; yl1_r <= '0; yl2_r <= '0;
      xr1_r <= '0; xr2_r <= '0; yr1_r <= '0; yr2_r <= '0;
      m_tdata <= '0; m_tvalid <= 1'b0;
    end else begin
      m_tvalid <= 1'b0;

      //! ingest beats (active mode only queues; bypass primes history
      //! directly so an enable transition does not thump). The count is
      //! kept in ONE expression covering every ingest/pop combination -
      //! the old per-branch bookkeeping leaked a phantom entry whenever a
      //! pop coincided with a skipped ingest (full FIFO, or bypass mode),
      //! walking bcnt up until the engine read permanently-full and
      //! m_tvalid stopped forever (silicon wedge class, 2026-07-21).
      //! full+pop now also ACCEPTS the beat into the freed slot.
      if (beat_acc && active_o && (bcnt_r != 4'd8 || bpop_w)) begin
        bfifo_r[bwr_r] <= {xr_in, xl_in};
        bwr_r  <= bwr_r + 3'd1;
      end
      if (beat_acc && !active_o) begin
        xl1_r <= xl_in; xl2_r <= xl1_r; yl1_r <= xl_in; yl2_r <= yl1_r;
        xr1_r <= xr_in; xr2_r <= xr1_r; yr1_r <= xr_in; yr2_r <= yr1_r;
      end
      bcnt_r <= bcnt_r
                + ((beat_acc && active_o && (bcnt_r != 4'd8 || bpop_w))
                   ? 4'd1 : 4'd0)
                - (bpop_w ? 4'd1 : 4'd0);

      //! pop -> MAC sequence
      if (bpop_w) begin
        {curr_r, curl_r} <= bfifo_r[brd_r];
        brd_r  <= brd_r + 3'd1;
        busy_r <= 1'b1;
        step_r <= 4'd0;
        acc_r  <= '0;
      end else if (busy_r) begin
        if (ch_l_done_w) begin
          yl_hold_r <= yfin_w;
          acc_r     <= 44'(sub_w ? -prod_w : prod_w);
          step_r    <= step_r + 4'd1;
        end else if (pair_done_w) begin
          //! both channels done: publish + advance history
          m_tdata  <= { 8'h00, yfin_w[7:0], yfin_w[15:8], yfin_w[23:16],
                        8'h00, yl_hold_r[7:0], yl_hold_r[15:8],
                        yl_hold_r[23:16] };
          m_tvalid <= 1'b1;
          xl1_r <= curl_r; xl2_r <= xl1_r;
          yl1_r <= yl_hold_r; yl2_r <= yl1_r;
          xr1_r <= curr_r; xr2_r <= xr1_r;
          yr1_r <= yfin_w; yr2_r <= yr1_r;
          busy_r <= 1'b0;
        end else begin
          acc_r  <= acc_r + 44'(sub_w ? -prod_w : prod_w);
          step_r <= step_r + 4'd1;
        end
      end
    end
  end : engine

endmodule

`default_nettype wire
