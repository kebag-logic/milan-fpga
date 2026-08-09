/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_i2s_feed_mux.sv
  Author      : Kebag Logic

  Date        : 2026-07-26
  Description : DAC feed selector - the single link that decides WHAT and at
                WHAT RATE KL_i2s_playback's producer side is fed, and the
                only place the render/playback chain is counted.

                Two mutually exclusive sources:

                LEGACY TAP (sel_render_i = 0, reset default): the listener
                render tap (KL_pcm_route render_tdata + the ring handshake)
                exactly as the deployed compliance path wires it - tdata / tvalid /
                tready / tlast / wire_chans pass through COMBINATIONALLY and
                bit-identically, and the KL_pcm_lpf override is forwarded
                untouched. Zero added latency, zero behavioural delta.

                RENDER CROSSBAR (sel_render_i = 1): KL_chan_map_render's
                phys{0,1} pair, paced by phys_valid_i - ONE media frame per
                48 kHz tick. This is the path that carries the host PLAYBACK
                ring (KL_pcm_tx -> render map src = PB) to the line-out.

                WHY THE PACE MOVES WITH THE SOURCE (two defects this module
                closes, both of which made the crossbar's DAC path unusable
                for playback):
                  1. The legacy feed's valid is the RX depacketizer's
                     ACCEPTED BEAT and its walker stride is the LISTENER's
                     wire channel count. Driving the crossbar's output from
                     those means (a) the DAC does not advance at all unless
                     an inbound AVB stream is arriving - a host-ring playback
                     into a silent network is silent forever - and (b) the
                     stereo crossbar frame gets re-strided by an unrelated
                     stream's channel count: at an odd C the walker pushes
                     {lhold, s0}, i.e. it emits phys1 as LEFT and phys0 as
                     RIGHT, a hard channel swap that follows the listener,
                     not the render map. The crossbar already emits exactly
                     one stereo frame per media tick; that is the correct and
                     only pace and stride for it.
                  2. KL_i2s_playback's walker gives the LPF source ABSOLUTE
                     priority (lpf_active_i wins over the AXIS tap), and
                     KL_pcm_lpf is active whenever LPF_CTRL[0]=1 and the
                     bound stream is 2-channel - the shipped default. So with
                     the crossbar selected, the mapped samples were silently
                     discarded and the raw RX tap played instead. The LPF
                     belongs to the LISTENER tap it filters, so it is masked
                     off in render mode here rather than at its own enable
                     (LPF_CTRL keeps its meaning for the compliance path).

                HONEST REPORTING: feeds_o counts every frame handed to the
                producer on the LIVE source (legacy: accepted tap beats;
                render: media ticks) - a stuck count is the "chain is dead"
                evidence. unarmed_o saturates on render-mode frames delivered
                while NO physical DAC channel is armed in the map, which is
                the difference between "the crossbar is disarmed" and "the
                crossbar is armed and the audio is genuinely silent" - both
                render 24'd0, only one is a configuration error.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! DAC feed selector: legacy listener render tap (handshake-paced, LPF
//! override honoured, bit-identical pass-through) vs the chmap render
//! crossbar phys{0,1} pair (media-tick paced, LPF masked) - plus the
//! delivered-frame and disarmed-render counters the chain is read by.

