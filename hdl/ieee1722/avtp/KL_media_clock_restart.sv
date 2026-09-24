/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_media_clock_restart.sv
  Author      : Kebag Logic

  Date        : 2026-07-30
  Description : The AVTP "mr" (media clock restart) level this end station
                stamps into its outgoing Stream Data AVTPDUs, per talker.

                WHY THIS EXISTS. IEEE 1722-2016 4.4.4.3 is a shall for any
                talker whose timestamps come from a received CRF stream:

                  "If a Clock Reference Format (CRF) stream (see Clause 8) is
                   being received by a Talker, then any streams deriving
                   timestamps from the CRF stream shall toggle the mr bit if
                   a disruption of the CRF stream occurs or if the mr bit in
                   the CRF stream has been toggled."

                Until this module the AAF packetizer emitted a CONSTANT
                mr = 0 (a literal 8'h81 header byte), so a board slaved to an
                external CRF media clock told every listener "the media clock
                never restarted" straight through a CRF dropout - and the
                Milan v1.2 Table 5.4 MEDIA_RESET counter, which Table 5.17
                makes a "shall implement and return", was claimed in the
                GET_COUNTERS valid mask over an event port tied to 1'b0. One
                gap, two symptoms.

                THE TOGGLE IS A LEVEL, NOT A PULSE. 4.4.4.3: the bit "is
                toggled by the Talker each time a media clock restart is
                needed, and it stays at its new value until a new media clock
                restart is needed". So a restart request FLIPS a target level
                and the level is what gets stamped.

                THE >= 8 PDU HOLD. 4.4.4.3: "Once this bit toggles, it shall
                remain in its new state for a minimum of eight (8) AVTPDUs for
                a given continuous stream." The clause counts AVTPDUs of ONE
                stream, so the hold is per talker context, and it counts only
                PDUs that actually WENT OUT carrying the current level -
                which is why frame_mr_i (the bit the completed PDU really
                carried) qualifies the increment rather than frame_p_i alone.
                A frame already granted when the level flips still carries the
                old value; counting it toward the new value's hold would emit
                the new state for seven PDUs, not eight.

                A stream that is not streaming has no "continuous stream" to
                hold across: its hold is held satisfied so it adopts the
                current media-clock truth on its first PDU rather than
                starting life with a stale bit.

                A PENDING RESTART ABSORBS A SECOND REQUEST (#387, ruling
                5802264260 item 2). A request is pending on a stream from
                the cycle it arrives until that stream stamps the new level,
                which waits for the >= 8 PDU hold of its previous toggle. A
                second request landing in that window (a PHC step on top of
                a CRF disruption, say) asks for what the first already
                asked for, so the two merge: the stream puts exactly ONE
                toggle on the wire, and its MEDIA_RESET counts it. A request
                therefore does not flip a target; it sets the stream's
                target to the complement of the level the stream stamps now,
                which a second request cannot undo. Until #387 every request
                flipped one shared target, so a second request inside the
                hold flipped it back and NEITHER restart reached the wire. A
                request that lands after the stream has stamped the previous
                toggle is a new restart, not a merge: that stream's
                listeners have already seen the earlier toggle, so the new
                one follows once the earlier has held its eight PDUs.

                So the target is PER STREAM. Every request still reaches
                every stream, but whether it is pending is a property of one
                stream's hold: the CRF output's eight PDUs at 500/s outlast
                an AAF talker's at 8000/s, so one request can be pending on
                one stream and already stamped on the other, and a shared
                target could not both merge the first and restart the
                second. Two streams can end on opposite levels after such a
                sequence. That carries no meaning: a listener reads a
                stream's toggles, never its level against another stream's
                (10.4.3: only the mr bit of the stream a Listener recovers
                its media clock from is valid).

                THE SOURCE-CHANGE TRIGGER. 4.4.4.3's PRIMARY case is a change
                of the media clock SOURCE (its S/PDIF A->B example), and PICS
                Table F.7 AAF-5 makes it AAF:M MANDATORY. clk_src_i carries the
                live clock_source_index (SET_CLOCK_SOURCE); a change of its
                value toggles the level exactly like a disruption pulse, so
                switching internal<->CRF or between two external sources
                restarts the media clock on the wire (2026-07-30).

                THE CRF-mr-ECHO TRIGGER. 4.4.4.3's third case - "or if the mr
                bit in the CRF stream has been toggled" - arrives on
                restart_p_i beside the disruption pulse. This banner used to
                say the trigger was unimplemented "because KL_crf_rx does not
                parse it"; that stopped being true when the CRF sink started
                serving Milan Table 5.6 MEDIA_RESET off the received bit
                (AVTP-5t), and the sink now exports the same edge as a pulse
                (mr_toggle_p_o, gh #62 H2a). All three 4.4.4.3 triggers are
                wired. The integration gates the echo with clock_source ==
                CRF, which is 10.4.3's own scoping ("only the mr bit from the
                stream being used by the Listener for recovering the media
                clock is valid"), not a convenience.

                WHICH CONTEXTS. Every Stream Output the device has, and that
                includes a CRF Media Clock OUTPUT: 10.4.3 gives a CRF Talker
                the same mr duty as 4.4.4.3 gives a media-stream Talker, and
                PICS Table F.16 makes both CRF-3 (the bit) and CRF-5 (the
                >= 8 AVTPDU hold) mandatory for it. Its context index is the
                one the integration already uses for the CRF output
                everywhere else; its PDU strobe is the CRF PDU strobe and its
                frame_mr_i the bit that PDU stamped, so the hold below counts
                CRF AVTPDUs at 500/s while an AAF talker's counts its own at
                8000/s - independently, each against its own target.

  Spec refs   : IEEE 1722-2016 4.4.4.3 (+ 10.4.3 for the CRF talker side,
                PICS Table F.16 CRF-3/CRF-4/CRF-5),
                Milan v1.2 5.3.7.7 Table 5.4 MEDIA_RESET
  Company     : Kebag Logic
------------------------------------------------------------------------------
*/

//! Per-talker AVTP mr level: a restart request sets each talker's target to
//! the complement of the level it stamps, so a request landing on a pending
//! one merges with it, and each talker adopts its target once its own last
//! change has been on the wire for HOLD_PDU_P transmitted PDUs (1722-2016
//! 4.4.4.3).

`default_nettype none

module KL_media_clock_restart #(
  parameter int unsigned N_TALKERS_P = 1,   //! talker stream contexts
  //! minimum PDUs the bit must hold its new state; 8 is the clause floor and
  //! raising it is legal (the clause sets a minimum, not a value)
  parameter int unsigned HOLD_PDU_P  = 8
)(
  input  wire                    clk_i,
  input  wire                    rst_n,

  //! media-clock restart request: one cycle per restart event. The
  //! integration ORs every trigger but the source change here: a disruption
  //! of the CRF stream our media clock is slaved to, that stream's own mr
  //! toggle, and a PHC step (#387); the source-change trigger has its own
  //! clk_src_i below.
  input  wire                    restart_p_i,
  //! the live media clock SOURCE (SET_CLOCK_SOURCE / clock_source_index). A
  //! CHANGE of this value is 4.4.4.3's PRIMARY restart trigger (the clause's
  //! S/PDIF A->B example) and PICS Table F.7 AAF-5 makes it AAF:M MANDATORY -
  //! it is detected here, beside the disruption pulse, so all of 4.4.4.3
  //! lives in one place. Reset it to whatever clock_source_index resets to
  //! (0 = internal) so power-up raises no spurious restart.
  input  wire [15:0]             clk_src_i,

  //! per-talker streaming level (a stopped stream holds nothing)
  input  wire [N_TALKERS_P-1:0]  streaming_i,

  //! PDU completion feed: which talker, and the mr bit that PDU carried
  input  wire                    frame_p_i,
  input  wire [3:0]              frame_idx_i,
  input  wire                    frame_mr_i,

  //! the level to stamp, per talker
  output logic [N_TALKERS_P-1:0] mr_o
);

  if (N_TALKERS_P < 1 || N_TALKERS_P > 16)
    $error("KL_media_clock_restart: N_TALKERS_P=%0d outside 1..16 (4-bit idx).",
           N_TALKERS_P);
  if (HOLD_PDU_P < 8)
    $error("KL_media_clock_restart: HOLD_PDU_P=%0d below the 1722-2016 4.4.4.3 floor of 8.",
           HOLD_PDU_P);

  localparam int unsigned IXW_C   = $clog2(N_TALKERS_P == 1 ? 2 : N_TALKERS_P);
  localparam int unsigned HOLDW_C = $clog2(HOLD_PDU_P + 1);

  //! per-talker target: the level each talker stamps once its hold allows.
  //! It differs from mr_o exactly while a restart is pending on that talker.
  logic [N_TALKERS_P-1:0]   tgt_r /* verilator public_flat_rw */;
  //! shadow of the media clock source; a difference is a source-change edge
  logic [15:0]              clk_src_q_r;
  wire                      src_change_w = (clk_src_q_r != clk_src_i);
  //! per-talker transmitted-PDU count since this talker's level last changed
  logic [HOLDW_C-1:0]       hold_r [N_TALKERS_P];

  wire                      idx_ok_w = 32'(frame_idx_i) < N_TALKERS_P;
  wire [IXW_C-1:0]          fidx_w   = frame_idx_i[IXW_C-1:0];

  always_ff @(posedge clk_i) begin : mcr_track
    if (!rst_n) begin
      tgt_r <= '0;
      mr_o  <= '0;
      clk_src_q_r <= 16'd0;
      for (int t = 0; t < N_TALKERS_P; t++)
        //! start satisfied: the first PDU of a fresh stream may carry the
        //! current truth immediately
        hold_r[t] <= HOLDW_C'(HOLD_PDU_P);
    end else begin
      clk_src_q_r <= clk_src_i;
      //! request on EITHER input: restart_p_i OR a media-clock source change.
      //! A no-op SET (same source) does not fire. Every talker's target
      //! becomes the complement of the level it stamps: a talker with a
      //! restart pending (tgt_r != mr_o) keeps its target, so the second
      //! request merges instead of cancelling the first (#387).
      if (restart_p_i | src_change_w) tgt_r <= ~mr_o;

      //! a completed PDU that carried this talker's CURRENT level counts
      //! toward its hold (saturating - only the >= comparison matters)
      if (frame_p_i && idx_ok_w && (frame_mr_i == mr_o[fidx_w])
          && (hold_r[fidx_w] != HOLDW_C'(HOLD_PDU_P)))
        hold_r[fidx_w] <= hold_r[fidx_w] + 1'b1;

      for (int t = 0; t < N_TALKERS_P; t++) begin
        if (!streaming_i[t]) begin
          //! no continuous stream to protect: stay adoptable and track the
          //! target directly, so nothing starts up with a stale bit
          mr_o[t]   <= tgt_r[t];
          hold_r[t] <= HOLDW_C'(HOLD_PDU_P);
        end
        else if ((mr_o[t] != tgt_r[t]) && (hold_r[t] == HOLDW_C'(HOLD_PDU_P))) begin : g_adopt
          mr_o[t]   <= tgt_r[t];
          hold_r[t] <= '0;
        end
      end
    end
  end : mcr_track

endmodule

`default_nettype wire
