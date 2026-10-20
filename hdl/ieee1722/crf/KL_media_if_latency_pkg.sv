/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_media_if_latency_pkg.sv
  Description : The per-interface latency constants of a media clock domain
                (#632, #764), DERIVED from each interface's own parameters in
                one place, never mirrored.

                A clock domain has one media event (KL_media_domain_event):
                the instant a frame of its grid starts at the media
                interface. Several interfaces may share the domain; each
                carries its own constants relative to that event, so every
                interface's pin instants fall on the same CRF timing points
                (IEEE 1722-2016 4.3.5; 10.8 within +/-5 % of Ps), and adding
                an interface adds its constants, never a second loop. A
                capture interface's constant is its MARKER LATENCY: from the
                instant its frame starts at its pins to the strobe of the
                frame's last pair in the datapath clock, which is when the
                frame is complete and can be stamped. Back-dating the marker
                by it gives the frame's own instant, so the capture age (how
                long the frame waits for the media tick) and the pair offset
                (when each pair of the frame was strobed) never reach the
                timestamp at all.

                THE TERMS, each from the front-end's RTL:
                  frame   the last bit of the last slot is sampled at the
                          frame span (1/fs) after the frame instant, less one
                          bit period when the slot-0 MSB rides the sync edge
                          itself (data delay 0);
                  write   the front-end registers the completed pair and
                          writes it into its crossing FIFO: wr_cyc cycles of
                          its write clock (KL_tdm_capture_master: one
                          clk_tdm_i cycle; KL_tdm_capture: one bit period;
                          KL_aaf_capture_i2s: five clk_audio_i cycles after
                          the LRCK edge);
                  read    the FIFO's read side in the datapath clock: two
                          synchroniser flops, the empty flag, the pop and the
                          valid - 4 cycles after the first edge, which waits
                          half a cycle on average: 4.5 cycles.
                Each term rounds to the nanosecond: the sum is within 1.5 ns
                of the exact rational and within one datapath cycle of any
                one frame's marker.

                The per-slot pin offset (slot k's MSB after the frame instant,
                (k x word_bits + data_delay) bit periods) is the constant a
                grader subtracts from a decoded slot-MSB pin instant to reach
                the frame instant the timestamp describes; it is here so the
                two cannot be derived twice.

  Spec refs   : IEEE 1722-2016 4.3.5, 10.8 Eq. 15; Milan v1.2 7.6.1
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/

`default_nettype none

package KL_media_if_latency_pkg;

  localparam longint NS_PER_S_C = 64'd1_000_000_000;

  //! n cycles of a clock at hz, in ns, rounded to the nearest
  function automatic longint cyc_ns(input longint n, input longint hz);
    return (n * NS_PER_S_C + hz / 2) / hz;
  endfunction

  //! half cycles of a clock at hz, in ns, rounded to the nearest
  function automatic longint half_cyc_ns(input longint halves, input longint hz);
    return (halves * NS_PER_S_C + hz) / (2 * hz);
  endfunction

  //! A capture interface's marker latency, ns: its frame instant at the
  //! pins to the strobe of its frame's last pair in the datapath clock.
  //!   fs_hz       sample rate (one frame per sample)
  //!   bit_hz      the bus's bit clock (slots x word bits x fs; 2 x fs for I2S)
  //!   data_delay  1 = slot 0's MSB one bit after the sync edge, 0 = on it
  //!   wr_hz       the front-end's FIFO write clock
  //!   wr_cyc      its cycles from the last bit to the FIFO write
  //!   axis_hz     the datapath clock the FIFO is read in
  function automatic longint mark_lat_ns(input longint fs_hz, input longint bit_hz,
                                         input int data_delay, input longint wr_hz,
                                         input longint wr_cyc, input longint axis_hz);
    longint frame_ns;
    frame_ns = cyc_ns(1, fs_hz) - ((data_delay != 0) ? 64'd0 : cyc_ns(1, bit_hz));
    return frame_ns + cyc_ns(wr_cyc, wr_hz) + half_cyc_ns(9, axis_hz);
  endfunction

  //! slot k's MSB at the pins after the frame instant, ns
  function automatic longint slot_msb_ns(input int k, input int word_bits,
                                         input int data_delay, input longint bit_hz);
    return cyc_ns(longint'(k) * longint'(word_bits) + longint'(data_delay), bit_hz);
  endfunction

endpackage : KL_media_if_latency_pkg

`default_nettype wire
