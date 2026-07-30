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

                WHAT IS NOT IMPLEMENTED. The second trigger of 4.4.4.3 - "or
                if the mr bit in the CRF stream has been toggled" - needs the
                received CRF PDU's own mr bit, and KL_crf_rx does not parse it
                (it decodes pull/base/interval/dlen/type and the timestamps).
                Only the DISRUPTION trigger is wired. Recorded, not hidden:
                see docs/traceability/milan-v12.md.

  Spec refs   : IEEE 1722-2016 4.4.4.3 (+ 10.4.3 for the CRF talker side),
                Milan v1.2 5.3.7.7 Table 5.4 MEDIA_RESET
  Company     : Kebag Logic
------------------------------------------------------------------------------
*/

//! Per-talker AVTP mr level: a restart request flips an engine-wide target,
//! each talker adopts it once its own last change has been on the wire for
//! HOLD_PDU_P transmitted PDUs (1722-2016 4.4.4.3).

`default_nettype none

module KL_media_clock_restart #(
  parameter int unsigned N_TALKERS_P = 1,   //! talker stream contexts
  //! minimum PDUs the bit must hold its new state; 8 is the clause floor and
  //! raising it is legal (the clause sets a minimum, not a value)
  parameter int unsigned HOLD_PDU_P  = 8
)(
  input  wire                    clk_i,
  input  wire                    rst_n,

  //! media-clock restart request: one cycle per restart event. Today this is
  //! a disruption of the CRF stream our media clock is slaved to; any future
  //! "the media clock source changed" event (4.4.4.3's S/PDIF example) joins
  //! here with no change below.
  input  wire                    restart_p_i,

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

  //! engine-wide target: one media clock, so one restart history
  logic                     tgt_r;
  //! per-talker transmitted-PDU count since this talker's level last changed
  logic [HOLDW_C-1:0]       hold_r [N_TALKERS_P];

  wire                      idx_ok_w = 32'(frame_idx_i) < N_TALKERS_P;
  wire [IXW_C-1:0]          fidx_w   = frame_idx_i[IXW_C-1:0];

  always_ff @(posedge clk_i) begin : mcr_track
    if (!rst_n) begin
      tgt_r <= 1'b0;
      mr_o  <= '0;
      for (int t = 0; t < N_TALKERS_P; t++)
        //! start satisfied: the first PDU of a fresh stream may carry the
        //! current truth immediately
        hold_r[t] <= HOLDW_C'(HOLD_PDU_P);
    end else begin
      if (restart_p_i) tgt_r <= ~tgt_r;

      //! a completed PDU that carried this talker's CURRENT level counts
      //! toward its hold (saturating - only the >= comparison matters)
      if (frame_p_i && idx_ok_w && (frame_mr_i == mr_o[fidx_w])
          && (hold_r[fidx_w] != HOLDW_C'(HOLD_PDU_P)))
        hold_r[fidx_w] <= hold_r[fidx_w] + 1'b1;

      for (int t = 0; t < N_TALKERS_P; t++) begin
        if (!streaming_i[t]) begin
          //! no continuous stream to protect: stay adoptable and track the
          //! target directly, so nothing starts up with a stale bit
          mr_o[t]   <= tgt_r;
          hold_r[t] <= HOLDW_C'(HOLD_PDU_P);
        end
        else if ((mr_o[t] != tgt_r) && (hold_r[t] == HOLDW_C'(HOLD_PDU_P))) begin : g_adopt
          mr_o[t]   <= tgt_r;
          hold_r[t] <= '0;
        end
      end
    end
  end : mcr_track

endmodule

`default_nettype wire