`default_nettype none

module KL_i2s_feed_mux (
  input  wire         clk_i,          //! datapath clock
  input  wire         rst_n,          //! active-low synchronous reset

  //! --- source select (CHMAP_CTRL 0x900[0]) --------------------------------
  input  wire         sel_render_i,   //! 0 = legacy tap, 1 = render crossbar

  //! --- legacy listener render tap (KL_pcm_route + the ring handshake) -----
  input  wire [63:0]  tap_tdata_i,    //! S32BE payload beat (2 samples)
  input  wire         tap_tvalid_i,
  input  wire         tap_tready_i,   //! the ring sink's ready (shared)
  input  wire         tap_tlast_i,
  input  wire [7:0]   tap_chans_i,    //! wire-truth channels/frame (0 -> 2)
  input  wire         lpf_active_i,   //! KL_pcm_lpf engaged on the tap

  //! --- chmap render crossbar (KL_chan_map_render phys{0,1}) ---------------
  input  wire [23:0]  phys_l_i,       //! phys channel 0 sample (top 24 bits)
  input  wire [23:0]  phys_r_i,       //! phys channel 1 sample
  input  wire         phys_valid_i,   //! one pulse per 48 kHz media frame
  input  wire         phys_armed_i,   //! phys{0,1} map entries: any EN set

  //! --- producer feed into KL_i2s_playback ---------------------------------
  output logic [63:0] pcm_tdata_o,
  output logic        pcm_tvalid_o,
  output logic        pcm_tready_o,
  output logic        pcm_tlast_o,
  output logic [7:0]  chans_o,        //! walker stride (render mode = 2)
  output logic        lpf_active_o,   //! LPF override, masked in render mode

  //! --- observability (CSR PBK_STAT 0x8C8) ---------------------------------
  output logic [31:0] feeds_o,        //! frames handed to the producer (wraps)
  output logic [15:0] unarmed_o,      //! render frames with no armed phys
                                      //! channel (saturates at 0xFFFF)
  output logic        src_render_o    //! 1 = the crossbar is the live source
);

  //! phys{0,1} repacked into the depacketizer's S32BE beat order: wire byte
  //! first in lane 0, 24-in-32 left-justified so the pad byte (lanes 3/7) is
  //! zero - byte-identical to what KL_aaf_rx_depacketizer emits, which is
  //! what KL_i2s_playback's walker de-interleaves.
  wire [63:0] phys_beat_w = {
    8'h00, phys_r_i[7:0], phys_r_i[15:8], phys_r_i[23:16],
    8'h00, phys_l_i[7:0], phys_l_i[15:8], phys_l_i[23:16] };

  assign src_render_o = sel_render_i;

  // ------------------------------------------------------------------ //
  // Source mux: combinational, so sel_render_i = 0 is cycle- AND bit-    //
  // identical to the direct wiring it replaces                          //
  // ------------------------------------------------------------------ //
  always_comb begin : feed_sel
    if (sel_render_i) begin
      pcm_tdata_o  = phys_beat_w;
      pcm_tvalid_o = phys_valid_i;
      pcm_tready_o = 1'b1;            //! the tick is a strobe, not a handshake
      pcm_tlast_o  = 1'b1;            //! one whole frame per tick
      chans_o      = 8'd2;            //! the crossbar always renders a pair
      lpf_active_o = 1'b0;            //! see header defect 2
    end
    else begin
      pcm_tdata_o  = tap_tdata_i;
      pcm_tvalid_o = tap_tvalid_i;
      pcm_tready_o = tap_tready_i;
      pcm_tlast_o  = tap_tlast_i;
      chans_o      = tap_chans_i;
      lpf_active_o = lpf_active_i;
    end
  end : feed_sel

  //! a frame is DELIVERED when the live source's producer-side push fires:
  //! the LPF-driven pushes ride the same tap handshake, so the accepted-beat
  //! strobe is the honest event on both sources
  wire feed_p_w = sel_render_i ? phys_valid_i
                               : (tap_tvalid_i && tap_tready_i);

  always_ff @(posedge clk_i) begin : feed_counters
    if (!rst_n) begin
      feeds_o   <= 32'd0;
      unarmed_o <= 16'd0;
    end
    else begin
      if (feed_p_w) feeds_o <= feeds_o + 32'd1;
      //! disarmed-render evidence: the crossbar ticked, the DAC got a frame,
      //! and NO map entry backs phys{0,1} - the frame is guaranteed silence
      if (feed_p_w && sel_render_i && !phys_armed_i)
        unarmed_o <= (&unarmed_o) ? unarmed_o : unarmed_o + 16'd1;
    end
  end : feed_counters

endmodule

`default_nettype wire
