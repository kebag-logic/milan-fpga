/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_render_queue.sv
  Author      : Kebag Logic

  Date        : 2026-10-21
  Description : The listener render path's presentation stage (#632): a
                timestamp-snapped queue of media EVENTS per Stream Input,
                between the AAF RX depacketizer and the render crossbars,
                that releases every sample so it reaches its interface's
                pins at its AVTP presentation time (IEEE 1722-2016 4.3.2,
                7.5: the avtp_timestamp is the presentation time of the
                PDU's first sample, event k of the PDU k periods later). It
                replaces the #386 fill law, whose fill set the latency
                instead.

                FRAMES. The clock domain's media event (KL_media_domain_event,
                ev_p_i / ev_ns_i) counts the domain's frames: frame n starts
                at the pins at E_n = ev_ns_i, and every interface of the
                domain frames on that grid. A row of the queue is one frame
                of one stream: the event whose presentation time is nearest
                that frame's instant. Rows are indexed by frame number
                modulo ROWS_C, so a sample is WRITTEN where its timestamp
                says and nothing walks a fill.

                PUSH. At each PDU's header (hdr_p_i: the depacketizer read
                side has parsed tv and avtp_timestamp, the payload follows
                at least PAY_LEAD cycles later) the stage takes
                d = avtp_timestamp - E_n (32-bit wrap, 1722-2016 4.4.4.9)
                and divides it by Ps exactly (in thirds of a nanosecond, Ps
                = 3e9 / fs units, restoring, one quotient bit per cycle): the
                PDU's first event belongs to frame F0 = n + round(d / Ps),
                event k to F0 + k. The payload's beats are walked by the
                crossbar's position counter (wire channel = position mod the
                stream's channel count, restart at tlast) and each sample is
                written into its frame's row, lane = wire channel, with a
                valid bit. Wire channels beyond N_CH_P are walked, never
                stored.

                READ. On every domain event n each interface i reads frame
                n + K_i, K_i = IF_LEAD_P byte i: the interface's derived
                out-lead, the whole frames from the event's frame instant to
                the frame start at the interface's pins that adopts what a
                read at that event commits (KL_media_if_latency_pkg
                out_lead_frames). So every sample of frame F reaches every
                interface's pins in the frame that starts at E_F, slot k's MSB
                its slot offset later: the sample's presentation time to
                within the snapping. One event per stream is presented to
                interface i's crossbar as PAIRS_C beats in the depacketizer's
                clone format (lanes without a valid sample carry zero, tlast
                on the last beat, streams in index order), then
                render_tick_p_o[i] fires. Interfaces are read one after the
                other on the one read port.

                CONSUMED ROWS. After the reads of event n, frame
                R = n + K_min has been read by every interface: R advances to
                it and its rows are invalidated (written invalid through the
                write ports, the push first), and only then may the next
                event's reads begin. A row therefore holds either invalid or
                the one frame of the window that maps to it.

                THE RULES, per event of a PDU, against R at its write:
                  late   F <= R: every interface has presented frame F; the
                         event is dropped. A PDU with any late event counts
                         once in late_o.
                  early  F >= R + ROWS_C: beyond the queue, its row still
                         holds frame F - ROWS_C; the event is dropped. A PDU
                         with any early event counts once in early_o.
                  else   written. An interface whose read of frame F has
                         already happened presents that frame as silence.
                A PDU with tv = 0, or whose payload starts before its frame
                is known (a header without the lead), carries no
                presentation time here: not written, counted once in
                untimed_o.

                SUPPORTED RANGE. Written for every interface when, at its
                arrival, max_i(K_i) x Ps - EV_LAT_NS_P + Ps/2 < PT - now
                (one post-grid lead: the frame must be read after the sample
                arrives), and written for at least the last reader up to
                PT - now < (K_min + ROWS_C - 1.5) x Ps - EV_LAT_NS_P, which
                the depth derivation holds at or above MAX_HOLD_NS_P (Milan
                v1.2 4.4.2.1: 2.126 ms).

                SLIPS. A listener grid that does not run at the talker's
                media rate (INTERNAL, or a hold of the media clock) moves the
                timestamps across the frame instants; at a half period the
                snapping either leaves a frame without its sample (a gap: the
                read finds the row empty while the stream was presenting) or
                gives two PDUs one frame (the later sample written over the
                earlier). Both count in slips_o.

                STEP. A gPTP step moves ev_ns_i and the talker's timestamps
                together; frames already queued keep their rows (they were
                placed by the old time base, and the frame count does not
                step). A PDU stamped in one time base and placed in the other
                lands late or early and is counted there. Nothing re-centres.

                FLUSH (bind loss) and reset invalidate every row of the
                stream (a walker on the write ports' idle cycles); its writes
                are dropped and its reads present silence until the walk has
                covered it.

                STORAGE. Two banks per stage, inferred, synchronous read,
                block-RAM style, no device primitive. Word (s, row, lane)
                lives in bank lane[0] ^ row[0] at {s, row, lane >> 1}, a
                24-bit sample and its valid bit. Two consecutive wire-order
                samples always land in different banks (the next lane of the
                same row, or lane 0 of the next row after the last lane of an
                odd count), so a beat's two samples are two writes on two
                ports; a pop reads the two lanes of one pair from the two
                banks at one address.

                Single clock domain. ev_p_i arrives synchronized, and
                ev_ns_i holds its event's instant until the next event.

  Spec refs   : IEEE 1722-2016 4.3.2, 4.4.4.9, 7.5; Milan v1.2 4.4.2.1, 5.3.7.6
  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! Render presentation stage: a per-stream queue of media events indexed by
//! presentation frame (avtp_timestamp against the domain's media event), in
//! two inferred block-RAM banks; each interface reads the frame its derived
//! out-lead puts at its pins on time; late, too-early and untimed PDUs are
//! dropped and counted.

`default_nettype none

module KL_render_queue #(
  parameter int unsigned N_STREAMS_P   = 8,   //! listener streams (<= 8, the
                                              //! crossbar's map field)
  parameter int unsigned N_CH_P        = 8,   //! wire channels kept per
                                              //! event row (<= 8)
  parameter int unsigned FS_HZ_P       = 48_000, //! media rate; 3e9 / fs
                                              //! must be whole
  parameter int unsigned MAX_HOLD_NS_P = 2_126_000, //! the longest
                                              //! arrival-to-presentation
                                              //! hold the depth must keep
                                              //! (Milan v1.2 4.4.2.1)
  parameter int unsigned EV_LAT_NS_P   = 20_964, //! the domain event's pulse
                                              //! after its frame instant
                                              //! (its marker latency)
  parameter int unsigned N_IF_P        = 1,   //! interfaces read (1..4)
  parameter logic [31:0] IF_LEAD_P     = 32'h0000_0002, //! byte i: K_i,
                                              //! interface i's out-lead in
                                              //! frames (>= 1)
  parameter int unsigned PAY_LEAD_P    = 16,  //! cycles the depacketizer
                                              //! guarantees from hdr_p_i
                                              //! to the PDU's first beat
  parameter int unsigned CLK_FREQ_HZ_P = 100_000_000 //! clk_i, Hz (the
                                              //! observer's millisecond)
)(
  input  wire                      clk_i,        //! datapath clock
  input  wire                      rst_n,        //! active-low synchronous
                                                 //! reset

  //! --- PDU header (the depacketizer read side) ---------------------------
  input  wire                      hdr_p_i,      //! a PDU's tv and timestamp
                                                 //! are on the next two
                                                 //! inputs; its payload
                                                 //! follows
  input  wire [31:0]               hdr_ts_i,     //! avtp_timestamp, ns
  input  wire                      hdr_tv_i,     //! tv

  //! --- depacketizer payload clone (accepted beats, never backpressured) --
  input  wire [63:0]               s_tdata_i,    //! 2 consecutive S32BE
                                                 //! samples, wire order
  input  wire                      s_tvalid_i,   //! accepted-beat strobe
  input  wire                      s_tlast_i,    //! one AXIS frame per PDU
  input  wire [3:0]                s_tuser_i,    //! stream index s

  //! --- per-stream wire channel count (RX monitors' wire_chans_o) ---------
  input  wire [N_STREAMS_P*4-1:0]  wire_chans_i, //! 4-bit fields; 0 -> 2

  //! --- the domain's media event and the bind wipes ----------------------
  input  wire                      ev_p_i,       //! one pulse per domain frame
  input  wire [31:0]               ev_ns_i,      //! its frame's instant at the
                                                 //! pins, gPTP ns (held)
  input  wire [N_STREAMS_P-1:0]    flush_i,      //! one-cycle per stream:
                                                 //! bind loss, empty it

  //! --- to the render crossbars (KL_chan_map_render s_* and tick_i) ------
  output logic [63:0]              m_tdata_o,    //! S32BE sample pair, wire
                                                 //! order; empty lanes zero
  output logic [N_IF_P-1:0]        m_tvalid_o,   //! beat strobe, per
                                                 //! interface
  output logic                     m_tlast_o,    //! last beat of the event
  output logic [3:0]               m_tuser_o,    //! stream index s
  output logic [N_STREAMS_P*4-1:0] m_wire_chans_o, //! every stream presents
                                                 //! 2 x PAIRS_C lanes
  output logic [N_IF_P-1:0]        render_tick_p_o, //! per interface: its
                                                 //! events are in, render

  //! --- observability (#443 RENDER_STAT) ---------------------------------
  output logic [N_STREAMS_P-1:0]   pop_p_o,      //! one-cycle per stream:
                                                 //! interface 0 was handed
                                                 //! an event with a sample
  output logic [N_STREAMS_P*8-1:0] lead_o,       //! per stream: frames
                                                 //! queued past the last
                                                 //! consumed one (8-bit)
  output logic [N_STREAMS_P-1:0]   idle_o,       //! per stream: interface
                                                 //! 0's last read found no
                                                 //! sample
  output logic [N_STREAMS_P-1:0]   converged_o,  //! per stream: presenting
                                                 //! for 100 ms running
  output logic [15:0]              late_o,       //! late PDUs (saturating)
  output logic [15:0]              early_o,      //! too-early PDUs
  output logic [15:0]              untimed_o,    //! PDUs without a frame
  output logic [15:0]              slips_o       //! gaps and overlaps
);

  // ------------------------------------------------------------------ //
  // Derived shape                                                       //
  // ------------------------------------------------------------------ //
  //! Ps in thirds of a nanosecond (62,500 at 48 kHz, exact)
  localparam longint unsigned PS3_L   = 64'd3_000_000_000 / 64'(FS_HZ_P);
  localparam int unsigned     PS3_C   = 32'(PS3_L);
  //! frames the depth must span: the longest hold plus the event's own
  //! lateness, two frames for the snapping and the consumed row
  localparam longint unsigned HOLD3_L = (64'(MAX_HOLD_NS_P) + 64'(EV_LAT_NS_P)) * 64'd3;
  localparam int unsigned     SPAN_C  = 32'((HOLD3_L + PS3_L - 64'd1) / PS3_L) + 2;
  localparam int unsigned     RW_C    = $clog2(SPAN_C);       //! row bits
  localparam int unsigned     ROWS_C  = 1 << RW_C;            //! rows per stream
  localparam int unsigned     PAIRS_C = (N_CH_P + 1) / 2;     //! beats per event
  localparam int unsigned     PST_C   = 1 << $clog2(PAIRS_C); //! pair stride
  localparam int unsigned     SPAN_C2 = ROWS_C * PST_C;       //! words per stream
  localparam int unsigned     DEPTH_C = N_STREAMS_P * SPAN_C2;
  localparam int unsigned     AW_C    = $clog2(DEPTH_C);      //! bank address
  //! frame numbers: wide enough that every difference the stage takes is
  //! inside half the wrap
  localparam int unsigned     FW_C    = RW_C + 3;

  //! the interfaces' out-leads
  function automatic int unsigned if_lead(input int unsigned i);
    return 32'(IF_LEAD_P[8*i +: 8]);
  endfunction
  function automatic int unsigned lead_min();
    int unsigned m = 255;
    for (int unsigned i = 0; i < N_IF_P; i++) if (if_lead(i) < m) m = if_lead(i);
    return m;
  endfunction
  function automatic int unsigned lead_max();
    int unsigned m = 0;
    for (int unsigned i = 0; i < N_IF_P; i++) if (if_lead(i) > m) m = if_lead(i);
    return m;
  endfunction
  localparam int unsigned KMIN_C = lead_min();
  localparam int unsigned KMAX_C = lead_max();

  //! the divider: quotients above QMAX_C are early whatever their value
  localparam int unsigned     QMAX_C  = ROWS_C + KMAX_C + 1;
  localparam int unsigned     QW_C    = $clog2(QMAX_C + 1);
  localparam longint unsigned NMAX_L  = 64'(QMAX_C + 1) * PS3_L;
  localparam int unsigned     NW_C    = $clog2(NMAX_L);
  //! d at or above this rounds past QMAX_C
  localparam longint unsigned DEARLY_L = (NMAX_L - PS3_L / 2 + 64'd2) / 64'd3;
  //! the observer's period and dwell
  localparam int unsigned     MS_DIV_C     = CLK_FREQ_HZ_P / 1000;
  localparam int unsigned     CONV_DWELL_C = 100;

  // ------------------------------------------------------------------ //
  // Elaboration contract                                                //
  // ------------------------------------------------------------------ //
  if (N_STREAMS_P < 1 || N_STREAMS_P > 8) begin : g_chk_streams
    $error("KL_render_queue: N_STREAMS_P=%0d must be 1..8 (the crossbar's 3-bit stream field)", N_STREAMS_P);
  end : g_chk_streams
  if (N_CH_P < 1 || N_CH_P > 8) begin : g_chk_chans
    $error("KL_render_queue: N_CH_P=%0d must be 1..8 (the crossbar's 3-bit channel field)", N_CH_P);
  end : g_chk_chans
  if (N_IF_P < 1 || N_IF_P > 4) begin : g_chk_if
    $error("KL_render_queue: N_IF_P=%0d must be 1..4 (IF_LEAD_P carries four leads)", N_IF_P);
  end : g_chk_if
  if (KMIN_C < 1) begin : g_chk_lead
    $error("KL_render_queue: every interface's out-lead in IF_LEAD_P=%0h must be at least one frame: a read at an event cannot reach the frame that event marks", IF_LEAD_P);
  end : g_chk_lead
  if ((64'd3_000_000_000 % 64'(FS_HZ_P)) != 0) begin : g_chk_fs
    $error("KL_render_queue: FS_HZ_P=%0d does not divide 3e9, so Ps is not a whole number of thirds of a nanosecond", FS_HZ_P);
  end : g_chk_fs
  //! the guaranteed longest hold, (K_min + ROWS - 1.5) Ps - EV_LAT, covers
  //! MAX_HOLD_NS_P
  if (((64'd2 * (64'(KMIN_C) + 64'(ROWS_C)) - 64'd3) * PS3_L) < (64'd6 * (64'(MAX_HOLD_NS_P) + 64'(EV_LAT_NS_P))))
  begin : g_chk_hold
    $error("KL_render_queue: %0d rows hold less than MAX_HOLD_NS_P=%0d ns at fs=%0d with out-lead %0d", ROWS_C, MAX_HOLD_NS_P, FS_HZ_P, KMIN_C);
  end : g_chk_hold
  if (KMAX_C + 2 >= ROWS_C) begin : g_chk_window
    $error("KL_render_queue: the out-lead %0d leaves no window in %0d rows", KMAX_C, ROWS_C);
  end : g_chk_window
  if (NW_C > 31 || DEARLY_L > 64'h7FFF_FFFF) begin : g_chk_div
    $error("KL_render_queue: the divider's %0d-bit numerator does not fit the 32-bit timestamp difference", NW_C);
  end : g_chk_div
  //! the header's frame is known QW_C + 2 cycles after hdr_p_i: one to take
  //! d, one to triple it, one per quotient bit
  if (PAY_LEAD_P < QW_C + 2) begin : g_chk_lead_cyc
    $error("KL_render_queue: PAY_LEAD_P=%0d is under the %0d cycles the header's frame takes", PAY_LEAD_P, QW_C + 2);
  end : g_chk_lead_cyc
  if (CLK_FREQ_HZ_P < 2000) begin : g_chk_clk
    $error("KL_render_queue: CLK_FREQ_HZ_P=%0d cannot divide to a millisecond observer period", CLK_FREQ_HZ_P);
  end : g_chk_clk

  //! increment-with-wrap at the stream's channel count (the crossbar's own)
  function automatic logic [3:0] chwrap(input logic [3:0] ch, input logic [3:0] chans);
    chwrap = ((4'(ch + 4'd1)) == chans) ? 4'd0 : 4'(ch + 4'd1);
  endfunction

  //! word address of (stream, row, pair): the stream and row strides are
  //! powers of two, so this is a concatenation
  function automatic logic [AW_C-1:0] waddr(input logic [3:0] s,
                                            input logic [RW_C-1:0] row,
                                            input logic [3:0] pair);
    waddr = AW_C'((32'(s) * ROWS_C + 32'(row)) * PST_C + 32'(pair));
  endfunction

  // ------------------------------------------------------------------ //
  // Storage: two banks, a 24-bit sample and its valid bit per word       //
  // ------------------------------------------------------------------ //
  (* ram_style = "block" *) logic [24:0] bank0_r [DEPTH_C];
  (* ram_style = "block" *) logic [24:0] bank1_r [DEPTH_C];

  logic              we0_w, we1_w;
  logic [AW_C-1:0]   wa0_w, wa1_w, ra_w;
  logic [24:0]       wd0_w, wd1_w;
  logic [24:0]       rd0_r, rd1_r;

  always_ff @(posedge clk_i) begin : bank0_write
    if (we0_w) bank0_r[wa0_w] <= wd0_w;
  end : bank0_write
  always_ff @(posedge clk_i) begin : bank0_read
    rd0_r <= bank0_r[ra_w];
  end : bank0_read
  always_ff @(posedge clk_i) begin : bank1_write
    if (we1_w) bank1_r[wa1_w] <= wd1_w;
  end : bank1_write
  always_ff @(posedge clk_i) begin : bank1_read
    rd1_r <= bank1_r[ra_w];
  end : bank1_read

  // ------------------------------------------------------------------ //
  // Frames                                                              //
  // ------------------------------------------------------------------ //
  logic [FW_C-1:0] n_r;        //! the latest domain event's frame number
  logic [FW_C-1:0] r_r;        //! the frame every interface has consumed
  //! the frame number ev_ns_i describes this cycle (the event's pulse and
  //! its instant arrive on the same edge)
  wire  [FW_C-1:0] n_now_w = n_r + FW_C'(ev_p_i);

  always_ff @(posedge clk_i) begin : frame_count
    if (!rst_n) n_r <= '0;
    else if (ev_p_i) n_r <= n_r + 1'b1;
  end : frame_count

  // ------------------------------------------------------------------ //
  // The PDU's frame: d / Ps, one quotient bit per cycle                  //
  // ------------------------------------------------------------------ //
  typedef enum logic [2:0] {
    P_NONE_S,     //! no header since the last PDU
    P_DIV_S,      //! dividing
    P_OK_S,       //! the frame is known
    P_LATE_S,     //! the whole PDU is late
    P_EARLY_S,    //! the whole PDU is beyond the queue
    P_UNTIMED_S   //! tv = 0
  } pstate_t;
  pstate_t pst_r;

  logic [NW_C-1:0] rem_r;      //! the numerator, then the remainder
  logic [QW_C-1:0] q_r;        //! the quotient
  logic [$clog2(QW_C+1)-1:0] step_r; //! the bit being decided
  logic            tri_r;      //! rem_r still holds d, to be tripled
  logic [FW_C-1:0] f0_r;       //! the header's frame number, then F0

  wire signed [31:0] d_w      = signed'(hdr_ts_i - ev_ns_i);
  wire               d_late_w = d_w[31];
  wire               d_far_w  = !d_w[31] && (64'(unsigned'(d_w)) >= DEARLY_L);
  //! the constant of step k: Ps << k, in thirds of a nanosecond
  wire [NW_C:0]      dstep_w  = (NW_C+1)'(64'(PS3_L) << step_r);
  wire               dge_w    = ({1'b0, rem_r} >= dstep_w);

  // ------------------------------------------------------------------ //
  // Push: walk the clone, classify each sample's frame, write its lane   //
  // ------------------------------------------------------------------ //
  wire s_ok_w = s_tvalid_i && (32'(s_tuser_i) < N_STREAMS_P);

  logic [3:0] chans_in_raw_w;
  always_comb begin : in_lookup
    chans_in_raw_w = 4'd0;
    for (int unsigned s = 0; s < N_STREAMS_P; s++)
      if (32'(s_tuser_i) == s) chans_in_raw_w = wire_chans_i[s*4 +: 4];
  end : in_lookup
  wire [3:0] c_in_w = (chans_in_raw_w == 4'd0) ? 4'd2 : chans_in_raw_w;

  logic [3:0] chpos_r;         //! wire channel of the beat's first sample
  logic [2:0] k_r;             //! the event's index in the PDU
  logic       sof_r;           //! the next beat starts a PDU
  logic       pdu_ok_r;        //! this PDU's payload is placed by its frame
  logic       pdu_late_r, pdu_early_r, pdu_untimed_r, pdu_slip_r;

  //! the two samples of the beat (the crossbar's decode: wire byte first =
  //! MSB, the pad byte dropped)
  wire [23:0] smp0_w = {s_tdata_i[7:0],   s_tdata_i[15:8],  s_tdata_i[23:16]};
  wire [23:0] smp1_w = {s_tdata_i[39:32], s_tdata_i[47:40], s_tdata_i[55:48]};
  wire [3:0]  ch0_w  = sof_r ? 4'd0 : chpos_r;
  wire [3:0]  ch1_w  = chwrap(ch0_w, c_in_w);
  wire [2:0]  k0_w   = sof_r ? 3'd0 : k_r;
  wire        cmpl0_w = (ch0_w == 4'(c_in_w - 4'd1));
  wire        cmpl1_w = (ch1_w == 4'(c_in_w - 4'd1));
  wire [2:0]  k1_w   = k0_w + 3'(cmpl0_w);

  //! the PDU is placed at its first beat if its frame is known by then
  wire        place_w = sof_r ? (pst_r == P_OK_S) : pdu_ok_r;
  wire [FW_C-1:0] fr0_w = f0_r + FW_C'(k0_w);
  wire [FW_C-1:0] fr1_w = f0_r + FW_C'(k1_w);
  //! the frame against R: late at or below it, early ROWS_C or more past it
  wire [FW_C-1:0] dr0_w = fr0_w - r_r;
  wire [FW_C-1:0] dr1_w = fr1_w - r_r;
  wire        late0_w  = dr0_w[FW_C-1] || (dr0_w == '0);
  wire        late1_w  = dr1_w[FW_C-1] || (dr1_w == '0);
  wire        early0_w = !late0_w && (32'(dr0_w) >= ROWS_C);
  wire        early1_w = !late1_w && (32'(dr1_w) >= ROWS_C);

  //! the stream's flush state (declared with the walker below)
  logic [N_STREAMS_P-1:0] flpend_r;
  logic                   fl_busy_r;
  logic [3:0]             fl_s_r;
  logic                   fl_in_w;
  always_comb begin : fl_lookup
    fl_in_w = 1'b0;
    for (int unsigned s = 0; s < N_STREAMS_P; s++)
      if (32'(s_tuser_i) == s) fl_in_w = flpend_r[s] || (fl_busy_r && (32'(fl_s_r) == s));
  end : fl_lookup

  //! the PDU's verdicts so far, this beat included: a whole PDU judged at
  //! its header, or its placed samples one by one (a stored lane only)
  wire        sto0_w = place_w && (32'(ch0_w) < N_CH_P);
  wire        sto1_w = place_w && (32'(ch1_w) < N_CH_P);
  wire        b_late_w    = (sof_r ? (pst_r == P_LATE_S) : pdu_late_r) ||
                            (sto0_w && late0_w) || (sto1_w && late1_w);
  wire        b_early_w   = (sof_r ? (pst_r == P_EARLY_S) : pdu_early_r) ||
                            (sto0_w && early0_w) || (sto1_w && early1_w);
  wire        b_untimed_w = sof_r ? !((pst_r == P_OK_S) || (pst_r == P_LATE_S) || (pst_r == P_EARLY_S))
                                  : pdu_untimed_r;
  logic       b_slip_w;
  //! counted once, at the PDU's last beat
  wire        pdu_end_w   = s_ok_w && s_tlast_i;
  wire        c_late_w    = pdu_end_w && b_late_w;
  wire        c_early_w   = pdu_end_w && b_early_w;
  wire        c_untimed_w = pdu_end_w && b_untimed_w;
  wire        c_olap_w    = pdu_end_w && b_slip_w;

  wire        st0_w = s_ok_w && place_w && !fl_in_w && (32'(ch0_w) < N_CH_P)
                      && !late0_w && !early0_w;
  wire        st1_w = s_ok_w && place_w && !fl_in_w && (32'(ch1_w) < N_CH_P)
                      && !late1_w && !early1_w;
  //! the bank of each sample: lane parity xor row parity
  wire        b0_w  = ch0_w[0] ^ fr0_w[0];
  wire        b1_w  = ch1_w[0] ^ fr1_w[0];
  wire [AW_C-1:0] pa0_w = waddr(s_tuser_i, fr0_w[RW_C-1:0], {1'b0, ch0_w[3:1]});
  wire [AW_C-1:0] pa1_w = waddr(s_tuser_i, fr1_w[RW_C-1:0], {1'b0, ch1_w[3:1]});
  //! the push's bank enables: the two samples never share a bank
  wire        pw0_w = (st0_w && !b0_w) || (st1_w && !b1_w);
  wire        pw1_w = (st0_w &&  b0_w) || (st1_w &&  b1_w);

  // ------------------------------------------------------------------ //
  // Per-stream state                                                    //
  // ------------------------------------------------------------------ //
  logic [FW_C-1:0] lw_r   [N_STREAMS_P];  //! the newest frame written
  logic            lwv_r  [N_STREAMS_P];  //! lw_r is inside the window
  logic            live_r [N_STREAMS_P];  //! interface 0's last read had a
                                          //! sample
  logic [6:0]      conv_ms_r   [N_STREAMS_P];
  logic            converged_r [N_STREAMS_P];
  logic [FW_C-1:0] lead_s_w    [N_STREAMS_P];  //! lw_r - R

  logic [FW_C-1:0] lw_in_w;
  logic            lwv_in_w;
  always_comb begin : lw_lookup
    lw_in_w  = '0;
    lwv_in_w = 1'b0;
    for (int unsigned s = 0; s < N_STREAMS_P; s++)
      if (32'(s_tuser_i) == s) begin
        lw_in_w  = lw_r[s];
        lwv_in_w = lwv_r[s];
      end
  end : lw_lookup
  //! a PDU's first written event on a frame the stream already wrote: two
  //! PDUs share a frame (the later sample wins), one slip
  wire        first_ev_w = st0_w && (k0_w == 3'd0) && (ch0_w == 4'd0);
  wire [FW_C-1:0] olap_w = lw_in_w - fr0_w;
  wire        overlap_w  = first_ev_w && lwv_in_w && !olap_w[FW_C-1];
  assign b_slip_w = (!sof_r && pdu_slip_r) || overlap_w;
  //! the newest frame this beat writes
  wire [FW_C-1:0] fnew_w = st1_w ? fr1_w : fr0_w;
  wire [FW_C-1:0] lwd_w  = fnew_w - lw_in_w;
  wire        lw_adv_w   = (st0_w || st1_w) && (!lwv_in_w || (!lwd_w[FW_C-1] && (lwd_w != '0)));

  // ------------------------------------------------------------------ //
  // Read schedule: per event, each interface, each stream, each pair;    //
  // then the consumed frame's rows are invalidated                       //
  // ------------------------------------------------------------------ //
  typedef enum logic [1:0] {
    S_IDLE_S,
    S_READ_S,
    S_SCRUB_S
  } sstate_t;
  sstate_t sst_r;

  logic [FW_C-1:0] served_r;   //! the last frame number whose reads and
                               //! invalidation are done
  logic [FW_C-1:0] sn_r;       //! the event being served
  logic [1:0]      if_r;
  logic [3:0]      slot_r;
  logic [3:0]      beat_r;

  wire last_beat_w = (32'(beat_r) == PAIRS_C - 1);
  wire last_slot_w = (32'(slot_r) == N_STREAMS_P - 1);
  wire last_if_w   = (32'(if_r) == N_IF_P - 1);
  //! the frame interface if_r reads
  logic [7:0] lead_rd_w;
  always_comb begin : lead_lookup
    lead_rd_w = 8'(if_lead(0));
    for (int unsigned i = 0; i < N_IF_P; i++) if (32'(if_r) == i) lead_rd_w = 8'(if_lead(i));
  end : lead_lookup
  wire [FW_C-1:0] rd_fr_w = sn_r + FW_C'(lead_rd_w);
  //! the frame consumed by this event: the smallest lead's
  wire [FW_C-1:0] cons_w  = sn_r + FW_C'(KMIN_C);

  //! the invalidation writes both banks at one address, on a cycle the push
  //! leaves both free
  wire        both_free_w = !pw0_w && !pw1_w;
  wire        scrub_go_w  = (sst_r == S_SCRUB_S) && both_free_w;

  // the flush walker: a stream's every word, when the scrub does not need
  // the ports
  logic [$clog2(SPAN_C2)-1:0] fl_a_r; //! the stream's word being invalidated
  wire  fl_go_w   = fl_busy_r && both_free_w && !(sst_r == S_SCRUB_S);
  wire  fl_last_w = (32'(fl_a_r) == SPAN_C2 - 1);
  wire  [AW_C-1:0] fl_addr_w = AW_C'(32'(fl_s_r) * SPAN_C2 + 32'(fl_a_r));

  //! the write ports
  always_comb begin : write_ports
    we0_w = 1'b0; wa0_w = '0; wd0_w = '0;
    we1_w = 1'b0; wa1_w = '0; wd1_w = '0;
    if (pw0_w) begin
      we0_w = 1'b1;
      wa0_w = (st0_w && !b0_w) ? pa0_w : pa1_w;
      wd0_w = {1'b1, (st0_w && !b0_w) ? smp0_w : smp1_w};
    end
    if (pw1_w) begin
      we1_w = 1'b1;
      wa1_w = (st0_w && b0_w) ? pa0_w : pa1_w;
      wd1_w = {1'b1, (st0_w && b0_w) ? smp0_w : smp1_w};
    end
    if (scrub_go_w) begin
      we0_w = 1'b1; wa0_w = waddr(slot_r, cons_w[RW_C-1:0], beat_r); wd0_w = '0;
      we1_w = 1'b1; wa1_w = waddr(slot_r, cons_w[RW_C-1:0], beat_r); wd1_w = '0;
    end else if (fl_go_w) begin
      we0_w = 1'b1; wa0_w = fl_addr_w; wd0_w = '0;
      we1_w = 1'b1; wa1_w = fl_addr_w; wd1_w = '0;
    end
  end : write_ports

  //! the read port: the schedule's (slot, frame, pair)
  wire rd_go_w = (sst_r == S_READ_S);
  assign ra_w = waddr(slot_r, rd_fr_w[RW_C-1:0], beat_r);

  //! the beat being read, one cycle behind its address (the banks' read
  //! register)
  logic       rv_r;            //! a beat is on the banks' outputs
  logic [1:0] rif_r;
  logic [3:0] rs_r;
  logic       rlast_r, rlastif_r;
  logic       rodd_r;          //! its row is odd: the even lane is bank 1
  logic       rmask_r;         //! its stream is flushing: silence
  logic       rany_r;          //! a sample on an earlier beat of this event

  wire  [24:0] even_w = rodd_r ? rd1_r : rd0_r;
  wire  [24:0] odd_w  = rodd_r ? rd0_r : rd1_r;
  wire         ev_v_w = !rmask_r && even_w[24];
  wire         od_v_w = !rmask_r && odd_w[24];
  wire  [23:0] smp_e_w = ev_v_w ? even_w[23:0] : 24'd0;
  wire  [23:0] smp_o_w = od_v_w ? odd_w[23:0]  : 24'd0;
  //! this event had a sample on some beat
  wire         any_w  = rany_r || ev_v_w || od_v_w;

  assign m_tdata_o = {8'h00, smp_o_w[7:0], smp_o_w[15:8], smp_o_w[23:16],
                      8'h00, smp_e_w[7:0], smp_e_w[15:8], smp_e_w[23:16]};
  assign m_tlast_o = rlast_r;
  assign m_tuser_o = rs_r;
  always_comb begin : tvalid_fan
    for (int unsigned i = 0; i < N_IF_P; i++) m_tvalid_o[i] = rv_r && (32'(rif_r) == i);
  end : tvalid_fan

  //! the stream being read is flushing: it presents silence
  logic fl_rd_w;
  always_comb begin : fl_rd_lookup
    fl_rd_w = 1'b0;
    for (int unsigned s = 0; s < N_STREAMS_P; s++)
      if (32'(slot_r) == s) fl_rd_w = flpend_r[s] || (fl_busy_r && (32'(fl_s_r) == s));
  end : fl_rd_lookup

  always_ff @(posedge clk_i) begin : schedule
    if (!rst_n) begin
      sst_r    <= S_IDLE_S;
      served_r <= '0;
      sn_r     <= '0;
      r_r      <= FW_C'(KMIN_C);
      if_r     <= '0;
      slot_r   <= '0;
      beat_r   <= '0;
      rv_r     <= 1'b0;
      rif_r    <= '0;
      rs_r     <= '0;
      rlast_r  <= 1'b0;
      rlastif_r <= 1'b0;
      rodd_r   <= 1'b0;
      rmask_r  <= 1'b0;
      rany_r   <= 1'b0;
      render_tick_p_o <= '0;
    end else begin
      rv_r      <= rd_go_w;
      rif_r     <= if_r;
      rs_r      <= slot_r;
      rlast_r   <= rd_go_w && last_beat_w;
      rlastif_r <= rd_go_w && last_beat_w && last_slot_w;
      rodd_r    <= rd_fr_w[0];
      rmask_r   <= fl_rd_w;
      if (rv_r) rany_r <= rlast_r ? 1'b0 : any_w;
      //! an interface's render tick follows its last beat by one cycle, so
      //! its crossbar has registered that beat when it renders
      render_tick_p_o <= '0;
      for (int unsigned i = 0; i < N_IF_P; i++)
        if (rv_r && rlastif_r && (32'(rif_r) == i)) render_tick_p_o[i] <= 1'b1;

      case (sst_r)
        S_IDLE_S: begin
          //! one schedule per frame, in order: a frame is never skipped,
          //! so every consumed frame is invalidated
          if (served_r != n_r) begin
            sst_r  <= S_READ_S;
            sn_r   <= served_r + 1'b1;
            if_r   <= '0;
            slot_r <= '0;
            beat_r <= '0;
          end
        end
        S_READ_S: begin
          if (last_beat_w) begin
            beat_r <= '0;
            if (last_slot_w) begin
              slot_r <= '0;
              if (last_if_w) begin
                //! every interface has read frame sn + K_min: consumed
                sst_r <= S_SCRUB_S;
                r_r   <= cons_w;
              end else begin
                if_r <= if_r + 1'b1;
              end
            end else begin
              slot_r <= slot_r + 1'b1;
            end
          end else begin
            beat_r <= beat_r + 1'b1;
          end
        end
        S_SCRUB_S: begin
          if (scrub_go_w) begin
            if (last_beat_w) begin
              beat_r <= '0;
              if (last_slot_w) begin
                slot_r   <= '0;
                sst_r    <= S_IDLE_S;
                served_r <= sn_r;
              end else begin
                slot_r <= slot_r + 1'b1;
              end
            end else begin
              beat_r <= beat_r + 1'b1;
            end
          end
        end
        default: sst_r <= S_IDLE_S;
      endcase
    end
  end : schedule

  // ------------------------------------------------------------------ //
  // Header, divider and the PDU walk                                    //
  // ------------------------------------------------------------------ //
  always_ff @(posedge clk_i) begin : pdu_frame
    if (!rst_n) begin
      pst_r  <= P_NONE_S;
      rem_r  <= '0;
      q_r    <= '0;
      step_r <= '0;
      tri_r  <= 1'b0;
      f0_r   <= '0;
    end else begin
      if (pst_r == P_DIV_S) begin
        if (tri_r) begin
          //! N = 3 d + Ps3 / 2: round to the nearest frame
          rem_r <= NW_C'({rem_r, 1'b0} + rem_r + NW_C'(PS3_C / 2));
          tri_r <= 1'b0;
        end else begin
          if (dge_w) begin
            rem_r <= rem_r - NW_C'(dstep_w);
            q_r   <= q_r | (QW_C'(1) << step_r);
          end
          if (step_r == '0) begin
            pst_r <= P_OK_S;
            f0_r  <= f0_r + FW_C'(q_r) + FW_C'({{(QW_C-1){1'b0}}, dge_w});
          end else begin
            step_r <= step_r - 1'b1;
          end
        end
      end
      //! the PDU's first beat ends the header's claim
      if (s_ok_w && sof_r) pst_r <= P_NONE_S;
      if (hdr_p_i) begin
        q_r    <= '0;
        step_r <= ($clog2(QW_C+1))'(QW_C - 1);
        tri_r  <= 1'b1;
        f0_r   <= n_now_w;
        rem_r  <= NW_C'(unsigned'(d_w));
        pst_r  <= !hdr_tv_i ? P_UNTIMED_S
                : d_late_w  ? P_LATE_S
                : d_far_w   ? P_EARLY_S
                :             P_DIV_S;
      end
    end
  end : pdu_frame

  always_ff @(posedge clk_i) begin : walker
    if (!rst_n) begin
      chpos_r       <= 4'd0;
      k_r           <= 3'd0;
      sof_r         <= 1'b1;
      pdu_ok_r      <= 1'b0;
      pdu_late_r    <= 1'b0;
      pdu_early_r   <= 1'b0;
      pdu_untimed_r <= 1'b0;
      pdu_slip_r    <= 1'b0;
    end else if (s_ok_w) begin
      chpos_r <= chwrap(ch1_w, c_in_w);
      k_r     <= k1_w + 3'(cmpl1_w);
      sof_r   <= s_tlast_i;
      if (sof_r) pdu_ok_r <= (pst_r == P_OK_S);
      pdu_late_r    <= b_late_w;
      pdu_early_r   <= b_early_w;
      pdu_untimed_r <= b_untimed_w;
      pdu_slip_r    <= b_slip_w;
    end
  end : walker

  // ------------------------------------------------------------------ //
  // Per-stream window, presentation state, flush                        //
  // ------------------------------------------------------------------ //
  //! the lowest stream waiting for its flush walk
  logic [3:0] fl_low_w;
  always_comb begin : fl_low
    fl_low_w = 4'd0;
    for (int s = N_STREAMS_P - 1; s >= 0; s--) if (flpend_r[s]) fl_low_w = 4'(s);
  end : fl_low

  logic [$clog2(MS_DIV_C)-1:0] ms_div_r;
  wire  ms_p_w = (32'(ms_div_r) == MS_DIV_C - 1);
  //! interface 0's read of a stream completes on its last beat
  wire  rd0_end_w = rv_r && rlast_r && (rif_r == 2'd0);
  logic gap_w;

  always_ff @(posedge clk_i) begin : stream_state
    if (!rst_n) begin
      for (int unsigned s = 0; s < N_STREAMS_P; s++) begin
        lw_r[s]        <= '0;
        lwv_r[s]       <= 1'b0;
        live_r[s]      <= 1'b0;
        conv_ms_r[s]   <= 7'd0;
        converged_r[s] <= 1'b0;
      end
      //! reset is a flush of every stream: the banks carry no reset
      flpend_r  <= '1;
      fl_busy_r <= 1'b0;
      fl_s_r    <= '0;
      fl_a_r    <= '0;
      pop_p_o   <= '0;
    end else begin
      pop_p_o <= '0;
      for (int unsigned s = 0; s < N_STREAMS_P; s++) begin : per_stream
        //! a stream with nothing queued past R has no lead
        if (lwv_r[s] && (sst_r == S_SCRUB_S) && (lead_s_w[s][FW_C-1] || (lead_s_w[s] == '0)))
          lwv_r[s] <= 1'b0;
        if (lw_adv_w && (32'(s_tuser_i) == s)) begin
          lw_r[s]  <= fnew_w;
          lwv_r[s] <= 1'b1;
        end
        if (rd0_end_w && (32'(rs_r) == s)) begin
          live_r[s] <= any_w;
          if (any_w) pop_p_o[s] <= 1'b1;
          if (!any_w) begin
            conv_ms_r[s]   <= 7'd0;
            converged_r[s] <= 1'b0;
          end
        end
        if (ms_p_w && live_r[s]) begin
          if (32'(conv_ms_r[s]) != CONV_DWELL_C) conv_ms_r[s] <= conv_ms_r[s] + 7'd1;
          else                                    converged_r[s] <= 1'b1;
        end
        if (flush_i[s]) begin
          flpend_r[s]    <= 1'b1;
          lwv_r[s]       <= 1'b0;
          live_r[s]      <= 1'b0;
          conv_ms_r[s]   <= 7'd0;
          converged_r[s] <= 1'b0;
        end
      end : per_stream

      //! the walker takes the lowest pending stream, which leaves pending as
      //! its walk starts; a flush of the stream it walks re-arms it, so the
      //! walk restarts after
      if (!fl_busy_r) begin
        if (|flpend_r) begin
          fl_busy_r <= 1'b1;
          fl_s_r    <= fl_low_w;
          fl_a_r    <= '0;
          for (int unsigned s = 0; s < N_STREAMS_P; s++)
            if ((32'(fl_low_w) == s) && !flush_i[s]) flpend_r[s] <= 1'b0;
        end
      end else if (fl_go_w) begin
        fl_a_r <= fl_a_r + 1'b1;
        if (fl_last_w) fl_busy_r <= 1'b0;
      end
    end
  end : stream_state

  //! a presenting stream's read found its frame empty: one slip
  always_comb begin : gap_detect
    gap_w = 1'b0;
    for (int unsigned s = 0; s < N_STREAMS_P; s++)
      if (rd0_end_w && !any_w && (32'(rs_r) == s) && live_r[s]) gap_w = 1'b1;
  end : gap_detect

  always_ff @(posedge clk_i) begin : counters
    if (!rst_n) begin
      ms_div_r  <= '0;
      late_o    <= 16'd0;
      early_o   <= 16'd0;
      untimed_o <= 16'd0;
      slips_o   <= 16'd0;
    end else begin
      ms_div_r <= ms_p_w ? '0 : ms_div_r + 1'b1;
      if (c_late_w    && !(&late_o))    late_o    <= late_o + 16'd1;
      if (c_early_w   && !(&early_o))   early_o   <= early_o + 16'd1;
      if (c_untimed_w && !(&untimed_o)) untimed_o <= untimed_o + 16'd1;
      //! a gap and an overlap can land on one cycle
      if ((gap_w || c_olap_w) && (slips_o < 16'hFFFE))
        slips_o <= slips_o + 16'(gap_w) + 16'(c_olap_w);
      else if (gap_w || c_olap_w)
        slips_o <= 16'hFFFF;
    end
  end : counters

  // ------------------------------------------------------------------ //
  // Observability and the crossbar's channel view                       //
  // ------------------------------------------------------------------ //
  //! the pad byte of each S32BE lane is dropped by construction; a read
  //! frame's bits above the row index name its lap, which the row's
  //! invalidation already settles
  wire _unused_ok = &{1'b0, s_tdata_i[63:56], s_tdata_i[31:24], rd_fr_w[FW_C-1:RW_C], 1'b0};

  always_comb begin : taps
    for (int unsigned s = 0; s < N_STREAMS_P; s++) begin
      lead_s_w[s]              = lw_r[s] - r_r;
      lead_o[s*8 +: 8]         = !lwv_r[s] ? 8'd0
                               : (32'(lead_s_w[s]) > 255) ? 8'd255 : 8'(lead_s_w[s]);
      idle_o[s]                = !live_r[s];
      converged_o[s]           = converged_r[s];
      m_wire_chans_o[s*4 +: 4] = 4'(2 * PAIRS_C);
    end
  end : taps

endmodule

`default_nettype wire
