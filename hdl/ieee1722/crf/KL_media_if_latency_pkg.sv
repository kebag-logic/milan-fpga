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
                instant its frame starts at its pins to the strobe, in the
                datapath clock, of the pair that closes the frame at the
                capture crossbar, which is when the frame is complete there
                and can be stamped. Back-dating the marker by it gives the
                frame's own instant, so the capture age (how long the frame
                waits for the media tick) and the pair offset (when each pair
                of the frame was strobed) never reach the timestamp at all.

                WHICH PAIR CLOSES. KL_chan_map_capture keeps at most four
                pairs of a bus and closes its frame on the pair of that frame
                that reaches it last (close_slot()). On a TDM bus that is the
                last pair it keeps (milan_datapath CMAP_TDM_FRAME_PAIRS_C):
                the frame's last pair up to TDM8, an INNER pair on a wider bus
                (pair 3 of 16 on TDM32, a quarter of the frame in);
                close_pair() names it, and the marker latency is counted to
                ITS last bit, never to the frame's end. On the I2S blend
                (KL_pair_blend: the I2S pair at merged slot 0, TDM pair k at
                1 + k) it is the I2S pair: KL_aaf_capture_i2s writes a pair
                when its frame ENDS, a whole frame after its instant, while
                the TDM pairs kept (TDM pairs 0..2 of TDM8) are in by three
                quarters of the frame and the next frame's first TDM pair
                comes a quarter of a frame after it. Closing on a TDM pair
                banked the I2S pair of the frame before, one sample older
                than the instant stamped on it. The blend's marker latency
                is therefore the I2S front end's (close_is_i2s()).

                THE TERMS, each from the front-end's RTL:
                  bits    pair k's last bit (slot 2k+1's LSB) is sampled
                          2 (k+1) word_bits + data_delay - 1 bit periods
                          after the frame instant (pair_end_bits): one frame
                          span (1/fs) for the last pair at a one-bit data
                          delay, one bit less at data delay 0;
                  write   the front-end registers the completed pair and
                          writes it into its crossing FIFO: wr_cyc cycles of
                          its write clock (KL_tdm_capture_master: one
                          clk_tdm_i cycle; KL_tdm_capture: one bit period;
                          KL_aaf_capture_i2s: five clk_audio_i cycles after
                          the LRCK edge; KL_pair_blend passes a TDM strobe
                          through in the same cycle);
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

  //! The TDM bus pair whose strobe closes a frame at the capture crossbar:
  //! the last of the frame_pairs it keeps
  function automatic int close_pair(input int frame_pairs);
    return frame_pairs - 1;
  endfunction

  //! The crossbar's pair slot whose strobe closes a frame: the last kept TDM
  //! pair, or on an I2S blend the I2S pair at merged slot 0, the last of its
  //! frame to arrive (see WHICH PAIR CLOSES)
  function automatic int close_slot(input int frame_pairs, input int blend);
    return (blend != 0) ? 0 : close_pair(frame_pairs);
  endfunction

  //! The closing pair is the I2S front end's: an I2S-only shape (no TDM
  //! slots) or an I2S blend
  function automatic bit close_is_i2s(input int tdm_slots, input int blend);
    return (tdm_slots == 0) || (blend != 0);
  endfunction

  //! Bit periods from the frame instant to the last bit of bus pair k (slots
  //! 2k and 2k+1 of word_bits each, data_delay bits after the sync edge)
  function automatic longint pair_end_bits(input int k, input int word_bits,
                                           input int data_delay);
    return 64'd2 * (longint'(k) + 64'd1) * longint'(word_bits) + longint'(data_delay) - 64'd1;
  endfunction

  //! A capture interface's marker latency, ns: its frame instant at the
  //! pins to the strobe, in the datapath clock, of its closing pair.
  //!   mark_bits   pair_end_bits() of the closing pair
  //!   bit_hz      the bus's bit clock (slots x word bits x fs; 64 x fs for I2S)
  //!   wr_hz       the front-end's FIFO write clock
  //!   wr_cyc      its cycles from the pair's last bit to the FIFO write
  //!   axis_hz     the datapath clock the FIFO is read in
  function automatic longint mark_lat_ns(input longint mark_bits, input longint bit_hz,
                                         input longint wr_hz, input longint wr_cyc,
                                         input longint axis_hz);
    return cyc_ns(mark_bits, bit_hz) + cyc_ns(wr_cyc, wr_hz) + half_cyc_ns(9, axis_hz);
  endfunction

  //! slot k's MSB at the pins after the frame instant, ns
  function automatic longint slot_msb_ns(input int k, input int word_bits,
                                         input int data_delay, input longint bit_hz);
    return cyc_ns(longint'(k) * longint'(word_bits) + longint'(data_delay), bit_hz);
  endfunction

  //! The read-to-adoption path of a TDM master render lane (#632), ns, read
  //! as the render queue's interface `rank` (0-based): the queue's reads of
  //! every stream for the interfaces before it and for itself, then its tick
  //! ((rank + 1) x streams x pairs + 3 datapath cycles), the crossbar's
  //! render (1) and the slot adapter's walk and commit (slots + 2), then the
  //! frame crossing into the serializer's clock and its prefetch: three
  //! serial cycles at the shortest; at the longest six, and one datapath
  //! cycle more for the crossing's phase.
  function automatic longint out_pipe_ns(input int rank, input int streams, input int pairs,
                                         input int slots, input longint axis_hz,
                                         input longint ser_hz, input bit longest);
    return cyc_ns((longint'(rank) + 64'd1) * longint'(streams) * longint'(pairs) + 64'd3 +
                  64'd1 + longint'(slots) + 64'd2 + (longest ? 64'd1 : 64'd0), axis_hz) +
           cyc_ns(longest ? 64'd6 : 64'd3, ser_hz);
  endfunction

  //! A render interface's OUT-LEAD, whole frames (#632): the domain event of
  //! frame n pulses ev_lat_ns after that frame's instant; a read at that pulse
  //! reaches the interface's serializer pipe_ns later at most, and the
  //! serializer adopts it at the next frame start at its pins, so the frame
  //! read is presented in frame n + out_lead_frames, at E_n plus that many
  //! periods. The read must therefore take the samples presented then.
  function automatic int out_lead_frames(input longint ev_lat_ns, input longint pipe_ns,
                                         input longint fs_hz);
    return int'(((ev_lat_ns + pipe_ns) * fs_hz + NS_PER_S_C - 1) / NS_PER_S_C);
  endfunction

  //! the out-lead holds for every pipeline delay from pipe_min_ns to
  //! pipe_ns: the read reaches the serializer after the frame start before
  //! the one it names and before that one, each by at least guard_ns
  function automatic bit out_lead_ok(input longint ev_lat_ns, input longint pipe_min_ns,
                                     input longint pipe_ns, input longint fs_hz,
                                     input longint guard_ns);
    longint k = longint'(out_lead_frames(ev_lat_ns, pipe_ns, fs_hz));
    return ((ev_lat_ns + pipe_min_ns - guard_ns) * fs_hz >= (k - 1) * NS_PER_S_C) &&
           ((ev_lat_ns + pipe_ns + guard_ns) * fs_hz <= k * NS_PER_S_C);
  endfunction

endpackage : KL_media_if_latency_pkg

`default_nettype wire
