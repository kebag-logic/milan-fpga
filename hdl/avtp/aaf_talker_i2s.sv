/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : aaf_talker_i2s.sv
//  Project     : Milan AVTP talker (IEEE 1722-2016 AAF-PCM, Milan v1.2)
//
//  Description : MVP Milan TALKER, fabric-only (rev-2 delimitation): captures
//                stereo audio from a Digilent Pmod I2S2 ADC (CS5343, slave
//                mode — this module is the I2S clock MASTER) and emits IEEE
//                1722 AAF-PCM class-A frames, VLAN-tagged, on a 64-bit AXIS
//                master that merges into the TX datapath BEFORE the
//                classifier (PCP 3 -> class-A queue -> CBS).
//
//  Audio       : MCLK = clk/4 (12.5 MHz @ the Arty's 50 MHz datapath),
//                SCLK = MCLK/4 (64 fs), LRCK = SCLK/64 -> fs = clk/1024
//                (48.828 kHz @ 50 MHz — DECLARED 48 kHz; the +1.7 % media
//                clock offset is the accepted MVP tradeoff, a proper
//                12.288 MHz source or CRF follows). 24-bit I2S (MSB 1 SCLK
//                after the LRCK edge), samples left-justified into 32-bit
//                AAF INT32 slots (low byte 0).
//
//  Frame       : 6 samples/ch per AVTPDU (Milan class A, one frame per
//                6/48k = 125 us nominal): dst MAC (CSR, MAAP-range default)
//                + src station MAC + 802.1Q {PCP 3, VID (CSR)} + 0x22F0 +
//                AAF header (subtype 0x02, sv=1, tv=1, seq++, stream_id =
//                {station MAC, uid 0}, avtp_timestamp = PHC ns + 2 ms) +
//                2 ch x 6 x 4 B payload = 90 B on the wire, ~5.8 Mbit/s.
//
//  No CPU in the path. Enable + dest MAC come from milan_csr (0x654 group);
//  everything runs in cd_milan (single clock domain, no CDC).
//---------------------------------------------------------------------------//

