/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_media_domain_event.sv
  Description : The clock domain's own media event (#632, #764): the instant,
                in gPTP nanoseconds, at which each frame of the domain's
                frame grid starts at the media interface.

                WHY ONE EVENT. Several media interfaces may share one media
                clock (Milan v1.2 CLOCK_DOMAIN: one domain, one clock source,
                any number of streams and interfaces). The servo that phases
                the domain to a followed CRF stream is its single master, so
                it needs one defined point of the media-clock chain to
                compare the CRF timing points against, never a particular
                interface's pins. Every interface of the domain frames on the
                grid this event marks; each carries its own derived in and out
                constants relative to it (docs/design/MEDIA_CLOCK_FOLLOWING.md,
                Phase alignment). The same instant stamps the domain's
                outputs: KL_crf_tx counts 96 of these events per PDU, and the
                AAF talkers stamp the frame they capture with it (mark_ns_o,
                carried through KL_chan_map_capture's frame and walk banks
                with the frame itself), so both
                outputs fall on whole periods of one grid (IEEE 1722-2016
                4.3.5) and on the followed stream's timing points once the
                servo holds the phase (10.8 Eq. 15).

                WHAT IT OBSERVES. The domain's frame-timing owner closes each
                frame with a marker in this clock domain: the strobe of the
                frame's last pair (the same marker KL_media_grid_align
                follows). The marker comes MARK_LAT_NS_P after the instant the
                frame started at the pins: one frame span (1/fs exactly) plus
                the owner's own capture and crossing pipeline, which the
                integration derives from that front-end's parameters. The
                event is the marker's gPTP time back-dated by that latency.
                Sub-nanosecond terms round to the nearest ns, five orders of
                magnitude below the +/-5 % of Ps (1,042 ns at 48 kHz) the
                instant has to meet.

                LIVENESS. live_o falls when no marker arrives for
                TIMEOUT_CYC_P cycles (a dead or absent frame grid). The
                domain then has no physical grid to phase, and the servo
                holds its phase term off; the packet-grid tick (alt_i)
                stands in for the event, stamped with the live PHC, so the
                domain's outputs keep one grid between them.

  Spec refs   : Milan v1.2 7.6.1; IEEE 1722-2016 4.3.5, 10.7 Eq. 14, 10.8
                Eq. 15
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/

`default_nettype none

module KL_media_domain_event #(
  //! frame start at the pins -> the owner's frame marker, ns (derived by the
  //! integration from the front-end: frame span + capture + crossing)
  parameter int unsigned MARK_LAT_NS_P = 20_833,
  //! cycles without a marker that read the grid dead (4 frames, say)
  parameter int unsigned TIMEOUT_CYC_P = 4_167
)(
  input  wire         clk_i,       //! datapath clock (the PHC's)
  input  wire         rst_n,       //! active-low synchronous reset
  input  wire         mark_i,      //! the frame-timing owner's frame marker
  input  wire         alt_i,       //! the packet-grid tick: the event while not live
  input  wire  [63:0] ptp_now_i,   //! live PHC nanoseconds
  output logic        ev_p_o,      //! one cycle per frame, one cycle after mark_i
  output logic [63:0] ev_ns_o,     //! that frame's start at the pins, gPTP ns
  //! the start of the frame a marker on THIS cycle closes: ptp_now_i
  //! back-dated, combinational, for a consumer that banks the frame on the
  //! marker's own edge (KL_chan_map_capture's frame bank). ev_ns_o is this
  //! value registered, so the back-dating is derived once.
  output wire  [63:0] mark_ns_o,
  output logic        live_o       //! a marker within TIMEOUT_CYC_P cycles
);

  localparam int unsigned TOW_C = $clog2(TIMEOUT_CYC_P + 1);
  logic [TOW_C-1:0] quiet_r;

  assign mark_ns_o = ptp_now_i - 64'(MARK_LAT_NS_P);

  always_ff @(posedge clk_i) begin : domain_event
    if (!rst_n) begin
      ev_p_o  <= 1'b0;
      ev_ns_o <= '0;
      live_o  <= 1'b0;
      quiet_r <= '0;
    end else begin
      ev_p_o <= mark_i || (alt_i && !live_o);
      if (mark_i) begin
        ev_ns_o <= mark_ns_o;
        quiet_r <= '0;
        live_o  <= 1'b1;
      end else begin
        if (alt_i && !live_o) ev_ns_o <= ptp_now_i;
        if (quiet_r == TOW_C'(TIMEOUT_CYC_P)) live_o <= 1'b0;
        else                                  quiet_r <= quiet_r + 1'b1;
      end
    end
  end : domain_event

endmodule

`default_nettype wire
