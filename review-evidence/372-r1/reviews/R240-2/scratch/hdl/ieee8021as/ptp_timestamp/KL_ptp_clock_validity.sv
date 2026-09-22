/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_ptp_clock_validity.sv
  Description : The one place that decides whether this end station is
                allowed to claim its AVTP presentation times correspond
                to gPTP time. Its single output is the AVTP "tu"
                (timestamp uncertain) bit that EVERY talker in the
                fabric stamps into every Stream Data AVTPDU it emits
                (AAF packetizer, legacy AAF talker, CRF talker).

                WHY IT EXISTS (measured, 2026-07-27). Our Arty streamed
                31 M AAF frames whose presentation times came from a PHC
                216,446 s (60 h) away from the domain, at full rate,
                with tu hard-wired to 0 the whole time. The receiving
                Milan device counted 99.4 % of them LATE or EARLY and
                had no way to defend itself, because the only field that
                exists to warn it - tu - said "the timestamps are fine".
                See docs/findings/REF_LISTENER_TIMESTAMP_SWEEP_0727.md.

                WHAT THE STANDARD ACTUALLY REQUIRES. Not "stop
                streaming": Milan v1.2 5.3.7.3 forbids that outright
                ("it shall be streaming AVTP packets ... STREAMING_WAIT
                shall not be implemented"). Not tv=0 either: IEEE
                1722-2016 7.5 makes tv=1 mandatory for every AAF AVTPDU
                when sp=0, which is our shape. The prescribed behaviour
                is to KEEP STREAMING and RAISE tu - Milan v1.2 4.3.5.2
                ("A Talker PAAD shall set the AVTP tu bit as described
                in [AVTP, Clause 4.4.4.7]"), IEEE 1722-2016 4.4.4.7, and
                Milan v1.2 Annex B.1.1 (on a grandmaster change tu shall
                be 1 for at least 0.25 s).

                THE THREE TERMS, and where the fabric owner's evidence lives:

                  * SYNC HEALTH (fabric_sync_ok_i). The on-chip gPTP engine
                    owns the servo and publishes its selected-and-synchronised
                    verdict directly. When the engine is not elaborated there
                    is no clock owner: sync and asCapable are structural zero
                    and tu is structural one. There is no software input at
                    all - the retired sw_* ports are deleted, so a CSR write
                    has nothing to reach. This boundary is information-theoretic - see
                    docs/design/PRESENTATION_TIME_WRAP.md: avtp_timestamp
                    is the LOW 32 BITS of an unsigned nanosecond count,
                    so it laps every 4.294967296 s, and once the true
                    offset exceeds one lap the modular difference carries
                    no information about the direction OR the magnitude
                    of the error. A far-off clock produces blocks of
                    100 % LATE and blocks of 100 % EARLY that are
                    indistinguishable from a well-behaved error signal -
                    which is precisely the square wave measured on
                    2026-07-27. No listener-side heuristic, and no
                    fabric-side observation of our own wire, can recover the
                    truth; only an active servo knows. An option-off build
                    therefore emits tu=1 forever, which is the honest answer,
                    not the convenient one.

                  * FABRIC-OBSERVED PHC STEPS (phc_load_p_i /
                    phc_adj_p_i). A settime or adjtime IS a discontinuity
                    in gPTP time by construction - 1722 4.4.4.7's exact
                    trigger - and unlike sync state it is fully visible
                    here, as the PTP_CMD strobes. No software help
                    needed, no software trust required.

                  * GRANDMASTER CHANGE (gm_id_i). The fabric owner publishes
                    gptp_grandmaster_id for the advertiser; a change in that
                    value is a change of grandmaster. Detecting it here gets
                    Milan Annex B.1.1 for free. The option-off identity is
                    always zero, so software cannot arm this path.

                The last two arm a holdover of HOLD_QTICK_P quarter-
                seconds (default 2 -> 0.25..0.5 s against a free-running
                prescaler, so the B.1.1 minimum holds for an event at
                any phase).

                tu_ivals_o is the Milan Table 5.4 / Table 5.6
                TIMESTAMP_UNCERTAIN counter for the talker side, in
                Milan's own units: the number of one-second observation
                intervals during which tu was set at least once (Milan
                allows any interval <= 1 s). It exists so software can
                tell "tu never asserted" from "nothing computes tu" -
                the second half of the decorative-ABI fix
                (docs/limitations/RECURRING_DEFECT_PATTERNS.md 1).

                asCAPABLE FOLLOWS THE FABRIC OWNER (gh #64 J3). 802.1AS-2020
                10.2.5.1: "A Boolean that is TRUE if and only if it is
                determined that this PTP Instance and the PTP Instance at
                the other end of the link attached to this PTP Port can
                interoperate with each other via the IEEE 802.1AS
                protocol" - and the clause adds that the determination is
                MEDIUM-DEPENDENT. The on-chip engine publishes that verdict
                through fabric_as_cap_i. Without the engine there is no
                exchange and asCapable remains false by construction.

  Spec refs   : Milan v1.2 4.3.5.2 (talker shall set tu), 5.3.7.3
                (streaming shall not stop), Annex B.1.1 (0.25 s on GM
                change), Table 5.4 / Table 5.6 (TIMESTAMP_UNCERTAIN =
                observation intervals), Table 5.22 (asCapable push);
                IEEE 802.1AS-2020 10.2.5.1 (asCapable); IEEE 1722-2016
                4.4.4.5 (tv), 4.4.4.7 (tu), 7.5 (AAF tv=1 at sp=0);
                docs/findings/REF_LISTENER_TIMESTAMP_SWEEP_0727.md
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

module KL_ptp_clock_validity #(
  //! cycles per 250 ms quarter-tick (= CLK_FREQ_HZ / 4). Simulation shapes
  //! override this so a holdover and an observation interval are reachable.
  parameter int unsigned QTICK_CYC_P  = 25_000_000,
  //! discontinuity holdover in quarter-ticks. 2 => 0.25..0.5 s against the
  //! free-running prescaler, so Milan v1.2 Annex B.1.1's 0.25 s minimum
  //! holds whatever the phase of the event.
  parameter int unsigned HOLD_QTICK_P = 2,
  //! The product datapath passes its gPTP elaboration option here. At 1, the
  //! engine's published sync/asCapable levels own the verdict. At 0 there is
  //! no owner, so sync/asCapable are zero and tu is one permanently.
  parameter bit FABRIC_GPTP_P = 1'b0
) (
  input  wire        clk_i,           //! datapath clock
  input  wire        rst_n,           //! active-low synchronous reset

  //! --- fabric gPTP publication bank ------------------------------------
  input  wire        fabric_sync_ok_i,//! engine has selected and synchronised to a GM
  input  wire        fabric_as_cap_i, //! engine's 802.1AS asCapable verdict
  input  wire        fabric_disc_p_i, //! pre-commit GM/sync discontinuity pulse

  //! --- discontinuities this fabric can see for itself -------------------
  input  wire        phc_load_p_i,    //! PTP_CMD[0] settime applied (a step)
  input  wire        phc_adj_p_i,     //! PTP_CMD[1] adjtime applied (a step)
  input  wire [63:0] gm_id_i,         //! ADP_GM_LO/HI gptp_grandmaster_id

  //! --- verdict -----------------------------------------------------------
  output wire        ts_uncertain_o,  //! AVTP tu bit for EVERY talker (1 = uncertain)
  output wire        as_capable_o,    //! active-owner asCapable (GET_AVB_INFO flags[0])
  output wire [31:0] stat_o,          //! CLKV_STAT 0x77C
  output wire [31:0] tu_ivals_o       //! CLKV_TUCNT 0x780 (Milan Table 5.4 counter)
);

  // --------------------------------------------------------------------
  //  250 ms prescaler - the single time base for the holdover and the
  //  observation interval.
  // --------------------------------------------------------------------
  localparam int unsigned QTICK_MAX_C = (QTICK_CYC_P < 2) ? 2 : QTICK_CYC_P;
  localparam int unsigned QDIV_W_C    = $clog2(QTICK_MAX_C);

  logic [QDIV_W_C-1:0] qdiv_r;
  logic                qtick_w;

  assign qtick_w = (qdiv_r == QDIV_W_C'(QTICK_MAX_C - 1));

  always_ff @(posedge clk_i) begin : p_prescale
    if (!rst_n) qdiv_r <= '0;
    else        qdiv_r <= qtick_w ? '0 : (qdiv_r + QDIV_W_C'(1));
  end

  // --------------------------------------------------------------------
  //  One possible owner. The option-off shape has no gPTP servo and cannot
  //  truthfully claim synchronisation or asCapable. Keep that fact in the
  //  combinational owner select so no state or software write can override it.
  // --------------------------------------------------------------------
  wire sync_ok_w = FABRIC_GPTP_P ? fabric_sync_ok_i : 1'b0;
  wire as_cap_w  = FABRIC_GPTP_P ? fabric_as_cap_i  : 1'b0;

  // --------------------------------------------------------------------
  //  Discontinuity holdover: PHC step or a fabric-owner change of
  //  grandmaster. Milan v1.2 Annex B.1.1.
  // --------------------------------------------------------------------
  localparam int unsigned HOLD_MAX_C = (HOLD_QTICK_P < 1) ? 1 : HOLD_QTICK_P;
  localparam int unsigned HOLD_W_C   = $clog2(HOLD_MAX_C + 1);

  logic [63:0]          gm_r;
  logic [HOLD_W_C-1:0]  hold_r;
  logic                 disc_p_w;
  logic                 hold_w;

  //! gm_r resets to 0 and gm_id_i resets to 0, so the active owner's first
  //! publication of a real grandmaster id IS a change and arms the holdover.
  //! That is correct: before it we did not know who the grandmaster was.
  assign disc_p_w = phc_load_p_i | phc_adj_p_i |
                    (FABRIC_GPTP_P &
                     (fabric_disc_p_i | (gm_id_i != gm_r)));
  assign hold_w   = (hold_r != '0);

  always_ff @(posedge clk_i) begin : p_hold
    if (!rst_n) begin
      gm_r   <= 64'd0;
      hold_r <= '0;
    end else begin
      gm_r <= gm_id_i;
      if (disc_p_w)                 hold_r <= HOLD_W_C'(HOLD_MAX_C);
      else if (qtick_w && hold_w)   hold_r <= hold_r - HOLD_W_C'(1);
    end
  end

  // --------------------------------------------------------------------
  //  The verdict. NOT a stream gate: Milan v1.2 5.3.7.3 forbids stopping
  //  a Stream Output, so the only honest lever is this bit.
  // --------------------------------------------------------------------
  //! Include the live discontinuity pulse, not only the registered hold. The
  //! PHC step/publication commit and an AVTP launch can share an edge; omitting
  //! this term lets that edge capture tu=0 before hold_r becomes visible.
  assign ts_uncertain_o = (~sync_ok_w) | hold_w | disc_p_w;

  // --------------------------------------------------------------------
  //  Milan Table 5.4 TIMESTAMP_UNCERTAIN: one increment per one-second
  //  observation interval in which tu was set at least once. 4 quarter-
  //  ticks == 1.000 s, the largest interval Milan allows.
  // --------------------------------------------------------------------
  logic [1:0]  ival_r;
  logic        tu_seen_r;
  logic [31:0] tu_ivals_r;

  always_ff @(posedge clk_i) begin : p_ival
    if (!rst_n) begin
      ival_r     <= 2'd0;
      tu_seen_r  <= 1'b0;
      tu_ivals_r <= 32'd0;
    end else begin
      if (ts_uncertain_o) tu_seen_r <= 1'b1;
      if (qtick_w) begin
        ival_r <= ival_r + 2'd1;
        if (ival_r == 2'd3) begin
          if (tu_seen_r || ts_uncertain_o) tu_ivals_r <= tu_ivals_r + 32'd1;
          tu_seen_r <= 1'b0;   //! start the next interval clean
        end
      end
    end
  end

  assign tu_ivals_o = tu_ivals_r;

  //! Fabric-owner asCapable for GET_AVB_INFO and its Table 5.22 push
  //! signature. Option-off has no owner and therefore reports false.
  assign as_capable_o = as_cap_w;

  //! CLKV_STAT: [0] tu now, [1] effective sync claim, [3] discontinuity
  //! holdover, [16] effective asCapable. Compatibility fields [2] and
  //! [15:4] are structural zero in every shape.
  assign stat_o = {15'd0, as_cap_w, 12'd0, hold_w, 1'b0, sync_ok_w,
                   ts_uncertain_o};

endmodule

`default_nettype wire