`default_nettype none

module aaf_talker_i2s #(
    parameter int MCLK_DIV_LOG2 = 2   //! clk -> MCLK divide (log2): 50 MHz/4
) (
    input  wire         clk_i,
    input  wire         rst_n,
    input  wire         adv_i,             //! RETIRED (clean-clock rework): the
                                           //! I2S front-end runs in clk_audio_i
    input  wire         clk_audio_i,       //! clean MMCM audio clock (24.576 MHz)

    // ---- control (CSR 0x654 group) -------------------------------------
    input  wire         enable_i,
    input  wire [47:0]  dest_mac_i,        //! stream DMAC ([47:40] first on wire)
    input  wire [47:0]  station_mac_i,     //! src MAC; stream_id = {mac, 16'd0}
    input  wire [31:0]  transit_ns_i,      //! presentation offset added to the PHC timestamp (SET_STREAM_INFO msrp_acc_lat; reset default 2 ms)
    input  wire [11:0]  vlan_vid_i,        //! SR class VID (default 2)
    input  wire [63:0]  ptp_ns_i,          //! live PHC nanoseconds (cd_milan)
    //! pilot tone override (CSR TONE_CTRL: 1 kHz 0 dBFS test source; when
    //! set, the ADC samples are replaced by tone_smp_i on both channels)
    input  wire         tone_en_i,
    input  wire [23:0]  tone_smp_i,

    // ---- Pmod I2S2 ADC (line-in row; we are the clock master) -----------
    output wire         i2s_mclk_o,
    output wire         i2s_sclk_o,
    output wire         i2s_lrck_o,
    input  wire         i2s_sdout_i,       //! ADC serial data

    // ---- AAF frames out (64b AXIS little lane, into the TX classifier) --
    output logic [63:0] m_axis_tdata,
    output logic [7:0]  m_axis_tkeep,
    output logic        m_axis_tvalid,
    output logic        m_axis_tlast,
    input  wire         m_axis_tready,

    // ---- status (Linux-observable via CSR) --------------------------------
    output reg  [31:0]  frames_sent_o,     //! AAF frames completed on the AXIS master
    output reg  [31:0]  pairs_captured_o   //! I2S L+R sample pairs captured (liveness)
);

  localparam int SAMPLES_PER_FRAME = 6;       //! per channel (Milan 48k class A)
  localparam int FRAME_BYTES = 14 + 4 + 24 + 48;  //! eth+vlan+aaf hdr+payload = 90
  localparam int NUM_BEATS   = (FRAME_BYTES + 7) / 8;              //! 12
  localparam int LAST_KEEP   = FRAME_BYTES - (NUM_BEATS-1)*8;      //! 2

  // -----------------------------------------------------------------------
  // I2S master clocking: one free counter in cd_milan.
  //   cnt[MCLK_DIV_LOG2-1]        -> MCLK (clk/4)
  //   cnt[MCLK_DIV_LOG2+1]        -> SCLK (clk/16, 64 fs)
  //   cnt[MCLK_DIV_LOG2+7]        -> LRCK (clk/1024; 0 = LEFT half)
  // -----------------------------------------------------------------------
  //! CLEAN-CLOCK front-end (07-18): the ADC-facing I2S master clocks are
  //! plain registered dividers of clk_audio_i (24.576 MHz MMCM): MCLK /2,
  //! SCLK /8 (64 fs), LRCK /512 (48.000 kHz +-ppm). The fractional-N
  //! +-1-cycle edge jitter distorted the CS5343 exactly as it did the DAC
  //! (measured THD+N -4.5 dB from the ADC leg alone). Captured pairs cross
  //! into clk_i via a gray-pointer CDC FIFO.
  logic [1:0] tarst_n_r;                //! audio-domain reset sync
  always_ff @(posedge clk_audio_i) begin : t_audio_rst
    tarst_n_r <= {tarst_n_r[0], rst_n};
  end : t_audio_rst

  logic [8:0] tdiv_r;
  always_ff @(posedge clk_audio_i) begin : t_audio_div
    if (!tarst_n_r[1]) tdiv_r <= '0;
    else               tdiv_r <= tdiv_r + 1'b1;
  end : t_audio_div
  assign i2s_mclk_o = tdiv_r[0];
  assign i2s_sclk_o = tdiv_r[2];
  assign i2s_lrck_o = tdiv_r[8];

  //! SCLK rising edge (sample SDOUT): tdiv[2:0] wraps 011 -> 100
  wire tsclk_rise_w = (tdiv_r[2:0] == 3'b011);
  logic        tlrck_q_r;
  logic [31:0] tshift_r;
  logic [23:0] tsample_l_r;
  logic [23:0] cap_l_r, cap_r_r;
  logic        cap_wen_r;
  wire         cap_full_w;

  always_ff @(posedge clk_audio_i) begin : t_audio_cap
    if (!tarst_n_r[1]) begin
      tlrck_q_r <= 1'b0; tshift_r <= '0; tsample_l_r <= '0;
      cap_l_r <= '0; cap_r_r <= '0; cap_wen_r <= 1'b0;
    end else begin
      cap_wen_r <= 1'b0;
      if (tsclk_rise_w) begin
        if (i2s_lrck_o != tlrck_q_r) begin
          // the half that just ENDED: tlrck_q==0 -> LEFT ended
          if (!tlrck_q_r) tsample_l_r <= tone_en_i ? tone_smp_i : tshift_r[30:7];
          else begin
            //! tone: both channels carry the same sample
            cap_l_r   <= tsample_l_r;
            cap_r_r   <= tone_en_i ? tsample_l_r : tshift_r[30:7];
            cap_wen_r <= !cap_full_w;
          end
          tshift_r <= {31'd0, i2s_sdout_i};
        end else begin
          tshift_r <= {tshift_r[30:0], i2s_sdout_i};
        end
        tlrck_q_r <= i2s_lrck_o;
      end
    end
  end : t_audio_cap

  //! pairs into the datapath clock domain
  wire        cap_rempty_w;
  wire [47:0] cap_pair_w;
  logic       cap_ren_r;
  cdc_pair_fifo #(.WIDTH(48), .LOG2D(3)) u_tcdc (
    .wclk_i  (clk_audio_i),
    .wrst_n  (tarst_n_r[1]),
    .wen_i   (cap_wen_r),
    .wdata_i ({cap_l_r, cap_r_r}),
    .wfull_o (cap_full_w),
    .rclk_i  (clk_i),
    .rrst_n  (rst_n),
    .ren_i   (cap_ren_r),
    .rdata_o (cap_pair_w),
    .rempty_o(cap_rempty_w)
  );

  //! clk_i side: pop one pair at a time; pair_valid_r pulses per pop
  reg [23:0] sample_l_r, sample_r_r;
  reg        pair_valid_r;
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      sample_l_r <= '0; sample_r_r <= '0;
      pair_valid_r <= 1'b0; cap_ren_r <= 1'b0;
    end else begin
      pair_valid_r <= cap_ren_r;        //! rdata registered: valid follows ren
      if (cap_ren_r) begin
        sample_l_r <= cap_pair_w[47:24];
        sample_r_r <= cap_pair_w[23:0];
      end
      cap_ren_r <= !cap_rempty_w && !cap_ren_r && !pair_valid_r;
    end
  end

  // -----------------------------------------------------------------------
  // Sample accumulator: 6 L/R pairs per AAF frame. Timestamp latched at the
  // FIRST pair of the frame (+ max transit time).
  // -----------------------------------------------------------------------
  reg [23:0] buf_l [0:SAMPLES_PER_FRAME-1];
  reg [23:0] buf_r [0:SAMPLES_PER_FRAME-1];
  reg [2:0]  nsamp_r;
  reg [31:0] ts_r;
  reg [7:0]  seq_r;
  reg        frame_pend_r;              //! a full frame waits for the serialiser

  // -----------------------------------------------------------------------
  // Frame byte assembly (combinational over registered fields)
  // -----------------------------------------------------------------------
  logic [7:0] fb [0:NUM_BEATS*8-1];
  wire [63:0] stream_id = {station_mac_i, 16'd0};
  always_comb begin
    for (int k = 0; k < NUM_BEATS*8; k++) fb[k] = 8'h00;
    // Ethernet + 802.1Q (PCP 3, DEI 0, VID)
    {fb[0],fb[1],fb[2],fb[3],fb[4],fb[5]} = dest_mac_i;
    {fb[6],fb[7],fb[8],fb[9],fb[10],fb[11]} = station_mac_i;
    fb[12]=8'h81; fb[13]=8'h00;
    fb[14]={3'd3, 1'b0, vlan_vid_i[11:8]}; fb[15]=vlan_vid_i[7:0];
    fb[16]=8'h22; fb[17]=8'hF0;
    // AAF-PCM AVTPDU (IEEE 1722-2016 clause 7)
    fb[18]=8'h02;                       // subtype AAF
    fb[19]=8'h81;                       // sv=1, ver=0, mr=0, tv=1
    fb[20]=seq_r;                       // sequence_num
    fb[21]=8'h00;                       // reserved, tu=0
    {fb[22],fb[23],fb[24],fb[25],fb[26],fb[27],fb[28],fb[29]} = stream_id;
    {fb[30],fb[31],fb[32],fb[33]} = ts_r;                  // avtp_timestamp
    fb[34]=8'h02;                       // format = INT_32BIT
    fb[35]={4'h5, 4'h0};                // nsr = 48 kHz, rsvd
    fb[36]=8'h02;                       // channels_per_frame = 2 (10 bits w/ [35] low)
    fb[37]=8'h20;                       // bit_depth = 32
    fb[38]=8'h00; fb[39]=8'h30;         // stream_data_length = 48
    fb[40]=8'h00;                       // sp=0 (normal), evt=0
    fb[41]=8'h00;                       // reserved
    // payload: 6 x {L, R}, INT32 left-justified (sample << 8), big-endian
    for (int i = 0; i < SAMPLES_PER_FRAME; i++) begin
      fb[42+i*8+0]=buf_l[i][23:16]; fb[42+i*8+1]=buf_l[i][15:8];
      fb[42+i*8+2]=buf_l[i][7:0];   fb[42+i*8+3]=8'h00;
      fb[42+i*8+4]=buf_r[i][23:16]; fb[42+i*8+5]=buf_r[i][15:8];
      fb[42+i*8+6]=buf_r[i][7:0];   fb[42+i*8+7]=8'h00;
    end
  end

  // -----------------------------------------------------------------------
  // Serialiser (little lane): 12 beats, last keep = 2
  // -----------------------------------------------------------------------
  typedef enum logic [0:0] { IDLE_S, SEND_S } st_t;
  st_t st_r;
  reg [3:0] beat_r;
  logic [63:0] w_beat;
  always_comb
    for (int l = 0; l < 8; l++) w_beat[8*l +: 8] = fb[{28'd0, beat_r}*8 + l];

  assign m_axis_tdata  = w_beat;
  assign m_axis_tvalid = (st_r == SEND_S);
  assign m_axis_tlast  = (st_r == SEND_S) && (beat_r == NUM_BEATS-1);
  assign m_axis_tkeep  = (beat_r == NUM_BEATS-1) ? 8'((1 << LAST_KEEP) - 1) : 8'hFF;

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      st_r <= IDLE_S; beat_r <= '0; nsamp_r <= '0; seq_r <= '0;
      ts_r <= '0; frame_pend_r <= 1'b0; frames_sent_o <= '0; pairs_captured_o <= '0;
      for (int i = 0; i < SAMPLES_PER_FRAME; i++) begin
        buf_l[i] <= '0; buf_r[i] <= '0;
      end
    end else begin
      if (pair_valid_r) pairs_captured_o <= pairs_captured_o + 1'b1; //! counts even while pending (I2S is alive?)
      // accumulate pairs (drop if a frame is still pending — MVP backpressure)
      if (enable_i && pair_valid_r && !frame_pend_r) begin
        buf_l[nsamp_r] <= sample_l_r;
        buf_r[nsamp_r] <= sample_r_r;
        if (nsamp_r == 0)
          ts_r <= ptp_ns_i[31:0] + transit_ns_i;
        if (nsamp_r == SAMPLES_PER_FRAME-1) begin
          nsamp_r      <= '0;
          frame_pend_r <= 1'b1;
        end else
          nsamp_r <= nsamp_r + 1'b1;
      end
      if (!enable_i) begin
        nsamp_r <= '0; frame_pend_r <= 1'b0;
      end

      case (st_r)
        IDLE_S: if (frame_pend_r) begin beat_r <= '0; st_r <= SEND_S; end
        SEND_S: if (m_axis_tready) begin
          if (beat_r == NUM_BEATS-1) begin
            st_r <= IDLE_S; frame_pend_r <= 1'b0;
            seq_r <= seq_r + 1'b1;
            frames_sent_o <= frames_sent_o + 1'b1;
          end else
            beat_r <= beat_r + 1'b1;
        end
        default: st_r <= IDLE_S;
      endcase
    end
  end

endmodule

`default_nettype wire
